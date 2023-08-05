"""
Separate home for custom exceptions raised by ConWech functions.

What's that you ask? Why on earth would you subclass ValueError for so
many specific cases when you can just raise one from the function call?
What an insightful question! I'm so glad you asked...

    1)  The main reason is that when a function is designed to take
        input as a string that must conform to a particular format, it
        helps to have very informative exceptions to say not just, "Hey
        I want a string!" but also to whine about the format it needs
        that string to be in and having different types of exceptions
        for different violations of that format can help, especially if
        said format is both multifaceted and highly specific.

    2)  In order to be more explicit about what exactly went wrong,
        some of these exceptions warrant fairly long/detailed messages,
        especially if the user doesn't know what a zillion value is for
        instance. You're README is your code's first impression; the
        metaphorical handshake, if you will. The documentation (where we
        are now) is the causal conversation that ensues. Fortunately, we
        live in a perfect world and every single user always reads every
        word of the wonderful detailed documentation provided by every
        developer ever... No, but really the problem is, most of the
        time, you probably only shake someone's hand once (if ever). In
        that sense, Exceptions are anything from a developer's subtle
        clearing of the throat to the kindest god-smack to the user's
        face for passing up the aforementioned handshake.

    3)  The exception type is the very first thing a user sees. That
        being the case, the more experienced a developer gets, the more
        information they tend to glean directly from the name of the
        exception with little need to read further. In keeping with the
        "no such thing as too much information" theme, you might notice
        that most of these exceptions have very verbose names. This is
        by design. Now, let's shift paradigms.

    4)  Readability... Not necessarily the exceptions per se (although
        there's a good case there too), but the functions tasked with
        calling them. Usually, when raising exceptions, the programmer
        is left with an ultimatum. Do I lay everything out and explain
        why this exception is being raised, or do I keep it short and
        sweet by raising quite possibly the most condensed, cryptic
        exception possible? Clearly, this module leans into the former
        rather aggressively. However, it's been my experience, that
        developers often default to the later. There are many possible
        reasons for that, some of which might be reasonable in other
        contexts, but not this one (in my humblest of opinions). One
        might argue that it's helpful to have exception strings in
        plain view and tucking it away in a custom class might be
        obfuscating the code. To that, I would say if you're relying
        on raw strings to figure out how the code works, the code base
        probably has much larger readability issues (the irony that you
        just read that from a python docstring is not lost on me). See
        my second point (above). The function should tell you how it
        works, not how it doesn't. Leave that to the exception.

    5)  In a similar vein of thought, intelligent use of custom
        exceptions can help with QA. Simple exceptions look more like
        half-a$$ed built-in exceptions which could already be hit or
        miss, but as a developer, the more distinctive your exceptions
        are the easier it is to debug. If you go this route, then
        ideally, nothing in your codebase should never raise an
        exception that isn't yours, and you should know exactly how to
        force your code into raising the ones you've written; something
        that you can not only use to spot-check code as you write it,
        but that makes for some slick and easy unit testing.

    6)  I was bored...

Sorry, I'm off my soapbox now. You probably didn't need half of that
explanation and you might still disagree, but there it is anyway. Thank
you for coming to my TED talk.
"""


class InvalidNumericString(ValueError):
    """
    Custom exception for :func:`.number2text`.
    """

    def __init__(self, number, *args):
        """
        Args:
            number (str): Invalid number-like string input.
            *args: Additional ValueError positional arguments.
        """
        super(InvalidNumericString, self).__init__(
            '\n\n\tInput is not a valid number-like format!'
            '\n\tDid not understand "{}"'.format(number),
            *args
        )


class InvalidNumeralString(ValueError):
    """
    Custom exception for :func:`.text2number`.
    """

    def __init__(self, text, *args):
        """
        Args:
            text (str): Invalid number text.
            *args: Additional ValueError positional arguments.
        """
        super(InvalidNumeralString, self).__init__(
            '\n\n\t"{}" does not follow expected lexical pattern!'
            '\n\t"<whole_number> [and <decimal_numerator> <decimal_denominator>ths]"'
            '\n\tSee module documentation for more details.'.format(text),
            *args
        )


class InvalidPeriodValueText(ValueError):
    """
    Custom exception for :func:`.text2number`.
    """

    def __init__(self, value, period, *args):
        """
        Args:
            value (str): Invalid period value text.
            period (str): Name of the period.
            *args: Additional ValueError positional arguments.
        """
        super(InvalidPeriodValueText, self).__init__(
            '\n\n\tCould not determine value for the {}s!'
            '\n\tDid not understand "{}"'.format(period or 'unit', value),
            *args
        )


class InvalidPeriodNameText(ValueError):
    """
    Custom exception for :func:`.readperiod`.
    """

    def __init__(self, name, prefix, *args):
        """
        Args:
            name (str): Full invalid period name
            prefix (str): Invalid prefix in period name
            *args: Additional ValueError positional arguments.
        """
        super(InvalidPeriodNameText, self).__init__(
            '"{}" is not a valid Conway-Wechsler period name; '
            'specifically, prefix "{}" not found'.format(name, prefix),
            *args
        )
