Convert Korean people's Hangul names to romanized versions
==========================================================
|pipeline| |coverage|
Korean script (*Hangul*) has used various notations over the years to be
converted to latin (*Roman*) characters. The currently used official system for
normal words is **Revised Romanization (RR)**, which eliminated ambiguity in
the old system **McCune–Reischauer (McR)**. McR uses accented characters to
denote differences in pronounciation. Accented characters were commonly not used
in internet communications as they are hard to type and/or not well supported in
fonts. Over the years font support has improved tremendously, but keyboard
support is still flunky.

The lack of accents caused ambiguity in romanized words and people had to guess
from the context what the writer meant (*yo* and *yŏ* were both spelled as
*yo*). The Revised Romanization system uses plain characters from the `ASCII`_
range to denote the differences in pronounciation for example through the use of
multi-letter vowels (*yeo* instead of *yŏ*).

However, for people's names (famous or not), the rules are bent, because people
are used to a certain romanization of their name and have traditionally not
strictly adhered to one system or another. The classical example is that the
surname *김* is always romanized to *Kim*, whereas RR dictates *Gim*.

This library contains a set of rules that can be implemented to deviate from RR
notation using transliteration definitions and succession rules. It was inspired
by the author's work on `Dramawiki`_, which uses a documented set of prefences,
so that people with the same name in Hangul script, end up romanized exactly the
same. Since Dramawiki aims to support English readers it didn't make sense to
create pages with titles written in Hangul.

.. _ASCII: https://en.wikipedia.org/wiki/ASCII
.. _Dramawiki: https://wiki.d-addicts.com/DramaWiki:Korean_Personal_Names_Romanization_Preferences
.. |pipeline| image:: https://gitlab.com/venture-forth/hangul-names/badges/master/pipeline.svg
   :target: https://gitlab.com/venture-forth/hangul-names/-/commits/master
   :alt: Pipeline status
.. |coverage| image:: https://gitlab.com/venture-forth/hangul-names/badges/master/coverage.svg
   :target: https://gitlab.com/venture-forth/hangul-names/-/commits/master
   :alt: Coverage

