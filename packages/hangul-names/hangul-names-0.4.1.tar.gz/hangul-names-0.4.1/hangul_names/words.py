# This is based on work by Jeong YunWon:
#
# Copyright (c) 2015, Jeong YunWon <jeong+hangul-romanize@youknowone.org>
#
# The interface and relations between objects has changed to match features
# needed for this library.
#
# Copyright (c) 2020 Melvyn Sopacua
#
from __future__ import annotations

import typing as t
import warnings

from . import defs


class Letter:
    base = 0x0

    def __init__(self, hangul: str, default_transliteration: str = ""):
        self.hangul = hangul
        self.code = ord(self.hangul)
        self.index = self.code - self.base
        self.translit = default_transliteration

    def clone(self):
        return self.__class__(self.hangul, self.translit)

    def set_transliteration(self, value: str) -> str:
        old = self.translit
        self.translit = value
        return old

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.hangul} ({self.translit}) U+{hex(self.code)}/{self.index}>"

    def __eq__(self, other: t.Any):
        if not hasattr(other, "hangul"):
            return False
        return self.hangul == other.hangul


_L = t.TypeVar("_L", bound=Letter)


class Initial(Letter):
    base = defs.UCD_INITIAL_CONSONANT_START


class Vowel(Letter):
    base = defs.UCD_VOWEL_START


class Final(Letter):
    base = defs.UCD_FINAL_CONSONANT_START
    MAX = defs.UCD_FINAL_CONSONANT_START + 27
    NOTHING = chr(defs.UCD_FINAL_CONSONANT_START)


class Rule:
    def __init__(
        self,
        initial: t.Optional[str] = None,
        vowel: t.Optional[str] = None,
        final: t.Optional[str] = None,
        result_initial: t.Optional[str] = None,
        result_vowel: t.Optional[str] = None,
        result_final: t.Optional[str] = None,
    ):
        self.initial = initial
        self.vowel = vowel
        self.final = final
        self.result = {
            "initial": result_initial,
            "vowel": result_vowel,
            "final": result_final,
        }

    def match(
        self,
        initial: t.Optional[Initial] = None,
        vowel: t.Optional[Vowel] = None,
        final: t.Optional[Final] = None,
    ) -> bool:
        if initial is None and vowel is None and final is None:
            return False

        if (
            initial
            and initial.hangul == self.initial
            and vowel
            and vowel.hangul == self.vowel
        ):
            return True

        if (
            vowel
            and vowel.hangul == self.vowel
            and final
            and final.hangul == self.final
        ):
            return True

        return False

    def apply(self, syllable: Syllable):
        """
        Default rule application

        This implementation will work for most if not all rules, but can be
        overridden by subclasses. For the syllable passed in, its letter
        transliteration must be modified to reflect the desired result.

        :param syllable: The syllable to apply the rule to
        """
        for name in "initial", "vowel", "final":
            if self.result[name] is not None:
                orig = getattr(syllable, name)
                clone = orig.clone()
                clone.set_transliteration(self.result[name])
                setattr(syllable, name, clone)


