import collections
try:
    import numpy as np
except ImportError:
    _numpy_is_imported = False
else:
    _numpy_is_imported = True

__all__ = [
    'NotFreezableError',
    'ishashable',
    'freeze',
    'unfreeze',
    'deepfrozendict'
]

class NotFreezableError(Exception):
    def __init__(self, msg):
        self.msg = msg

def ishashable(obj):
    '''Returns if obj is hashable without modifying it

    Parameters
    ----------
    obj : any
        Python object of any type

    Returns
    -------
    bool
        whether the object is hashable
    '''
    # NOTE: `return isinstance(obj, collections.Hashable)` does not work.
    # e.g. `isinstance((1, [1, 2]), collections.Hashable)` returns `True`,
    # but it is not hashable since it is a hashable type with a *unhashable* element.
    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True

def freeze(obj, custom_conversions=None):
    '''Convert a object to a hashable

    Parameters
    ----------
    obj : any
        Python object of any type
    custom_conversions : dict
        key is type, value is conversion function. Applied in key order.

    Returns
    -------
    hashable
        Hashable equivalent of the object

    Raises
    ------
    UnhashableError
        When the object cannot be converted to a hashable

    Supported conversion
    - set -> frozenset
    - list -> tuple
    - dict -> deepfrozendict
    '''
    # TODO: Prioritize custom_coversion
    # TODO: Add np.ndarray conversion to default
    if custom_conversions is not None:
        for otype, conv in custom_conversions.items():
            if isinstance(obj, otype):
                ret = conv(obj)
                break
    elif ishashable(obj):
        ret = obj
    elif isinstance(obj, set):
        # Elements in a set are guaranteed to be hashable.
        ret = frozenset(obj)
    elif isinstance(obj, dict):
        ret = deepfrozendict(obj, custom_conversions=custom_conversions)
    elif isinstance(obj, (list, tuple)) or (_numpy_is_imported and isinstance(obj, np.ndarray)):
        ret = tuple(freeze(e, custom_conversions=custom_conversions) for e in obj)
    else:
        raise NotFreezableError('Freezing method for object {} is not defined.'.format(repr(obj)))

    if not ishashable(ret):
        raise NotFreezableError('Object {} cannot be converted to a hashable.'.format(repr(ret)))

    return ret

def unfreeze(frozen_obj, original_obj_like, custom_conversions_inv=None):
    if ishashable(original_obj_like):
        ret = frozen_obj
    elif isinstance(original_obj_like, set):
        # Elements in a set are guaranteed to be hashable.
        # ret = frozenset(original_obj_like)
        ret = set(frozen_obj)
    elif isinstance(original_obj_like, dict):
        # ret = deepfrozendict(original_obj_like, custom_conversions_inv=custom_conversions_inv)
        ret = {k: unfreeze(v, original_obj_like[k], custom_conversions_inv=custom_conversions_inv) for k, v in frozen_obj.items()}
    elif isinstance(original_obj_like, (list, tuple)):
        # ret = tuple(freeze(e, custom_conversions_inv=custom_conversions_inv) for e in obj)
        ret = [unfreeze(e, e_like, custom_conversions_inv=custom_conversions_inv) for e, e_like in zip(frozen_obj, original_obj_like)]
        if isinstance(original_obj_like, tuple):
            ret = tuple(ret)
    elif custom_conversions_inv is not None:
        for otype, conv in custom_conversions_inv.items():
            if isinstance(original_obj_like, otype):
                ret = conv(frozen_obj)
                # ret = conv(obj)

                break
    else:
        raise UnhashableError('Object {} cannot be converted to a hashable.'.format(repr(original_obj_like)))

    # if not ishashable(ret):
    #     raise UnhashableError('Object {} cannot be converted to a hashable.'.format(repr(ret)))

    return ret



# Implementation of deepfrozendict is based on frozendict:
# https://github.com/slezica/python-frozendict

try:
    from collections import OrderedDict
except ImportError:  # python < 2.7
    OrderedDict = NotImplemented

iteritems = getattr(dict, 'iteritems', dict.items) # py2-3 compatibility

class deepfrozendict(collections.Mapping):
    """
    An immutable wrapper around dictionaries that implements the complete :py:class:`collections.Mapping`
    interface. It can be used as a drop-in replacement for dictionaries where immutability is desired.
    """

    dict_cls = dict

    def __init__(self, *args, **kwargs):
        if 'custom_conversions' in kwargs:
            self._custom_conversions = kwargs.pop('custom_conversions')
        else:
            self._custom_conversions = None
        _raw_dict = self.dict_cls(*args, **kwargs)

        # Hopefully this operation does not change hidden property of _raw_dict such as key order...
        self._dict = self.dict_cls({key: freeze(value, custom_conversions=self._custom_conversions) for key, value in _raw_dict.items()})

        self._hash = None

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        return hash(tuple((key, value) for key, value in self._dict.items()))


class FrozenOrderedDict(deepfrozendict):
    """
    A frozendict subclass that maintains key order
    """

    dict_cls = OrderedDict


if OrderedDict is NotImplemented:
    del FrozenOrderedDict
