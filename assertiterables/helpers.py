from typing import Any, Tuple

def _len(x: Any, max_try: int) -> Tuple[bool,int]:
    """
    Brute-force attempt at getting length.

    **NB!** This method may iterate through any iterator or generator provided.
    I.e., this method has **side effects** that may require subsequent
    rewinding/resetting the iterator!

    :param x:
        An object that either has ``__len__`` method
        or supports iterations.

    :param max_try:
        When falling back to using iterations, the maximum number 
        of iterations before reporting back.

    :returns:
        Tuple with 2 values.
        1. Boolean, the resulting length is exact.
        2. The found length, either exact or estimated value.
    
    :raises TypeError:
        Raised if `x` is not an iterable.

    Example::
        >>> x = range(2500)
        >>> len(x)
        2500
        >>> _len(x, 2)
        (True, 2500)
        >>> y = (i for i in x)
        >>> len(y)
        Traceback (most recent call last):
            ...
        TypeError: object of type 'generator' has no len()
        >>> _len((i for i in x), 2)
        (False, 2)
    """
    try:
        length = len(x)
        return (True, length)
    except TypeError:
        length = 0
        has_length = True
        for _ in x:
            if length == max_try:
                has_length = False
                break
            length += 1
        return (has_length, length)
