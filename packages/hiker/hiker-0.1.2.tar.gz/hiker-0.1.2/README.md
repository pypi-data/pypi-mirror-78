[![Documentation Status](https://readthedocs.org/projects/hiker/badge/?version=latest)](https://hiker.readthedocs.io/en/latest/?badge=latest)

![Logo](assets/walker.png)

# Hiker

Navigating nested python objects with ease.

This package ships a lot of functionality you might recognise from python's
`dict` or `list` methods, like getters and setters, the update function and the
likes, but for nested objects consiting of `dict`s and `list`s. You can specify
what part of you nested object you want by using a '/deep/path/syntax/' and can
update only branches of your objects without overwriting of deleting
unspecified paths.

The basis for all this is the `walk` function. It accepts your nested object
and calls a function on all leaf variables.

### Example

    dol = {'a': [1, 2], 'b': {'c': 3, 'd': 4}}

    def fn(val):
        return val**2

    result = walk(dol, fn)
    print(result)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}
    print(dol)  # {'a': [1, 2], 'b': {'c': 3, 'd': 4}}

    result = walk(dol, fn, inplace=True)
    print(result)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}
    print(dol)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}


Below you can find a table which compares `hiker`'s functionality with those of
python's `dict` and `list`.


| hiker | dict | list | Example |
| --- | --- | --- | --- |
| `walk` | - | - |  |
| `retrieve` | `dict[key]`, `dict.get()` | `list[index]` | `retrieve({'a': [1, 2]}, 'a/0]) => 1` |
| `pop_keypath` | `dict.pop()` | `list.pop` | | 
| `set_default` | `dict.setdefault()` | | | 
| `set_value` | `dict[key] = val`, | `list[index] = val` | | 
| `contains_key` | `key in dict` | `0 <= index < len(list)` | | 
| `update` | `dict.update()` | | |
| `get_lead_names` | `dict.keys()` | | |
