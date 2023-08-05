"""Some Utility functions, that make yur life easier but don't fit in any
better catorgory than util."""

import numpy as np
import os
import pickle
from typing import *
import importlib


def walk(
    dict_or_list,
    fn,
    inplace=False,
    pass_key=False,
    prev_key="",
    splitval="/",
    walk_np_arrays=False,
):  # noqa
    """
    Walk a nested list and/or dict recursively and call fn on all non
    list or dict objects.

    Example
    -------

    .. code-block:: python

        dol = {'a': [1, 2], 'b': {'c': 3, 'd': 4}}

        def fn(val):
            return val**2

        result = walk(dol, fn)
        print(result)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}
        print(dol)  # {'a': [1, 2], 'b': {'c': 3, 'd': 4}}

        result = walk(dol, fn, inplace=True)
        print(result)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}
        print(dol)  # {'a': [1, 4], 'b': {'c': 9, 'd': 16}}

    Parameters
    ----------
    dict_or_list : dict or list
        Possibly nested list or dictionary.
    fn : Callable
        Applied to each leave of the nested list_dict-object.
    inplace : bool
        If False, a new object with the same structure
        and the results of fn at the leaves is created. If True the leaves
        are replaced by the results of fn.
    pass_key : bool
        Also passes the key or index of the leave element to
        ``fn``.
    prev_key : str
        If ``pass_key == True`` keys of parent nodes are passed
        to calls of ``walk`` on child nodes to accumulate the keys.
    splitval : str
        String used to join keys if :attr:`pass_key` is ``True``.
    walk_np_arrays : bool
        If ``True``, numpy arrays are intepreted as list, ie not as leaves.

    Returns
    -------
    The resulting nested list-dict-object with the results of
    fn at its leaves. : dict or list
    """

    instance_test = (list, dict)
    list_test = (list,)

    if walk_np_arrays:
        instance_test += (np.ndarray,)
        list_test += (np.ndarray,)

    if not pass_key:

        def call(value):
            if isinstance(value, instance_test):
                return walk(value, fn, inplace, walk_np_arrays=walk_np_arrays)
            else:
                return fn(value)

    else:

        def call(key, value):
            if prev_key != "":
                key = splitval.join([prev_key, key])

            if isinstance(value, instance_test):
                return walk(
                    value,
                    fn,
                    inplace,
                    pass_key=True,
                    prev_key=key,
                    splitval=splitval,
                    walk_np_arrays=walk_np_arrays,
                )
            else:
                return fn(key, value)

    if isinstance(dict_or_list, list_test):
        results = []
        for i, val in strenumerate(dict_or_list):
            result = call(i, val) if pass_key else call(val)
            results += [result]
            if inplace:
                dict_or_list[int(i)] = result
    elif isinstance(dict_or_list, dict):
        results = {}
        for key, val in dict_or_list.items():
            result = call(key, val) if pass_key else call(val)
            results[key] = result
            if inplace:
                dict_or_list[key] = result
    else:
        if not inplace:
            if not pass_key:
                results = fn(dict_or_list)
            else:
                results = fn(prev_key, dict_or_list)
        else:
            if not pass_key:
                dict_or_list = fn(dict_or_list)
            else:
                dict_or_list = fn(prev_key, dict_or_list)

    if inplace:
        results = dict_or_list

    return results


class KeyNotFoundError(Exception):
    def __init__(self, cause, keys=None, visited=None):
        self.cause = cause
        self.keys = keys
        self.visited = visited
        messages = list()
        if keys is not None:
            messages.append("Key not found: {}".format(keys))
        if visited is not None:
            messages.append("Visited: {}".format(visited))
        messages.append("Cause:\n{}".format(cause))
        message = "\n".join(messages)
        super().__init__(message)


