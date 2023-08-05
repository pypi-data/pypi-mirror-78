# object-freezer
Python module for freezing objects.

## Installation

```
$ pip install object-freezer
```

Then import this module as:

```python
import object_freezer as of
```

## Examples
A list is frozen into a tuple:

```python
>>> l = [1, 2, 3]
>>> hash(l)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> fl = of.freeze(l)
>>> hash(fl)
2528502973977326415
>>> fl
(1, 2, 3)
```

A dictionary is frozen into a `deepfrozendict` instance:

```python
>>> import object_freezer as of
>>> d = {'a': 'A', 'b': 'B'}
>>> hash(d)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'
>>> fd = of.freeze(d)
>>> hash(fd)
3871628092596788623
>>> fd
<deepfrozendict {'a': 'A', 'b': 'B'}>
```

If an element of a list is not hashable, it will also be frozen:

```python
>>> l = [[1, 2], {3: 4}]
>>> hash(l)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> fl = of.freeze(l)
>>> hash(fl)
5879964472677921951
>>> fl
((1, 2), <deepfrozendict {3: 4}>)
```

If a value of a dictionary is not hashable, it will be frozen:

```python
>>> import object_freezer as of
>>> d = {'a': ['A', 0], 'b': {'B': 1}}
>>> hash(d)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'
>>> fd = of.freeze(d)
>>> hash(fd)
6230706721132225338
>>> fd
<deepfrozendict {'a': ('A', 0), 'b': <deepfrozendict {'B': 1}>}>
```

## Known issues & notes

### A `dict` with one `(key, value)` pair has the same hash value as a `tuple (key, value)`

Since a list is frozen into a tuple, it is obvious that `of.freeze([key, value])` and `of.freeze((key, value))` are the same and thus have the same hash value. However, `of.freeze({key: value})` also always has the same hash value.

```python
>>> d = {1: 2}
>>> t = (1, 2)
>>> fd = of.freeze(d)
>>> ft = of.freeze(t)
>>> hash(fd) == hash(ft)
True
```

It is not a major issue since `fd == ft` returns `False`. Therefore, for example, you can use `fd` and `ft` as a distinct dictionary keys.

```python
>>> fd == ft
False
>>> {fd: 0, ft: 1}
{<deepfrozendict {1: 2}>: 0, (1, 2): 1}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## TO-DO's

- [ ] Test against various Python versions.