class SyllableRuleSet:
    """
    A SyllableRuleSet consists of the following:
    - Ways to extract initial consonants, vowels and final consonants from a
      hangul syllable.
    - 1 to 1 mappings from letters to romanized versions of those letters
    - rules that change the 1 to 1 mappings based on the letter that follows
    - A process that converts a hangul syllable to its romanized version taking
      into account the mappings and rules.
    """

    supported_types = ("initials", "vowels", "finals")

    def __init__(self):
        """
        Setup various mappings so we can find what we're looking for

        Creates various mappings and range restrictions for validation and
        transliteration of input data.
        """
        self._hangul_map = {}
        self._class_map = {"initials": Initial, "vowels": Vowel, "finals": Final}
        self.initials: t.List[Initial] = []
        self.vowels: t.List[Vowel] = []
        self.finals: t.List[Final] = []
        self.rules: t.List[Rule] = []
        for _type in self.__class__.supported_types:
            self._setup_letter(_type)

        if "initials" in self.supported_types:
            self.initials_range = (self.initials[0].code, self.initials[-1].code)
        if "vowels" in self.supported_types:
            self.vowels_range = (self.vowels[0].code, self.vowels[-1].code)
        if "finals" in self.supported_types:
            self.finals_range = (self.finals[1].code, self.finals[-1].code)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def _setup_letter(self, type_: str):
        """
        Abstraction that orders `Initial`, `Vowel` and `Final` instance onto
        that matches the unicode position from their `base` attribute.

        Semantically, this allows us to fetch one letter instance that will be
        used for every syllable transliteration that contains the letter.

        :param type_: One of the supported types
        :return:
        """
        assert type_ in self.__class__.supported_types, f"{type_}: Illegal type"
        letter_list = getattr(self, type_.lower())
        rr_list = getattr(defs, f"REVISED_{type_.upper()}")
        letter_class = self._class_map[type_]
        if not letter_list:
            for i, rr in enumerate(rr_list):
                letter = letter_class(chr(letter_class.base + i), rr)
                letter_list.append(letter)
                self._hangul_map[letter.hangul] = letter

        else:
            warnings.warn(f"{type_.capitalize()} already setup", RuntimeWarning)

    def set_letter_romanization(self, hangul: str, value: str) -> str:
        letter = self._lookup_letter(hangul)
        return letter.set_transliteration(value)

    def _lookup_letter(self, hangul) -> _L:
        try:
            return self._hangul_map[hangul]
        except KeyError:
            if ord(hangul) > Final.MAX:
                raise ValueError(f"{ord(hangul)} out of range (> {Final.MAX})")
            if ord(hangul) < Initial.base:
                raise ValueError(f"{ord(hangul)} out of range (< {Initial.base})")
            raise


revised_romanization = SyllableRuleSet()


class Syllable:
    """
    Hangul syllable interface

    It is based on the organization of codepoints of the Korean Hangul script
    in the unicode database. This algorithm is described in the wikipedia
     article `Korean language and computers`_.

    There are:
    - 18 initial consonants
    - 20 medial vowels
    - 27 final consonants: 15 of the previous consonants, 1 sentinel that is
      silent and 11 doubles, who incoporporate rules of succession that have no
      exceptions. Characters that if followed by another consonant have a
      consistent representation:
      - ᆪ: ks
      - ᆬ: nch
      - ᆭ: nh
      - ᆰ: lg
      - ᆱ: lm
      - ᆲ: lb
      - ᆳ: ls
      - ᆴ: lt
      - ᆵ: lp
      - ᆶ: lh
      - ᆹ: ps

    Each of these can be assigned zero or more roman characters to form the
    romanized version. Various standards exist and some publications use
    deviations from those standards to suit their own needs.

    .. _`Korean language and computers`: https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode
    """

    MIN = ord("가")
    MAX = ord("힣")

    def __init__(self, char: str, ruleset: SyllableRuleSet = revised_romanization):
        self.code = ord(char)
        self.char = char
        self.ruleset = ruleset
        if self.is_hangul:
            self.initial = self.ruleset.initials[self.index // 588]
            self.vowel = self.ruleset.vowels[(self.index // 28) % 21]
            self.final = self.ruleset.finals[self.index % 28]

    @property
    def is_hangul(self):
        # The common case that this returns false is space (0x20) and other
        # punctuation.
        return self.MIN <= self.code <= self.MAX

    @property
    def index(self) -> int:
        return self.code - self.MIN

    def romanize(self) -> str:
        if not self.is_hangul:
            return self.char
        for rule in self.ruleset.rules:
            if rule.match(self.initial, self.vowel, self.final):
                rule.apply(self)
        return "".join(
            [self.initial.translit, self.vowel.translit, self.final.translit]
        )

    @classmethod
    def all_ending_with(cls, letter: str) -> t.Set[Syllable]:
        qs = set()
        for i in range(cls.MIN, cls.MAX):
            if (i - cls.MIN) % 28 == ord(letter) - Final.base:
                qs.add(Syllable(chr(i)))
        return qs

    def __str__(self):
        return self.char

    def __repr__(self):
        return """<Syllable {} ({}) -> {} {} {}>""".format(
            self.code, self.char, self.initial, self.vowel, self.final,
        )

    def __eq__(self, other: t.Any):
        if not hasattr(other, "char"):
            return False
        return self.char == other.char

    def __hash__(self):
        return self.char.__hash__()
