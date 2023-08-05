# Based on  https://stackoverflow.com/questions/6358481/using-functools-lru-cache-with-dictionary-arguments/53394430#53394430

import functools
from .core import freeze

__all__ = [
    'freezeargs'
]

def freezeargs(func):
    '''
    Transform mutable arguments into immutable.
    Useful to be compatible with lru_cache
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple(freeze(arg) for arg in args)
        kwargs = {k: freeze(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)
    return wrapped
