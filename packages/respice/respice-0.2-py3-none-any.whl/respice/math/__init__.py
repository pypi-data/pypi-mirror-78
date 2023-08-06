from math import floor


def fraction(x):
    """
    Returns the positive fractional part of `x`.

    The fraction will always be positive, regardless `x` being negative or not.
    For negative numbers, this means that the positive fraction is counted from the next lower
    integer. E.g. while `fraction(0.7) = 0.7`, `fraction(-0.7) = 0.3` - counted from `-1`, the
    next lower integer, so that `-1 + 0.3 = -0.7` adds up to the original number `x`.
    """
    return x - floor(x)
