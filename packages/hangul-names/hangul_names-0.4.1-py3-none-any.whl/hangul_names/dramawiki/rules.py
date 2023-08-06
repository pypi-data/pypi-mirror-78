from ..words import Rule, Final

__all__ = (
    "gwo_to_kwo",
    "gwa_to_kwa",
    "gyeo_to_kyu",
    "gyu_to_kyu",
    "oe_to_oi",
    "si_to_shi",
    "silent_a",
    "silent_eo",
    "silent_u",
    "silent_o",
)
gwo_to_kwo = Rule(initial="ᄀ", vowel="ᅯ", result_initial="k")
gwa_to_kwa = Rule(initial="ᄀ", vowel="ᅪ", result_initial="k")
gyeo_to_kyu = Rule(initial="ᄀ", vowel="ᅧ", result_initial="k", result_vowel="yu")
gyu_to_kyu = Rule(initial="ᄀ", vowel="ᅲ", result_initial="k", result_vowel="yu")
oe_to_oi = Rule(vowel="ᅬ", final=Final.NOTHING, result_vowel="oi")
si_to_shi = Rule(initial="ᄉ", vowel="ᅵ", result_initial="sh")
silent_a = Rule(initial="ᄋ", vowel="ᅡ", result_vowel="ah")
silent_eo = Rule(initial="ᄋ", vowel="ᅥ", result_vowel="uh")
silent_u = Rule(initial="ᄋ", vowel="ᅮ", result_initial="w", result_vowel="oo")
silent_o = Rule(initial="ᄋ", vowel="ᅩ", result_vowel="oh")
