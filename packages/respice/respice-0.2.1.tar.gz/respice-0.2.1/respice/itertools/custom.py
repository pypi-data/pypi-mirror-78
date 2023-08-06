from . import flatten, take


def compact(list_of_lists):
    """
    Compacts a list of lists.

    This is the same as flattening but also returns the compactification scheme, i.e. a list of lengths of the original
    sub-lists that were flattened. This is intended to be used with `uncompact`.
    """
    compacted = list(flatten(list_of_lists))
    compactification = list(map(len, list_of_lists))

    return compacted, compactification


def uncompact(compacted, compactification):
    """
    Reverses the compactification from `compact`.
    """
    fli = iter(compacted)
    return list(list(take(c, fli)) for c in compactification)
