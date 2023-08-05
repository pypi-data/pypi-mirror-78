"""
Separate home for useful, pre-compiled regular expressions.

Just about every seasoned programmer has their own opinion of regular
expressions. It's been my experience that most seem to avoid them, and
not without good reason. They have a nack for getting fairly complicated
rather quickly and tend to be extraordinarily difficult to alter or
maintain without breaking them should the need arise. I.e. they can be
quite brittle. However, this can be somewhat mitigated through good
design and decent documentation, both of which hopefully exist herein.

In this module there are two main groups of pre-compiled regular
expressions. The first three: :data:`.NUMERIC_STRING`,
:data:`.NUMERAL_STRING`, and :data:`.PERIOD_STRING` all help with
processing :func:`.number2text` and :func:`.text2number` input. The last
four: :data:`.PREFIX_EXCEPTION_X`, :data:`.PREFIX_EXCEPTION_S`,
:data:`.PREFIX_EXCEPTION_M`, and :data:`.PREFIX_EXCEPTION_N` are all
used to catch and adjust invalid prefix combinations when
:data:`.ZILLION_PERIOD_PREFIXES` is initialized.
"""

import re


NUMERIC_STRING = re.compile(
    r"^\s*(?# match, but exclude any leading whitespace)"
    r"(?P<bsign>[-+])?(?# capture base sign if it exists)"
    r"(?!\s*\.\s*(?:[eE]|$))(?# whole or fraction must match)"
    r"0*(?# match, but exclude leading zeros from base whole)"
    r"(?P<bwhole>\d+)?(?# capture base whole number value)"
    r"(?:\.(?# only match base fraction following decimal)"
    r"(?P<bfraction>\d*[1-9])?(?# capture base fraction value)"
    r"0*)?(?# match, but exclude trailing zeros from base fraction)"
    r"(?:(?<=[.\d])(?# exponent flag must follow a digit or decimal)"
    r"[eE](?# only match exponent preceded by an e/E flag)"
    r"(?P<esign>[-+])?(?# capture exponent sign if exists)"
    r"0*(?# match, but exclude leading zeros from exponent value)"
    r"(?P<evalue>\d+)?)?(?# capture exponent value if exists)"
    r"(?<=[.\d])(?# number must end in decimal or digit to be valid)"
    r"\s*(?# match, but exclude any trailing whitespace)$")
"""
Pattern for matching number-like strings.

This compiled regular expression captures the numerical elements of a
number-like string (a string which could be cast to an int or float) in
the :abbr:`bsign ((base sign))`, :abbr:`bwhole ((base whole))`,
:abbr:`bfraction ((base fraction))` :abbr:`esign ((exponent sign))` and
:abbr:`evalue ((exponent value))` capture groups:

**bsign** - *optional*

    A "+" or "-" the at the beginning of the string representing the
    sign of the base.

**bwhole** - *optional*

    Any digits before the decimal following the **bsign** group or the
    beginning of the string, ignoring any leading zeros.

**bfraction** - *optional*

    Any digits following the decimal and preceding the exponent
    indicator ("e" or "E"), ignoring any trailing zeros.

**esign** - *optional*

    A "+" or "-" directly following the exponent indicator ("e" or "E")
    representing the sign of the exponent.

**evalue** - *optional*

    Any digits following the exponent marker and the optional **esign**
    group, excluding any leading zeros.

Examples:
    >>> from conwech._regexlib import NUMERIC_STRING
    >>> NUMERIC_STRING.match("010").groupdict()
    {'bsign': None, 'bwhole': '10', 'bfraction': None, 'esign': None, 'evalue': None}
    >>> NUMERIC_STRING.match("-010.020").groupdict()
    {'bsign': '-', 'bwhole': '10', 'bfraction': '02', 'esign': None, 'evalue': None}
    >>> NUMERIC_STRING.match("+010e030").groupdict()
    {'bsign': '+', 'bwhole': '10', 'bfraction': None, 'esign': None, 'evalue': '30'}
    >>> NUMERIC_STRING.match(".020e-030").groupdict()
    {'bsign': None, 'bwhole': None, 'bfraction': '02', 'esign': '-', 'evalue': '30'}
    >>> NUMERIC_STRING.match("010.020e+030").groupdict()
    {'bsign': None, 'bwhole': '10', 'bfraction': '02', 'esign': '+', 'evalue': '30'}

"""


