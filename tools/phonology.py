"""Library over docs/spec/channels.json: syllables, registers, romanization,
enumeration, and word validation. Stdlib only.

The spec file is the single source of truth; nothing phonological is
hardcoded here except the romanization surface conventions (single-letter
onsets, vowel doubling for the long register).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

SPEC_PATH = Path(__file__).resolve().parent.parent / "docs" / "spec" / "channels.json"


def load_spec(path: Path = SPEC_PATH) -> dict:
    return json.loads(Path(path).read_text())


@dataclass(frozen=True)
class Syllable:
    onset: str
    vowel: str
    coda: str  # "" for open syllables

    def __str__(self) -> str:
        return f"{self.onset}{self.vowel}{self.coda or ''}"


class Inventory:
    def __init__(self, spec: dict | None = None):
        self.spec = spec or load_spec()
        content = self.spec["onsets"]["content"]
        particle = self.spec["onsets"]["particle"]
        self.onset_records = {o["roman"]: o for o in content + particle}
        self.content_onsets = [o["roman"] for o in content]
        self.particle_onsets = [o["roman"] for o in particle]
        self.vowel_records = {v["roman"]: v for v in self.spec["vowels"]}
        self.vowels = list(self.vowel_records)
        self.coda_records = {c["roman"]: c for c in self.spec["codas"]}
        self.codas = list(self.coda_records)
        self.pos_by_coda = {c["roman"]: c["pos_class"] for c in self.spec["codas"]}
        self.coda_by_pos = {v: k for k, v in self.pos_by_coda.items()}
        ws = self.spec["word_shapes"]
        self.content_syllable_range = (ws["content"]["syllables"]["min"],
                                       ws["content"]["syllables"]["max"])
        self.glide_cells = {("j", "i"), ("w", "u")}

    # --- register ---

    def check_sum(self, syl: Syllable) -> int:
        return (self.onset_records[syl.onset]["check"]
                + self.vowel_records[syl.vowel]["check"]
                + self.coda_records[syl.coda]["check"])

    def register(self, syl: Syllable, payload: bool = False) -> int:
        """0 short / 1 long. Lexical register satisfies the check rule;
        payload syllables take the anti-check register."""
        lexical = self.check_sum(syl) % 2
        return 1 - lexical if payload else lexical

    # --- romanization ---

    def romanize_syllable(self, syl: Syllable, payload: bool = False,
                          double_long: bool = True) -> str:
        v = syl.vowel
        if double_long and self.register(syl, payload=payload) == 1:
            v = v * 2
        return f"{syl.onset}{v}{syl.coda}"

    def romanize_word(self, syllables: list[Syllable], payload: bool = False,
                      double_long: bool = True) -> str:
        return "".join(self.romanize_syllable(s, payload, double_long)
                       for s in syllables)

    def parse_word(self, text: str) -> list[Syllable]:
        """Parse one romanized word (no spaces) into syllables.

        Deterministic because onsets are mandatory: a consonant followed
        by a vowel is always an onset; a consonant not followed by a
        vowel is a coda. Doubled vowels (long register) are accepted and
        collapsed — register is derivable, so parsing ignores it.
        """
        onsets = set(self.onset_records)
        vowels = set(self.vowel_records)
        codas = {c for c in self.coda_records if c}
        sylls: list[Syllable] = []
        i, n = 0, len(text)
        while i < n:
            if text[i] not in onsets:
                raise ValueError(f"expected onset at {i} in {text!r}")
            onset = text[i]
            i += 1
            if i >= n or text[i] not in vowels:
                raise ValueError(f"expected vowel at {i} in {text!r}")
            vowel = text[i]
            i += 1
            if i < n and text[i] == vowel:  # doubled = long register marking
                i += 1
            coda = ""
            if i < n and text[i] in codas:
                # coda only if not the onset of a following syllable
                nxt = i + 1
                if nxt >= n or text[nxt] not in vowels:
                    coda = text[i]
                    i += 1
            sylls.append(Syllable(onset, vowel, coda))
        return sylls

    # --- enumeration ---

    def iter_triples(self, onsets: list[str]) -> Iterator[Syllable]:
        for o in onsets:
            for v in self.vowels:
                for c in self.codas:
                    yield Syllable(o, v, c)

    def lexical_content_syllables(self) -> list[Syllable]:
        """All content-onset triples (register computed). Includes glide
        cells — exclusion is a lexicon rule, not a phonotactic one."""
        return list(self.iter_triples(self.content_onsets))

    def particle_syllables(self) -> list[Syllable]:
        return list(self.iter_triples(self.particle_onsets))

    # --- validation ---

    def validate_content_word(self, syllables: list[Syllable],
                              pos: str | None = None) -> list[str]:
        issues = []
        lo, hi = self.content_syllable_range
        if not lo <= len(syllables) <= hi:
            issues.append(f"content words are {lo}-{hi} syllables, got {len(syllables)}")
        for s in syllables:
            if s.onset in self.particle_onsets:
                issues.append(f"particle onset {s.onset!r} inside a content word")
            if (s.onset, s.vowel) in self.glide_cells:
                issues.append(f"glide cell {s.onset}{s.vowel} is not lexical")
        if syllables:
            final = syllables[-1]
            cls = self.pos_by_coda[final.coda]
            if cls == "reserved":
                issues.append(f"final coda {final.coda!r} is a reserved POS class")
            if pos is not None and cls != pos:
                issues.append(f"final coda {final.coda!r} is {cls}, expected {pos}")
        return issues

    def validate_particle(self, syllables: list[Syllable]) -> list[str]:
        issues = []
        if len(syllables) != 1:
            issues.append("particles are exactly one syllable")
        for s in syllables:
            if s.onset not in self.particle_onsets:
                issues.append(f"particle onset must be h, got {s.onset!r}")
        return issues


# --- pairwise lexicon conflicts (assignment-time checks) ---

def _pair_set(policy_block: dict) -> dict[str, set[frozenset[str]]]:
    return {channel: {frozenset(p) for p in pairs}
            for channel, pairs in policy_block.items() if channel != "comment"}


class ConflictRules:
    def __init__(self, inv: Inventory):
        self.inv = inv
        pol = inv.spec["confusion_policy"]
        self.forbidden = _pair_set(pol["forbidden"])
        self.weighted = _pair_set(pol["weighted"])
        cor = inv.spec["spacing_rules_v01"]
        # coronal-i pairs are a structural rule, not in confusion_policy
        self.coronal_i_onsets = [frozenset(("t", "c")), frozenset(("s", "c"))]

    def single_substitution(self, a: list[Syllable], b: list[Syllable]
                            ) -> tuple[str, frozenset[str]] | None:
        """If words a and b differ in exactly one channel of one syllable,
        return (channel, {value_a, value_b}); else None."""
        if len(a) != len(b):
            return None
        diff = None
        for sa, sb in zip(a, b):
            for channel in ("onset", "vowel", "coda"):
                va, vb = getattr(sa, channel), getattr(sb, channel)
                if va != vb:
                    if diff is not None:
                        return None
                    diff = (channel, frozenset((va, vb)))
        return diff

    def classify_pair(self, a: list[Syllable], b: list[Syllable],
                      same_root: bool = False) -> str:
        """'ok' | 'weighted' | 'forbidden' for coexistence in the lexicon."""
        sub = self.single_substitution(a, b)
        if sub is None:
            return "ok"
        channel, values = sub
        if same_root and channel == "coda":
            return "ok"  # POS alternation exemption (SPEC §4.3 rule 2)
        if channel == "onset" and values in self.coronal_i_onsets:
            # forbidden only before /i/ (SPEC §4.3 coronal-i rule)
            idx = next(i for i, (sa, sb) in enumerate(zip(a, b))
                       if sa.onset != sb.onset)
            if a[idx].vowel == "i":
                return "forbidden"
        if values in self.forbidden.get(channel, set()):
            return "forbidden"
        if values in self.weighted.get(channel, set()):
            return "weighted"
        # different check bits: register-detected; still distance-relevant
        # for length-deaf listeners — callers may weight it separately.
        return "ok"

    def fake_geminate(self, word: list[Syllable]) -> bool:
        return any(s1.coda and s1.coda == s2.onset
                   for s1, s2 in zip(word, word[1:]))

    def echo_vowel_conflict(self, a: list[Syllable], b: list[Syllable]) -> bool:
        """True if b is a plus an echo vowel on a final s/l coda:
        /...Cs/ vs /...C + su/-type (any echo vowel)."""
        for shorter, longer in ((a, b), (b, a)):
            if len(longer) != len(shorter) + 1:
                continue
            if not shorter or shorter[-1].coda not in ("s", "l"):
                continue
            if longer[:-1] == [*shorter[:-1],
                               Syllable(shorter[-1].onset, shorter[-1].vowel, "")] \
                    and longer[-1].onset == shorter[-1].coda \
                    and longer[-1].coda == "":
                return True
        return False

    def tosmabru_conflict(self, word: list[Syllable],
                          particles: list[Syllable],
                          lexicon: set[str]) -> list[str]:
        """Resyllabification hazards: word ends in a consonant coda and a
        following h-dropped particle could resyllabify into a legal word.
        Returns the romanized hazard strings found in `lexicon`."""
        hazards = []
        if not word or not word[-1].coda:
            return hazards
        final = word[-1]
        for p in particles:
            merged = [*word[:-1], Syllable(final.onset, final.vowel, ""),
                      Syllable(final.coda, p.vowel, p.coda)]
            key = "".join(str(s) for s in merged)
            if key in lexicon:
                hazards.append(key)
        return hazards
