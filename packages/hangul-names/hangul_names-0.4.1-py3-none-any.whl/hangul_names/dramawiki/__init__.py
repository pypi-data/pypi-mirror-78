import string
import typing as t

from . import rules
from ..transliterator import Transliterator
from ..words import SyllableRuleSet


class DramaWikiFormatter:
    @staticmethod
    def format_parts(parts: t.Sequence[str]) -> str:
        return string.capwords(" ".join(parts))


class DramaWiki(DramaWikiFormatter, Transliterator):
    ruleset = SyllableRuleSet()
    syllable_overrides = {
        "서": "suh",
        "영": "young",
        "강": "kang",
        "이": "yi",
        "의": "eui",
        "허": "huh",
    }
    surname_overrides = {
        "김": "kim",
        "박": "park",
        "이": "lee",
    }
    letter_overrides = {"ᅧ": "yu", "ᅥ": "u", "ᅮ": "oo", "ᅴ": "ee", "ᅲ": "yoo"}

    def __init__(self):
        super().__init__()
        for rule in rules.__all__:
            self.ruleset.add_rule(getattr(rules, rule))


class DramaWikiRR(DramaWikiFormatter, Transliterator):
    pass