def retrieve(
    list_or_dict, key, splitval="/", default=None, expand=True, pass_success=False
):
    """Given a nested list or dict return the desired value at key expanding
    callable nodes if necessary and :attr:`expand` is ``True``. The expansion
    is done in-place.

    Parameters
    ----------
        list_or_dict : list or dict
            Possibly nested list or dictionary.
        key : str
            key/to/value, path like string describing all keys necessary to
            consider to get to the desired value. List indices can also be
            passed here.
        splitval : str
            String that defines the delimiter between keys of the
            different depth levels in `key`.
        default : obj
            Value returned if :attr:`key` is not found.
        expand : bool
            Whether to expand callable nodes on the path or not.

    Returns
    -------
        The desired value or if :attr:`default` is not ``None`` and the
        :attr:`key` is not found returns ``default``.

    Raises
    ------
        Exception if ``key`` not in ``list_or_dict`` and :attr:`default` is
        ``None``.
    """

    keys = key.split(splitval)

    success = True
    try:
        visited = []
        parent = None
        last_key = None
        for key in keys:
            if callable(list_or_dict):
                if not expand:
                    raise KeyNotFoundError(
                        ValueError(
                            "Trying to get past callable node with expand=False."
                        ),
                        keys=keys,
                        visited=visited,
                    )
                list_or_dict = list_or_dict()
                parent[last_key] = list_or_dict

            last_key = key
            parent = list_or_dict

            try:
                if isinstance(list_or_dict, dict):
                    list_or_dict = list_or_dict[key]
                else:
                    list_or_dict = list_or_dict[int(key)]
            except (KeyError, IndexError, ValueError) as e:
                raise KeyNotFoundError(e, keys=keys, visited=visited)

            visited += [key]
        # final expansion of retrieved value
        if expand and callable(list_or_dict):
            list_or_dict = list_or_dict()
            parent[last_key] = list_or_dict
    except KeyNotFoundError as e:
        if default is None:
            raise e
        else:
            list_or_dict = default
            success = False

    if not pass_success:
        return list_or_dict
    else:
        return list_or_dict, success


def pop_keypath(
    current_item: Union[callable, list, dict],
    key: str,
    splitval: str = "/",
    default: object = None,
    expand: bool = True,
    pass_success: bool = False,
):
    """Given a nested list or dict structure, pop the desired value at key expanding
    callable nodes if necessary and :attr:`expand` is ``True``. The expansion
    is done in-place.

    Parameters
    ----------
        current_item : list or dict
            Possibly nested list or dictionary.
        key : str
            key/to/value, path like string describing all keys necessary to
            consider to get to the desired value. List indices can also be
            passed here.
        splitval : str
            String that defines the delimiter between keys of the
            different depth levels in `key`.
        default : obj
            Value returned if :attr:`key` is not found.
        expand : bool
            Whether to expand callable nodes on the path or not.

    Returns
    -------
        The desired value or if :attr:`default` is not ``None`` and the
        :attr:`key` is not found returns ``default``.

    Raises
    ------
        Exception if ``key`` not in ``list_or_dict`` and :attr:`default` is
        ``None``.
    """

    keys = key.split(splitval)

    success = True
    visited = []
    parent = None
    last_key = None
    try:
        for key in keys:
            if callable(current_item):
                if not expand:
                    raise KeyNotFoundError(
                        ValueError(
                            "Trying to get past callable node with expand=False."
                        ),
                        keys=keys,
                        visited=visited,
                    )
                else:
                    current_item = current_item()
                    parent[last_key] = current_item

            last_key = key
            parent = current_item

            try:
                if isinstance(current_item, dict):
                    current_item = current_item[key]
                else:
                    current_item = current_item[int(key)]
            except (KeyError, IndexError) as e:
                raise KeyNotFoundError(e, keys=keys, visited=visited)

            visited += [key]
        # final expansion of retrieved value
        if expand and callable(current_item):
            current_item = current_item()
            parent[last_key] = current_item

        if isinstance(parent, list):
            parent[int(last_key)] = None
        else:
            del parent[last_key]

    except KeyNotFoundError as e:
        if default is None:
            raise e
        else:
            current_item = default
            success = False
    if pass_success:
        return current_item, success
    else:
        return current_item


