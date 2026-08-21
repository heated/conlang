#!/usr/bin/env python3
"""Mode subsystems: numbers, dates, times, spell-out — frame encoders AND
decoders over the payload (anti-check) space, with checksum verification
and the digit confusion analysis.

Frame grammar (romanized, space-separated tokens):
  frame    := particle payload* [close]
  close    := 'haas' | 'hoos' checksum-symbol
  number   := hu pair+                     (base-100, big-endian)
  date     := ho pair{2}                   (yearless: month day)
            | ho pair{4} | ho pair{5}      (year 4 or 6 digits, month, day)
  time     := hi cell [offset-pair [seconds-pair]]
  spell    := he letter+

Checksum: every payload symbol has a value <= 100 (digit pairs: the pair
value; time cells: 4*hour+quarter; letters: A=0..Z=25; offset pairs: the
pair value). checksum = sum((i+1) * value_i) mod 101 over the payload,
frame capped at 100 symbols. 101 is prime and exceeds every value delta,
so every single-symbol substitution (within the same symbol class) and
every transposition changes the checksum. The checksum symbol encodes
0-99 as a digit pair and 100 as `cas` (payload register).

All doc tables in docs/spec/modes.md are generated here (`examples`,
`particles`, `letters`, `confusion` subcommands) and exactly asserted by
tools/test_modes.py.
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
    "coord": ("i", "n"),      # reserved, sketch only
    "close": ("a", "s"),
    "close_checksum": ("o", "s"),
    "chunk_sep": ("a", "n"),  # list separator; also the residue-100 escape
}

QUARTER_VOWELS = {0: "a", 15: "e", 30: "i", 45: "o"}
HOUR_TENS_CODA = {0: "", 1: "n", 2: "s"}

CHECKSUM_MOD = 101
MAX_FRAME_SYMBOLS = 100
# Residue 100 has no symbol (v2 codebook, conlang-bd3/3mq): the sparse
# 100-point codebook spends its margin, so no clean 101st syllable
# exists — the old `cas` escape is now digit 36. Instead residue 100 is
# made UNREACHABLE by the chunking rule: a checksummed payload whose
# residue is 100 is split at the latest point where neither part has
# residue 100, and the parts are joined by the chunk separator. A split
# always exists because a single pair's residue is its own value <= 99.

# Spell mode letter table — PROVISIONAL normative data. Design rules:
# consonants whose sound is an onset: onset + e; vowel letters: c + that
# vowel + coda l (no h-onset anywhere in payloads — a payload h-syllable
# differs from a mode particle only by register, which length-deaf
# listeners cannot hear); remaining consonants: nearest-sound onset + a
# (or +u where +a is taken). No letter uses a digit rime shape with its
# tens onset... (letters and digit pairs share the space; the mode
# separates them — the constraint that matters is no h-onsets).
LETTERS = {
    "a": ("c", "a", "l"), "b": ("p", "a", ""), "c": ("c", "e", ""),
    "d": ("t", "a", ""), "e": ("c", "e", "l"), "f": ("w", "a", ""),
    "g": ("k", "a", ""), "h": ("k", "a", "l"), "i": ("c", "i", "l"),
    "j": ("j", "e", ""), "k": ("k", "e", ""), "l": ("l", "e", ""),
    "m": ("m", "e", ""), "n": ("n", "e", ""), "o": ("c", "o", "l"),
    "p": ("p", "e", ""), "q": ("k", "u", ""), "r": ("l", "a", ""),
    "s": ("s", "e", ""), "t": ("t", "e", ""), "u": ("c", "u", "l"),
    "v": ("w", "e", ""), "w": ("w", "u", ""), "x": ("s", "a", ""),
    "y": ("j", "a", ""), "z": ("s", "u", ""),
}
LETTER_ORDER = "abcdefghijklmnopqrstuvwxyz"


class FrameError(ValueError):
    pass


class Modes:
    def __init__(self, inv: Inventory | None = None):
        self.inv = inv or Inventory()
        self.tens_onset = {o["digit_tens"]: o["roman"]
                           for o in self.inv.spec["onsets"]["content"]}
        self.onset_tens = {v: k for k, v in self.tens_onset.items()}
        self.units_rime = {u["digit"]: (u["vowel"], u["coda"])
                           for u in self.inv.spec["digit_units_rimes"]["map"]}
        self.rime_units = {v: k for k, v in self.units_rime.items()}
        self.particle_by_shape = {v: k for k, v in MODE_PARTICLES.items()}
        self.letter_by_shape = {v: k for k, v in LETTERS.items()}

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

    def rom(self, sylls: list[Syllable]) -> list[str]:
        return [self.inv.romanize_syllable(s, payload=True) for s in sylls]

    def rom_particle(self, mode: str) -> str:
        return self.inv.romanize_syllable(self.particle(mode), payload=False)

    # --- checksum over payload symbol values ---

    @staticmethod
    def checksum(values: list[int]) -> int:
        if len(values) > MAX_FRAME_SYMBOLS:
            raise FrameError(f"frame exceeds {MAX_FRAME_SYMBOLS} symbols")
        if any(not 0 <= v <= 100 for v in values):
            raise FrameError("checksum values must be 0-100")
        return sum((i + 1) * v for i, v in enumerate(values)) % CHECKSUM_MOD

    def checksum_syllable(self, value: int) -> Syllable:
        if value == 100:
            raise FrameError(
                "checksum residue 100 has no symbol — split the payload "
                "with the chunk separator (see chunk_payload)")
        return self.digit_pair_syllable(value)

    def read_checksum_syllable(self, syl: Syllable) -> int:
        return self.syllable_digit_pair(syl)

    def chunk_payload(self, values: list[int]) -> list[list[int]]:
        """Split a payload so no chunk has checksum residue 100
        (the residue-100 escape). Splits as late as possible; a split
        always exists since a single value <= 99 is its own residue."""
        if self.checksum(values) != 100:
            return [values]
        for cut in range(len(values) - 1, 0, -1):
            head, tail = values[:cut], values[cut:]
            if self.checksum(head) != 100 and self.checksum(tail) != 100:
                return [head] + self.chunk_payload(tail)
        raise FrameError(  # unreachable: single-value chunks are <= 99
            f"no residue-100-free split for {values}")

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
        out = [self.rom_particle("number")]
        if not checksum:
            return out + self.rom([self.digit_pair_syllable(p)
                                   for p in pairs])
        chunks = self.chunk_payload(pairs)
        for i, chunk in enumerate(chunks):
            if i:
                out.append(self.rom_particle("chunk_sep"))
            out += self.rom([self.digit_pair_syllable(p) for p in chunk])
            out.append(self.rom_particle("close_checksum"))
            out += self.rom([self.checksum_syllable(self.checksum(chunk))])
        return out

    # --- dates (wire rule: year is 0, 4, or 6 digits — 0, 2, or 3 pairs;
    #     payload lengths 2/4/5 pairs are the only legal date frames) ---

    def date_pairs(self, year: str | None, month: int, day: int) -> list[int]:
        if not (1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError("month 1-12, day 1-31")
        pairs = []
        if year is not None:
            y = year.lstrip("-")
            if len(y) not in (4, 6) or not y.isdigit():
                raise ValueError("year must be 4 or 6 digits on the wire")
            pairs += [int(y[i:i + 2]) for i in range(0, len(y), 2)]
        return pairs + [month, day]

    def encode_date(self, year: str | None, month: int, day: int,
                    checksum: bool = False) -> list[str]:
        pairs = self.date_pairs(year, month, day)
        out = [self.rom_particle("date")]
        out += self.rom([self.digit_pair_syllable(p) for p in pairs])
        if checksum:
            out.append(self.rom_particle("close_checksum"))
            out += self.rom([self.checksum_syllable(self.checksum(pairs))])
        return out

    # --- times ---

    def time_syllable(self, hour: int, quarter: int) -> Syllable:
        if not 0 <= hour <= 23:
            raise ValueError("hour 0-23")
        if quarter not in QUARTER_VOWELS:
            raise ValueError("quarter in {0,15,30,45}")
        return Syllable(self.tens_onset[hour % 10],
                        QUARTER_VOWELS[quarter],
                        HOUR_TENS_CODA[hour // 10])

    def decode_time_syllable(self, syl: Syllable) -> tuple[int, int]:
        last = self.onset_tens.get(syl.onset)
        tens = {v: k for k, v in HOUR_TENS_CODA.items()}.get(syl.coda)
        quarter = {v: k for k, v in QUARTER_VOWELS.items()}.get(syl.vowel)
        if last is None or tens is None or quarter is None:
            raise ValueError(f"not a time syllable: {syl}")
        hour = tens * 10 + last
        if hour > 23:
            raise ValueError(f"not a time syllable: {syl}")
        return hour, quarter

    def time_values(self, hour, quarter, offset, seconds) -> list[int]:
        vals = [4 * hour + quarter // 15]
        if offset is not None:
            vals.append(offset)
        if seconds is not None:
            vals.append(seconds)
        return vals

    def encode_time(self, hour: int, minute: int, second: int | None = None,
                    checksum: bool = False) -> list[str]:
        quarter = (minute // 15) * 15
        offset = minute - quarter
        out = [self.rom_particle("time")]
        sylls = [self.time_syllable(hour, quarter)]
        need_offset = bool(offset) or second is not None
        if need_offset:
            sylls.append(self.digit_pair_syllable(offset))
        if second is not None:
            sylls.append(self.digit_pair_syllable(second))
        out += self.rom(sylls)
        if checksum:
            vals = self.time_values(hour, quarter,
                                    offset if need_offset else None, second)
            out.append(self.rom_particle("close_checksum"))
            out += self.rom([self.checksum_syllable(self.checksum(vals))])
        return out

    # --- spell ---

    def encode_spell(self, text: str, checksum: bool = False) -> list[str]:
        out = [self.rom_particle("spell")]
        sylls, vals = [], []
        for ch in text.lower():
            if ch not in LETTERS:
                raise ValueError(f"no letter name for {ch!r}")
            sylls.append(Syllable(*LETTERS[ch]))
            vals.append(LETTER_ORDER.index(ch))
        out += self.rom(sylls)
        if checksum:
            out.append(self.rom_particle("close_checksum"))
            out += self.rom([self.checksum_syllable(self.checksum(vals))])
        return out

    # --- frame decoding ---

    def _classify(self, token: str) -> tuple[str, Syllable]:
        """-> ('particle', syl) for lexical-register h tokens,
              ('payload', syl) otherwise (payload register enforced)."""
        try:
            sylls = self.inv.parse_word(token, mode="structural")
        except ValueError as e:
            raise FrameError(f"unparseable token {token!r}: {e}")
        if len(sylls) != 1:
            raise FrameError(f"mode tokens are single syllables: {token!r}")
        syl = sylls[0]
        if syl.onset == "h":
            shape = (syl.vowel, syl.coda)
            if shape not in self.particle_by_shape:
                raise FrameError(f"unknown particle {token!r}")
            try:
                self.inv.parse_word(token, mode="lexical")  # register check
            except ValueError as e:
                raise FrameError(str(e))
            return "particle", syl
        try:
            self.inv.parse_word(token, mode="payload")
        except ValueError as e:
            raise FrameError(str(e))
        return "payload", syl

    def decode_frame(self, text: str) -> dict:
        """Decode a romanized mode frame. Returns a dict with 'mode',
        decoded fields, and 'checksum_ok' (None if no checksum given).
        Raises FrameError on any violation."""
        tokens = text.split()
        if not tokens:
            raise FrameError("empty frame")
        kind, syl = self._classify(tokens[0])
        if kind != "particle":
            raise FrameError("frame must open with a mode particle")
        mode = self.particle_by_shape[(syl.vowel, syl.coda)]
        if mode in ("close", "close_checksum", "phonetic", "coord"):
            raise FrameError(f"{mode} cannot open a frame")

        payload: list[Syllable] = []
        # chunked frames (residue-100 escape): each chunk carries its own
        # checksum; chunks concatenate into one payload and all their
        # checksums must verify.
        chunks: list[tuple[list[Syllable], int | None]] = []
        chunk: list[Syllable] = []
        check_val = None
        i = 1
        while i < len(tokens):
            kind, syl = self._classify(tokens[i])
            if kind == "particle":
                p = self.particle_by_shape[(syl.vowel, syl.coda)]
                if p == "close":
                    i += 1
                    break
                if p == "close_checksum":
                    if i + 1 >= len(tokens):
                        raise FrameError("hoos requires a checksum symbol")
                    _, csyl = self._classify(tokens[i + 1])
                    check_val = self.read_checksum_syllable(csyl)
                    i += 2
                    # a chunk separator may continue the frame
                    if i < len(tokens):
                        kind2, syl2 = self._classify(tokens[i])
                        if kind2 == "particle" and \
                                self.particle_by_shape[
                                    (syl2.vowel, syl2.coda)] == "chunk_sep":
                            if mode != "number":
                                raise FrameError(
                                    f"{mode} frames are not chunkable")
                            chunks.append((chunk, check_val))
                            chunk, check_val = [], None
                            i += 1
                            continue
                    break
                if p == "chunk_sep":
                    raise FrameError(
                        "chunk separator must follow a chunk checksum")
                raise FrameError(f"unexpected particle {tokens[i]!r} in frame")
            chunk.append(syl)
            i += 1
        if i < len(tokens):
            raise FrameError(f"trailing tokens after close: {tokens[i:]}")
        chunks.append((chunk, check_val))
        if any(not c for c, _ in chunks):
            raise FrameError("empty payload")
        payload = [s for c, _ in chunks for s in c]

        try:
            if len(chunks) > 1:
                for c, cv in chunks:
                    if cv is None:
                        raise FrameError("every chunk needs a checksum")
                    vals = [self.syllable_digit_pair(s) for s in c]
                    if self.checksum(vals) != cv:
                        return self._decode_payload(mode, payload, -1)
                return self._decode_payload(mode, payload, None) | \
                    {"checksum_ok": True, "chunks": len(chunks)}
            return self._decode_payload(mode, payload, check_val)
        except FrameError:
            raise
        except ValueError as e:
            raise FrameError(str(e))

    def _decode_payload(self, mode, payload, check_val) -> dict:
        if mode == "number":
            pairs = [self.syllable_digit_pair(s) for s in payload]
            result = {"mode": mode, "value": self._fold(pairs), "pairs": pairs}
            values = pairs
        elif mode == "date":
            pairs = [self.syllable_digit_pair(s) for s in payload]
            if len(pairs) == 2:
                year, (month, day) = None, pairs
            elif len(pairs) in (4, 5):
                ydigits = "".join(f"{p:02d}" for p in pairs[:-2])
                year, month, day = ydigits, pairs[-2], pairs[-1]
            else:
                raise FrameError(f"date frames carry 2, 4, or 5 pairs, "
                                 f"got {len(pairs)}")
            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise FrameError(f"invalid month/day {month}/{day}")
            result = {"mode": mode, "year": year, "month": month, "day": day}
            values = pairs
        elif mode == "time":
            hour, quarter = self.decode_time_syllable(payload[0])
            offset = second = None
            if len(payload) >= 2:
                offset = self.syllable_digit_pair(payload[1])
                if not 0 <= offset <= 14:
                    raise FrameError(f"minute offset 0-14, got {offset}")
            if len(payload) >= 3:
                second = self.syllable_digit_pair(payload[2])
                if not 0 <= second <= 59:
                    raise FrameError(f"seconds 0-59, got {second}")
            if len(payload) > 3:
                raise FrameError("time frames carry at most 3 symbols")
            result = {"mode": mode, "hour": hour,
                      "minute": quarter + (offset or 0), "second": second}
            values = self.time_values(hour, quarter, offset, second)
        elif mode == "spell":
            letters = []
            for s in payload:
                shape = (s.onset, s.vowel, s.coda)
                if shape not in self.letter_by_shape:
                    raise FrameError(f"not a letter symbol: {s}")
                letters.append(self.letter_by_shape[shape])
            result = {"mode": mode, "text": "".join(letters)}
            values = [LETTER_ORDER.index(ch) for ch in letters]
        else:  # pragma: no cover
            raise FrameError(f"undecodable mode {mode}")

        result["checksum_ok"] = (None if check_val is None
                                 else self.checksum(values) == check_val)
        return result

    @staticmethod
    def _fold(pairs: list[int]) -> int:
        n = 0
        for p in pairs:
            n = n * 100 + p
        return n

    # --- digit confusion analysis (review obligation) ---

    def digit_confusion_analysis(self) -> dict:
        """Classify every single-channel corruption of every digit-pair
        payload syllable: silent (another valid digit pair), mode_gram
        (breaks the digit grammar — caught by the frame parser), and how
        many silent ones are register-flagged (check bits differ)."""
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


# --- generated doc blocks (asserted verbatim by tests) ---

def examples_block(m: Modes) -> str:
    rows = [
        ("42", m.encode_number(42)),
        ("4207", m.encode_number(4207)),
        ("4207 with checksum", m.encode_number(4207, checksum=True)),
        ("0", m.encode_number(0)),
        ("1000000", m.encode_number(1000000)),
        ("date 2026-08-08", m.encode_date("2026", 8, 8)),
        ("date 08-08 (yearless)", m.encode_date(None, 8, 8)),
        ("time 14:30", m.encode_time(14, 30)),
        ("time 14:37", m.encode_time(14, 37)),
        ("time 08:00", m.encode_time(8, 0)),
        ("time 23:45", m.encode_time(23, 45)),
        ("spell NTNU", m.encode_spell("NTNU")),
        ("spell ZOE", m.encode_spell("ZOE")),
    ]
    lines = ["| value | rendering |", "|-------|-----------|"]
    for label, toks in rows:
        rendering = " ".join(toks)
        decoded = m.decode_frame(rendering)  # every doc example must decode
        assert decoded["checksum_ok"] is not False
        lines.append(f"| {label} | `{rendering}` |")
    return "\n".join(lines)


def particles_block(m: Modes) -> str:
    desc = {
        "number": "number: digit pairs follow, base-100, big-endian",
        "date": "date: [year pairs ×2-3] + month pair + day pair",
        "time": "time: one hour×quarter syllable [+ offset pair [+ seconds]]",
        "spell": "spell: one letter-name syllable per letter",
        "phonetic": "phonetic mode — reserved, mechanism only in v0.1",
        "coord": "coordinates — reserved, design sketched below",
        "close": "mode close (optional in casual speech)",
        "close_checksum": "mode close + checksum symbol follows",
        "chunk_sep": "chunk separator: next chunk of the same payload "
                     "(also the residue-100 escape)",
    }
    lines = ["| particle | canonical | mode |", "|----------|-----------|------|"]
    for mode, (v, c) in MODE_PARTICLES.items():
        lines.append(f"| h-{v}{'-' + c if c else ''} | "
                     f"`{m.rom_particle(mode)}` | {desc[mode]} |")
    return "\n".join(lines)


def letters_block(m: Modes) -> str:
    lines = ["| letter | rendering | letter | rendering |",
             "|--------|-----------|--------|-----------|"]
    half = 13
    for i in range(half):
        row = []
        for ch in (LETTER_ORDER[i], LETTER_ORDER[i + half]):
            syl = Syllable(*LETTERS[ch])
            row += [ch.upper(), f"`{m.inv.romanize_syllable(syl, payload=True)}`"]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def confusion_block(m: Modes) -> str:
    s = m.digit_confusion_analysis()
    return (f"total single-channel corruptions: {s['total']}; "
            f"silent digit substitutions: {s['silent']} "
            f"({100 * s['silent'] // s['total']}%); "
            f"caught by the frame grammar: {s['mode_gram']}; "
            f"silent but register-flagged: {s['silent_register_flagged']} "
            f"({100 * s['silent_register_flagged'] // s['silent']}% of silent)")


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
        year = None if "--no-year" in args else y
        print(" ".join(m.encode_date(year, int(mo), int(dd),
                                     checksum="--checksum" in args)))
    elif cmd == "time":
        hh, mm = args[1].split(":")
        print(" ".join(m.encode_time(int(hh), int(mm),
                                     checksum="--checksum" in args)))
    elif cmd == "spell":
        print(" ".join(m.encode_spell(args[1], checksum="--checksum" in args)))
    elif cmd == "decode":
        print(m.decode_frame(" ".join(args[1:])))
    elif cmd == "examples":
        print(examples_block(m))
    elif cmd == "particles":
        print(particles_block(m))
    elif cmd == "letters":
        print(letters_block(m))
    elif cmd == "confusion":
        print(confusion_block(m))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
