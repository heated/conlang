#!/usr/bin/env python3
"""Mode subsystems: numbers, dates, times, spell-out — encoders/decoders
over the payload (anti-check) space, plus the digit confusion analysis.

All worked examples in docs/spec/modes.md are generated here (see
`worked_examples`) so the documentation cannot drift from the code.

Usage:
  python3 tools/modes.py number 4207
  python3 tools/modes.py date 2026-08-08 [--year/--no-year]
  python3 tools/modes.py time 14:30 [also 14:37]
  python3 tools/modes.py spell NTNU
  python3 tools/modes.py examples          (regenerate the doc block)
  python3 tools/modes.py confusion         (digit corruption analysis)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phonology import Inventory, Syllable  # noqa: E402

# Mode particle assignments — PROVISIONAL until conlang-jbw fixes the
# particle budget. Values are (vowel, coda) of the h-onset particle.
MODE_PARTICLES = {
    "number": ("u", ""),
    "date": ("o", ""),
    "time": ("i", ""),
    "spell": ("e", ""),
    "phonetic": ("e", "n"),   # reserved, mechanism only
    "coord": ("i", "n"),
    "close": ("a", "s"),
    "close_checksum": ("o", "s"),
}

QUARTER_VOWELS = {0: "a", 15: "e", 30: "i", 45: "o"}
HOUR_TENS_CODA = {0: "", 1: "n", 2: "s"}

# Spell mode letter table — PROVISIONAL normative data (modes.md).
# Consonant letters that exist as onsets: onset + e. Vowel letters:
# payload-register h syllables. Others: nearest-sound onset + a
# (voiced stops to voiceless, r to l, f/v to w, x/z to s, q/g to k,
# y to j, b to p, d to t, h-the-letter to h+a... h letter uses ("h","a")
# which collides with vowel-letter A = ("h","a") — so letter H = ("h","u")
# wait, U = ("h","u"). Letter H uses coda: ("h","a","n").)
LETTERS = {
    "a": ("h", "a", ""), "b": ("p", "a", ""), "c": ("c", "e", ""),
    "d": ("t", "a", ""), "e": ("h", "e", ""), "f": ("w", "a", ""),
    "g": ("k", "a", ""), "h": ("h", "a", "n"), "i": ("h", "i", ""),
    "j": ("j", "e", ""), "k": ("k", "e", ""), "l": ("l", "e", ""),
    "m": ("m", "e", ""), "n": ("n", "e", ""), "o": ("h", "o", ""),
    "p": ("p", "e", ""), "q": ("k", "u", ""), "r": ("l", "a", ""),
    "s": ("s", "e", ""), "t": ("t", "e", ""), "u": ("h", "u", ""),
    "v": ("w", "e", ""), "w": ("w", "u", ""), "x": ("s", "a", ""),
    "y": ("j", "a", ""), "z": ("s", "u", ""),
}


class Modes:
    def __init__(self, inv: Inventory | None = None):
        self.inv = inv or Inventory()
        self.tens_onset = {o["digit_tens"]: o["roman"]
                           for o in self.inv.spec["onsets"]["content"]}
        self.onset_tens = {v: k for k, v in self.tens_onset.items()}
        self.units_rime = {u["digit"]: (u["vowel"], u["coda"])
                           for u in self.inv.spec["digit_units_rimes"]["map"]}
        self.rime_units = {v: k for k, v in self.units_rime.items()}

    # --- primitives ---

    def particle(self, mode: str) -> Syllable:
        v, c = MODE_PARTICLES[mode]
        return Syllable("h", v, c)

    def digit_pair_syllable(self, value: int) -> Syllable:
        if not 0 <= value <= 99:
            raise ValueError(f"digit pair out of range: {value}")
        vowel, coda = self.units_rime[value % 10]
        return Syllable(self.tens_onset[value // 10], vowel, coda)

    def syllable_digit_pair(self, syl: Syllable) -> int:
        tens = self.onset_tens.get(syl.onset)
        units = self.rime_units.get((syl.vowel, syl.coda))
        if tens is None or units is None:
            raise ValueError(f"not a digit-pair syllable: {syl}")
        return tens * 10 + units

    def rom(self, sylls: list[Syllable]) -> str:
        """Payload romanization (anti-check register, canonical doubling)."""
        return " ".join(self.inv.romanize_syllable(s, payload=True)
                        for s in sylls)

    def rom_particle(self, syl: Syllable) -> str:
        return self.inv.romanize_syllable(syl, payload=False)

    # --- numbers ---

    def number_pairs(self, n: int) -> list[int]:
        if n < 0:
            raise ValueError("negative numbers deferred to a math mode")
        digits = str(n)
        if len(digits) % 2:
            digits = "0" + digits
        return [int(digits[i:i + 2]) for i in range(0, len(digits), 2)]

    def encode_number(self, n: int, checksum: bool = False) -> list[str]:
        pairs = self.number_pairs(n)
        out = [self.rom_particle(self.particle("number"))]
        out += [self.rom([self.digit_pair_syllable(p)]) for p in pairs]
        if checksum:
            out.append(self.rom_particle(self.particle("close_checksum")))
            out.append(self.rom([self.digit_pair_syllable(self.checksum(pairs))]))
        return out

    def decode_number_pairs(self, pairs: list[int]) -> int:
        n = 0
        for p in pairs:
            n = n * 100 + p
        return n

    @staticmethod
    def checksum(pairs: list[int]) -> int:
        return sum((i + 1) * p for i, p in enumerate(pairs)) % 97

    # --- dates ---

    def encode_date(self, year: int | None, month: int, day: int) -> list[str]:
        out = [self.rom_particle(self.particle("date"))]
        if year is not None:
            out += [self.rom([self.digit_pair_syllable(p)])
                    for p in self.number_pairs(year)]
        if not (1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError("month 1-12, day 1-31")
        out.append(self.rom([self.digit_pair_syllable(month)]))
        out.append(self.rom([self.digit_pair_syllable(day)]))
        return out

    # --- times ---

    def time_syllable(self, hour: int, quarter: int) -> Syllable:
        """hour 0-23, quarter in {0,15,30,45} -> ONE payload syllable:
        onset = digit onset of hour%10, coda = hour tens (∅/n/s),
        vowel = quarter (a/e/i/o)."""
        if not 0 <= hour <= 23:
            raise ValueError("hour 0-23")
        if quarter not in QUARTER_VOWELS:
            raise ValueError("quarter in {0,15,30,45}")
        return Syllable(self.tens_onset[hour % 10],
                        QUARTER_VOWELS[quarter],
                        HOUR_TENS_CODA[hour // 10])

    def decode_time_syllable(self, syl: Syllable) -> tuple[int, int]:
        last = self.onset_tens[syl.onset]
        tens = {v: k for k, v in HOUR_TENS_CODA.items()}[syl.coda]
        quarter = {v: k for k, v in QUARTER_VOWELS.items()}[syl.vowel]
        hour = tens * 10 + last
        if hour > 23:
            raise ValueError(f"not a time syllable: {syl}")
        return hour, quarter

    def encode_time(self, hour: int, minute: int) -> list[str]:
        quarter = (minute // 15) * 15
        offset = minute - quarter
        out = [self.rom_particle(self.particle("time")),
               self.rom([self.time_syllable(hour, quarter)])]
        if offset:
            out.append(self.rom([self.digit_pair_syllable(offset)]))
        return out

    # --- spell ---

    def encode_spell(self, text: str) -> list[str]:
        out = [self.rom_particle(self.particle("spell"))]
        for ch in text.lower():
            if ch not in LETTERS:
                raise ValueError(f"no letter name for {ch!r}")
            o, v, c = LETTERS[ch]
            out.append(self.rom([Syllable(o, v, c)]))
        return out

    # --- digit confusion analysis (review obligation) ---

    def digit_confusion_analysis(self) -> dict:
        """Classify every single-channel corruption of every digit-pair
        payload syllable. Categories:
          silent      -> lands on another valid digit pair (only the
                         checksum or context can catch it)
          mode_gram   -> lands outside the digit grammar (invalid rime or
                         non-digit shape): detected by the mode parser
          register    -> the substituted value has a different check bit,
                         so the payload register flips: detectable by
                         register-sensitive listeners and machines even
                         when the result is a valid digit pair
        `register` overlaps `silent`: a silent-substitution that is also
        register-flagged is counted in both (reported separately).
        """
        onsets = self.inv.content_onsets
        vowels = self.inv.vowels
        codas = self.inv.codas
        ob = {o["roman"]: o["check"] for o in self.inv.spec["onsets"]["content"]}
        vb = {v["roman"]: v["check"] for v in self.inv.spec["vowels"]}
        cb = {c["roman"]: c["check"] for c in self.inv.spec["codas"]}
        stats = {"total": 0, "silent": 0, "mode_gram": 0,
                 "silent_register_flagged": 0}
        for value in range(100):
            syl = self.digit_pair_syllable(value)
            subs = ([(Syllable(o, syl.vowel, syl.coda), ob[syl.onset] != ob[o])
                     for o in onsets if o != syl.onset]
                    + [(Syllable(syl.onset, v, syl.coda), vb[syl.vowel] != vb[v])
                       for v in vowels if v != syl.vowel]
                    + [(Syllable(syl.onset, syl.vowel, c), cb[syl.coda] != cb[c])
                       for c in codas if c != syl.coda])
            for corrupted, register_flagged in subs:
                stats["total"] += 1
                try:
                    self.syllable_digit_pair(corrupted)
                    stats["silent"] += 1
                    if register_flagged:
                        stats["silent_register_flagged"] += 1
                except ValueError:
                    stats["mode_gram"] += 1
        return stats


def worked_examples(m: Modes) -> list[tuple[str, str]]:
    ex = []
    ex.append(("42", " ".join(m.encode_number(42))))
    ex.append(("4207", " ".join(m.encode_number(4207))))
    ex.append(("4207 with checksum", " ".join(m.encode_number(4207, checksum=True))))
    ex.append(("0", " ".join(m.encode_number(0))))
    ex.append(("1000000", " ".join(m.encode_number(1000000))))
    ex.append(("date 2026-08-08", " ".join(m.encode_date(2026, 8, 8))))
    ex.append(("date 08-08 (yearless)", " ".join(m.encode_date(None, 8, 8))))
    ex.append(("time 14:30", " ".join(m.encode_time(14, 30))))
    ex.append(("time 14:37", " ".join(m.encode_time(14, 37))))
    ex.append(("time 08:00", " ".join(m.encode_time(8, 0))))
    ex.append(("time 23:45", " ".join(m.encode_time(23, 45))))
    ex.append(("spell NTNU", " ".join(m.encode_spell("NTNU"))))
    ex.append(("spell ZOE", " ".join(m.encode_spell("ZOE"))))
    return ex


def main() -> int:
    m = Modes()
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    cmd = args[0]
    if cmd == "number":
        print(" ".join(m.encode_number(int(args[1]),
                                       checksum="--checksum" in args)))
    elif cmd == "date":
        y, mo, dd = args[1].split("-")
        year = None if "--no-year" in args else int(y)
        print(" ".join(m.encode_date(year, int(mo), int(dd))))
    elif cmd == "time":
        hh, mm = args[1].split(":")
        print(" ".join(m.encode_time(int(hh), int(mm))))
    elif cmd == "spell":
        print(" ".join(m.encode_spell(args[1])))
    elif cmd == "examples":
        for label, rendering in worked_examples(m):
            print(f"| {label} | `{rendering}` |")
    elif cmd == "confusion":
        for k, v in m.digit_confusion_analysis().items():
            print(f"{k:28s} {v}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