def set_default(list_or_dict, key, default, splitval="/"):
    """Combines :func:`retrieve` and :func:`set_value` to create the
    behaviour of pythons ``dict.setdefault``: If ``key`` is found in
    ``list_or_dict``, return its value, otherwise return ``default`` and add it
    to ``list_or_dict`` at ``key``.

    Parameters
    ----------
        list_or_dict : list or dict
            Possibly nested list or dictionary.  splitval (str): String that
            defines the delimiter between keys of the different depth levels in
            `key`.
        key : str
            key/to/value, path like string describing all keys necessary to
            consider to get to the desired value. List indices can also be
            passed here.
        default : object
            Value to be returned if ``key`` not in list_or_dict and set to be
            at ``key`` in this case.
        splitval : str
            String that defines the delimiter between keys of the different
            depth levels in :attr:`key`.

    Returns
    -------
        The retrieved value or if the :attr:`key` is not found returns
        ``default``.
    """

    try:
        ret_val = retrieve(list_or_dict, key, splitval, None)
    except KeyNotFoundError as e:
        set_value(list_or_dict, key, default, splitval)
        ret_val = default

    return ret_val


def set_value(list_or_dict, key, val, splitval="/"):
    """Sets a value in a possibly nested list or dict object.

    Parameters
    ----------

    key : str
        ``key/to/value``, path like string describing all keys necessary to
        consider to get to the desired value. List indices can also be passed
        here.
    value : object
        Anything you want to put behind :attr:`key`
    list_or_dict : list or dict
        Possibly nested list or dictionary.
    splitval : str
        String that defines the delimiter between keys of the different depth
        levels in :attr:`key`.


    Examples
    --------

    .. code-block:: python

        dol = {"a": [1, 2], "b": {"c": {"d": 1}, "e": 2}}

        # Change existing entry
        set_value(dol, "a/0", 3)
        # {'a': [3, 2], 'b': {'c': {'d': 1}, 'e': 2}}}

        set_value(dol, "b/e", 3)
        # {"a": [3, 2], "b": {"c": {"d": 1}, "e": 3}}

        set_value(dol, "a/1/f", 3)
        # {"a": [3, {"f": 3}], "b": {"c": {"d": 1}, "e": 3}}

        # Append to list
        dol = {"a": [1, 2], "b": {"c": {"d": 1}, "e": 2}}

        set_value(dol, "a/2", 3)
        # {"a": [1, 2, 3], "b": {"c": {"d": 1}, "e": 2}}

        set_value(dol, "a/5", 6)
        # {"a": [1, 2, 3, None, None, 6], "b": {"c": {"d": 1}, "e": 2}}

        # Add key
        dol = {"a": [1, 2], "b": {"c": {"d": 1}, "e": 2}}
        set_value(dol, "f", 3)
        # {"a": [1, 2], "b": {"c": {"d": 1}, "e": 2}, "f": 3}

        set_value(dol, "b/1", 3)
        # {"a": [1, 2], "b": {"c": {"d": 1}, "e": 2, 1: 3}, "f": 3}

        # Raises Error:
        # Appending key to list
        # set_value(dol, 'a/g', 3)  # should raise

        # Fancy Overwriting
        dol = {"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2}

        set_value(dol, "e/f", 3)
        # {"a": [1, 2], "b": {"c": {"d": 1}}, "e": {"f": 3}}

        set_value(dol, "e/f/1/g", 3)
        # {"a": [1, 2], "b": {"c": {"d": 1}}, "e": {"f": [None, {"g": 3}]}}

        # Toplevel new key
        dol = {"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2}
        set_value(dol, "h", 4)
        # {"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2, "h": 4}

        set_value(dol, "i/j/k", 4)
        # {"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2, "h": 4, "i": {"j": {"k": 4}}}

        set_value(dol, "j/0/k", 4)
        # {"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2, "h": 4, "i": {"j": {"k": 4}}, "j": [{"k": 4}], }

        # Toplevel is list new key
        dol = [{"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2}, 2, 3]

        set_value(dol, "0/k", 4)
        # [{"a": [1, 2], "b": {"c": {"d": 1}}, "e": 2, "k": 4}, 2, 3]

        set_value(dol, "0", 1)
        # [1, 2, 3]

    """

    # Split into single keys and convert to int if possible
    keys = []
    for k in key.split(splitval):
        try:
            newkey = int(k)
        except:
            newkey = k
        keys.append(newkey)
    next_keys = keys[1:] + [None]

    is_leaf = [False for k in keys]
    is_leaf[-1] = True

    next_is_leaf = is_leaf[1:] + [None]

    parent = None
    last_key = None
    for key, leaf, next_key, next_leaf in zip(keys, is_leaf, next_keys, next_is_leaf):

        if isinstance(key, str):
            # list_or_dict must be a dict
            if isinstance(list_or_dict, list):
                # Not possible
                raise ValueError("Trying to add a key to a list")
            elif not isinstance(list_or_dict, dict) or key not in list_or_dict:
                # Replace value based on next key -> This is only met if
                list_or_dict[key] = {} if isinstance(next_key, str) else []

        else:
            # list_or_dict must be list
            if isinstance(list_or_dict, list):
                if key >= len(list_or_dict):
                    # Append to list and pad with None
                    n_add = key - len(list_or_dict) + 1
                    list_or_dict += [None] * n_add
            elif not isinstance(list_or_dict, dict):
                if parent is None:
                    # We are at top level
                    list_or_dict = [None] * (key + 1)
                else:
                    parent[last_key] = [None] * (key + 1)

        if leaf:
            list_or_dict[key] = val
        else:
            if not isinstance(list_or_dict[key], (dict, list)):
                # Replacement condition met
                list_or_dict[key] = (
                    {} if isinstance(next_key, str) else [None] * (next_key + 1)
                )

            parent = list_or_dict
            last_key = key
            list_or_dict = list_or_dict[key]


