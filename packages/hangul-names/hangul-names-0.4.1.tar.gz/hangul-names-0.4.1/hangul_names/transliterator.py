# This is based on work by Jeong YunWon:
#
# Copyright (c) 2015, Jeong YunWon <jeong+hangul-romanize@youknowone.org>
#
# The interface and relations between objects has changed to match features
# needed for this library.
#
# Copyright (c) 2020 Melvyn Sopacua
#
import logging
import typing as t

from . import words

logger = logging.getLogger(__name__)


class RevisedRomanizationFormatter:
    @staticmethod
    def format_parts(parts: t.MutableSequence[str]) -> str:
        if len(parts) > 2:
            surname = parts.pop(0).capitalize()
            given = "-".join(parts).capitalize()
        else:
            surname, given = parts[0].capitalize(), parts[1].capitalize()

        return f"{surname} {given}"


class Transliterator(RevisedRomanizationFormatter):
    ruleset: words.SyllableRuleSet = words.revised_romanization
    syllable_overrides: t.Dict[str, str] = {}
    surname_overrides: t.Dict[str, str] = {
        "이": "lee",
    }
    letter_overrides: t.Dict[str, str] = {}

    def __init__(self):
        for hangul, latin in self.letter_overrides.items():
            old = self.ruleset.set_letter_romanization(hangul, latin)
            logger.debug(f"Letter override for {hangul}: {old} -> {latin}")

    def romanize(self, hangul: str) -> str:
        parts = []
        is_surname = True
        # The first try should always favor surname overrides
        # Then syllable overrides are favored
        # And finally delegated to Syllable class, which applies rules based on
        # letter order before direct letter lookups.
        for syllable in hangul:
            if is_surname and syllable in self.surname_overrides:
                parts.append(self.surname_overrides[syllable])
                is_surname = False
                continue

            if syllable in self.syllable_overrides:
                parts.append(self.syllable_overrides[syllable])
            else:
                parts.append(
                    words.Syllable(char=syllable, ruleset=self.ruleset).romanize()
                )

            is_surname = False

        logger.debug(f"Parts created: {parts}")
        return self.format_parts(parts)