NUMERAL_STRING = re.compile(
    r"^(?!\s*$)(?# assert string not empty or only whitespace)"
    r"\s*(?# match but do not capture leading whitespace)"
    r"(?:(?P<sign>negative|positive)\s)?(?# capture sign)"
    r"(?P<whole>.+\w)?(?# capture whole number text)"
    r"(?<!th)(?<!ths)(?# whole portion cannot end in th/ths)"
    r"(?(whole)(?# if any whole portion is captured...)"
    r"(?=\s+and\s+(?# ... anticipate ' and ' separator ...)"
    r"|\s*$)(?# ... or end of string...)|(?# ...otherwise nothing))"
    r"(?:\s+and\s+)?(?# match ' and ' if possible without capturing)"
    r"(?:(?P<numerator>.+\w)(?# capture fraction numerator text)"
    r"\s+(?# whitespace must separate numerator and denominator)"
    r"(?P<denominator>(?# capture fraction denominator text)"
    r"(?:\bhundred-|\bten-)?(?# denominator period value)"
    r"\w+)ths?)?(?# to capture fraction, must end in th/ths)"
    r"\s*$(?# match but do not capture trailing whitespace)")
"""
Pattern for matching strings of number text.

This compiled regular expression captures the lexical elements
corresponding to the components of the number that the text represents
according to an expected format in the whole, numerator, and denominator
capture groups:

**whole** - *optional*

    Any text following the start of the string and preceding the end of
    the string or the "and" that separates the **whole** from the
    **numerator**. The **whole** cannot match the end of the string if
    it would match a literal "th" or "ths" which indicates there must be
    a **numerator** and **denominator** in the string.

**numerator** - *co-optional*

    Any text following either the word "and" or the start of the string
    (in the absence of a matched **whole**) and preceding the
    **denominator** match, separated by whitespace.

**denominator** - *co-optional*

    Any text that starts with one of "one hundred"/"ten"/"one" following
    the **numerator** match and (necessarily) ending in "th" or "ths"
    followed by the end of the string.

The **numerator** & **denominator** must both match as part of a
non-capturing group representing all of the fraction text or neither
will match and the **whole** will consume the entire string. While,
technically, all groups are optional (lazy) the expression is not
allowed to match an empty or whitespace-only string.

Examples:
    >>> from conwech._regexlib import NUMERAL_STRING
    >>> NUMERAL_STRING.match("three hundred twenty-one").groupdict()
    {'whole': 'three hundred twenty-one', 'numerator': None, 'denominator': None}
    >>> NUMERAL_STRING.match("thirty-two and one tenth").groupdict()
    {'whole': 'thirty-two', 'numerator': 'one', 'denominator': 'ten'}
    >>> NUMERAL_STRING.match("three and twenty-one one hundredths").groupdict()
    {'whole': 'three', 'numerator': 'twenty-one', 'denominator': 'one hundred'}
    >>> NUMERAL_STRING.match("three hundred twenty-one one thousandths").groupdict()
    {'whole': None, 'numerator': 'three hundred twenty-one', 'denominator': 'one thousand'}

"""


PERIOD_STRING = re.compile(
    r"(?:^|\s+)(?# period must follow whitespace or start of string)"
    r"\b(?P<value>.+?)(?# capture period value and leave the name)"
    r"(?:\s+(?# whitespace must separate period value and name)"
    r"(?P<name>\w+illion\b|thousand\b)(?# capture the period name)"
    r"|\s*$)(?# second option allows period value to end a match)")
"""
Pattern for matching individual period substrings in number text.

This compiled regular expression captures the lexical elements
corresponding to the components of a period in a string of number text
in the value and name capture groups:

**value** - *required*

    All characters following either the start of the string or a
    previously matched period name and preceding either the end of the
    string or another period name.

**name** - *optional*

    A single word following a period value that is either "thousand" or
    ends with the "illion" suffix.

Examples:
    >>> from conwech._regexlib import PERIOD_STRING
    >>> PERIOD_STRING.findall("one million two hundred thirty-four thousand five hundred sixty-seven")
    [('one', 'million'), ('two hundred thirty-four', 'thousand'), ('five hundred sixty-seven', '')]
    >>> next(PERIOD_STRING.finditer("nine unnonagintaducentillion five tresquadragintacentillion")).groupdict()
    {'value': 'nine', 'name': 'unnonagintaducentillion'}

"""