def contains_key(nested_thing, key, splitval="/", expand=True):
    """
    Tests if the path like key can find an object in the nested_thing.
    """
    try:
        retrieve(nested_thing, key, splitval=splitval, expand=expand)
        return True
    except Exception:
        return False


def update(to_update, to_update_with, splitval="/", mode="lax"):
    """
    Updates the entries in a nested object given another nested object.

    Parameters
    ----------
    to_update : dict or list
        The object that will be manipulated
    to_update_with : dict or list
        The object used to manipulate :attr:`to_update`.
    splitval : str
        Path element seperator.
    mode : str
        One of ``['lax', 'medium', 'strict']``. Determines how the update is
        executed:

        ``lax``
            Any given key in :attr:`to_update_with` will be created in
            :attr:`to_update`.
        ``medium``
            Any key in :attr:`to_update_with` that does not exist in
            :attr:`to_update` will simply be ignored.
        ``strict``
            The first key in :attr:`to_update_with` that does not exist in
            :attr:`to_update` will raise a :class:`KeyNotFoundError`.

    Raises
    ------
    KeyNotFoundError
        If a key in :attr:`to_update_with` cannot be found in
        :attr:`to_update`.
    """
    assert mode in ["lax", "medium", "strict"]

    def _update(key, value):
        if mode == "strict" and not contains_key(to_update, key):
            raise KeyNotFoundError(
                "Trying to update a nested object in strict "
                f"mode that does not contain the key `{key}`."
            )
        elif mode == "medium" and not contains_key(to_update, key):
            pass
        else:
            set_value(to_update, key, value, splitval=splitval)

    walk(to_update_with, _update, splitval=splitval, pass_key=True)


def get_leaf_names(nested_thing):
    class LeafGetter:
        def __call__(self, key, value):
            if not hasattr(self, "keys"):
                self.keys = []

            self.keys += [key]

    LG = LeafGetter()

    walk(nested_thing, LG, pass_key=True)

    return LG.keys


def strenumerate(iterable):
    """Works just as enumerate, but the returned index is a string.

    Parameters
    ----------
    iterable : Iterable
        An (guess what) iterable object.
    """

    for i, val in enumerate(iterable):
        yield str(i), val
