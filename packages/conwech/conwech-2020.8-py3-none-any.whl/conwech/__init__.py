"""
The ConWech package is comprised of two primary submodules:
:mod:`.lexicon`, and :mod:`.functions`. All of the members in
:mod:`.functions` along with a few select members of :mod:`.lexicon`
are imported into the top level of the package for easy access.
Flat > nested, but organization = imperative.

.. currentmodule:: conwech

.. autosummary::
    :toctree: package

    functions
    lexicon

Two additional submodules :mod:`._exceptions` and :mod:`._regexlib` are
essentially repositories for... well, exactly what it sounds like. Both
submodules are considered pseudo-internal, but feel free to muck around
till your heart's content.

.. autosummary::
    :toctree: package

    _regexlib
    _exceptions

"""

# bring core elements to top of package
from conwech.lexicon import NATURAL_NUMBERS_LT_100
from conwech.lexicon import NATURAL_NUMBERS_LT_1000
from conwech.functions import nameperiod, readperiod
from conwech.functions import number2text, text2number