# prefix combination exception patterns
PREFIX_EXCEPTION_X = re.compile(
    r"(?<=^se)(?# exception must start with 'se'...)"
    r"(?=[co])(?# ...and be followed by 'c' or 'o')")
"""
Pattern for matching invalid combinations of period name prefix
components resulting from zillion periods: 86, 106, 806. The expression
will match the position in the string where "x" needs to be inserted to
correct the exception.

Examples:
    >>> from conwech._regexlib import PREFIX_EXCEPTION_X
    >>> PREFIX_EXCEPTION_X.sub('x', 'seoctogintillion')
    'sexoctogintillion'
    >>> PREFIX_EXCEPTION_X.sub('x', 'secentillion')
    'sexcentillion'

"""


PREFIX_EXCEPTION_S = re.compile(
 r"(?<=^se)(?# exception must start with 'se'...)"
 r"(?=[qtv])(?# ...and be followed by 'q', 't', or 'v')"
 r"|(?# or)(?<=^tre)(?# exception must start with 'tre'...)"
 r"(?=[coqtv])(?# ...and be followed by 'c', 'o', 'q', 't', or 'v')")
"""
Pattern for matching invalid combinations of period name prefix
components resulting from zillion periods: 23, 26, 33, 36, 43, 46, 54,
56, 83, 103, 303, 306, 403, 406, 503, 506, 803. The expression will
match the position in the string where "s" needs to be inserted to
correct the exception.

Examples:
    >>> from conwech._regexlib import PREFIX_EXCEPTION_S
    >>> PREFIX_EXCEPTION_S.sub('s', 'trevignitillion')
    'tresvignitillion'
    >>> PREFIX_EXCEPTION_S.sub('s', 'sevignitillion')
    'sesvignitillion'

"""


PREFIX_EXCEPTION_M = re.compile(
    r"(?<=^septe)(?# exception must start with 'septe'...)"
    r"(?=[ov])(?# ...and be followed by 'o' or 'v')"
    r"|(?# or)(?<=^nove)(?# exception must start with 'nove'...)"
    r"(?=[ov])(?# ...and be followed by 'o' or 'v')")
"""
Pattern for matching invalid combinations of period name prefix
components resulting from zillion periods: 27, 29, 87, 89, 807, 809.
The expression will match the position in the string where "m" needs to
be inserted to correct the exception.

Examples:
    >>> from conwech._regexlib import PREFIX_EXCEPTION_M
    >>> PREFIX_EXCEPTION_M.sub('m', 'septevignitillion')
    'septemvignitillion'
    >>> PREFIX_EXCEPTION_M.sub('m', 'novevignitillion')
    'novemvignitillion'

"""


PREFIX_EXCEPTION_N = re.compile(
    r"(?<=^septe)(?# exception must start with 'septe'...)"
    r"(?=[cdqst])(?# ...and be followed by 'c', 'd', 'q', 's', or 't')"
    r"|(?# or )(?<=^nove)(?# exception must start with 'nove'...)"
    r"(?=[cdqst])(?# ...and be followed by 'c', 'd', 'q', 's', or 't')")
"""
Pattern for matching invalid combinations of period name prefix
components resulting from zillion periods: 17, 19, 37, 39, 47, 49, 57,
59, 67, 69, 77, 79, 107, 109, 207, 209, 307, 309, 407, 409, 507, 509,
607, 609, 707, 709. The expression will match the position in the string
where "n" needs to be inserted to correct the exception.

Examples:
    >>> from conwech._regexlib import PREFIX_EXCEPTION_N
    >>> PREFIX_EXCEPTION_N.sub('n', 'septedecillion')
    'septendecillion'
    >>> PREFIX_EXCEPTION_N.sub('n', 'novedecillion')
    'novendecillion'

"""
