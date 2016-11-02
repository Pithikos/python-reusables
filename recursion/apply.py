def _apply_recursively_(obj, val_apply=None,     val_predicate=None,
                             dictkey_apply=None, key_predicate=None, dictval_apply=None):
    """
    Traverse a dict/list mixed structure recursively applying transformations
    to keys and/or values that meet corresponding predicates.

    This will be applied to any elements of dictionaries and lists recursively
    in-place. The traversal is done depth first in order to search the whole
    structure deeply. No optimizations are being made so this should be used
    carefully.

    Takes:
        obj(iterable):            The structure that will be parsed
        val_apply(function):      Function that will be applied on values
        val_predicate(function):  Predicate that needs matching against a value
                                  for a value or key to be applied
        dictkey_apply(function):      Function that will be applied on keys
        key_predicate(function):  Predicate that needs matching against a key
                                  in order for a value or key to be applied
        dictval_apply(function):       Function applied to key-value pairs in a dict

    Return:
        Updated object
    """
    apply = _apply_recursively_
    val_predicate = val_predicate or (lambda v: True)
    val_apply     = val_apply     or (lambda v: v)
    dictkey_apply = dictkey_apply or (lambda k, v: k)
    if type(obj) is list:
        if len(obj)>1:
            return [apply(obj[0], val_apply, val_predicate, dictkey_apply, key_predicate, dictval_apply)] +\
                    apply(obj[1:], val_apply, val_predicate, dictkey_apply, key_predicate, dictval_apply)
        else:
            return [apply(obj[0], val_apply, val_predicate, dictkey_apply, key_predicate, dictval_apply)]
    elif type(obj) is dict:
        for k,v in obj.items():
            if type(v) is dict or type(v) is list:
                obj[k] = apply(v, val_apply, val_predicate, dictkey_apply, key_predicate, dictval_apply)
            if not key_predicate or key_predicate(k):
                del obj[k]
                k = dictkey_apply(k, v)
                if val_predicate(v):
                    obj[k] = val_apply(v)
                else:
                    obj[k] = v
                if dictval_apply:
                    obj[k] = dictval_apply(k, v)
        return obj
    elif not key_predicate and val_predicate(obj):
        return val_apply(obj)
    else:
        return obj


def apply_on_keys(iterable, apply, key=None, value=None):
    """Apply recursively on keys of an arbitrary structure

    Takes:
        iterable: structure to apply in-place
        apply: function to run on matching keys
        value: function to select based on value
        key: function to select based on key
    """
    def dictkey_apply(k,v):
        return apply(k)
    return _apply_recursively_(iterable, dictkey_apply=dictkey_apply,
                                                          key_predicate=key,
                                                          val_predicate=value)


def apply_on_values(iterable, apply, key=None, value=None):
    """Apply recursively on values of an arbitrary structure

    Takes:
        iterable: structure to apply in-place
        apply: function to run on matching values
        value: function to select based on value
        key: function to select based on key
    """
    return _apply_recursively_(iterable, val_apply=apply, key_predicate=key,
                                                          val_predicate=value)


def transform_keys(iterable, apply, value=None, key=None):
    """Apply recursively on the keys of dicts of an arbitrary structure

    This is similar to other apply functions with the main difference
    that it works only on dict structures and key-value pairs are used.

    Takes:
        iterable: structure to apply in-place
        apply: function to run on matching keys
        value: function for selecting based on value
        key: function for selecting based on key
    """
    return _apply_recursively_(iterable, dictkey_apply=apply, key_predicate=key,
                                                              val_predicate=value)


def transform_values(iterable, apply, value=None, key=None):
    """Apply recursively on the values of dicts of an arbitrary structure

    This is similar to other apply functions with the main difference
    that it works only on dict structures and key-value pairs are used.

    Takes:
        iterable: structure to apply in-place
        apply: function to run on matching keys
        value: function for selecting based on value
        key: function for selecting based on key
    """
    return _apply_recursively_(iterable, dictval_apply=apply, key_predicate=key,
                                                              val_predicate=value)



def apply_leaves(struct, fn=lambda x: x, predicate=lambda x: True):
    """
    Apply to leaves of a mixed dict-list structure
    """
    if type(struct) is list:
        if len(struct) > 1:
            return [apply_leaves(struct[0], fn, predicate)] + apply_leaves(struct[1:], fn, predicate)
        else:
            return [apply_leaves(struct[0], fn, predicate)]
    elif type(struct) is dict:
        for k,v in struct.iteritems():
            struct[k] = apply_leaves(v, fn, predicate)
    else:
        if predicate(struct):
            return fn(struct)
        else:
            return struct
    return struct


def apply_leaves_by_key(struct, key_select=lambda k: k, apply=lambda v: v):
    """
    Apple to leaves only if they belong to a specific key
    ie. apply_leaves_by_key({'a' : 34, 'b' :  55 }, lambda k: k=='b', str)
                           => {'a' : 34, 'b' : '55'}
    """
    if type(struct) is list:
        if len(struct) > 1:
            return [apply_leaves_by_key(struct[0], key_select, apply)] + \
                    apply_leaves_by_key(struct[1:], key_select, apply)
        else:
            return [apply_leaves_by_key(struct[0], key_select, apply)]
    elif type(struct) is dict:
        for k,v in struct.items():
            if type(v) is not dict and type(v) is not list:
                if key_select(k):
                    struct[k] = apply(v)
            else:
                struct[k] = apply_leaves_by_key(v, key_select, apply)
    return struct



# --------------------------------- Tests --------------------------------------
from copy import deepcopy as clone

# Apply
assert _apply_recursively_([1], str) == ['1']

assert _apply_recursively_([[1, {'a' : 2}], 3], str) == [['1', {'a': '2'}], '3']

assert _apply_recursively_([['1', {'a' : '2'}], '3'], int, str.isdigit) == [[1, {'a': 2}], 3]
assert _apply_recursively_([['1', {'a' : '2'}], '3'], int, key_predicate=lambda k: k=='a') == [['1', {'a': 2}], '3']

assert _apply_recursively_([[1, {'a' : 2}], 3],
             dictkey_apply=lambda k,v: 'test') == [[1, {'test' : 2}], 3]
assert _apply_recursively_({'a' : 1, 'b' : 2},
             dictkey_apply=lambda k,v: k+'test',
             key_predicate=lambda k: k=='b') == {'a': 1, 'btest': 2}
assert _apply_recursively_({'a' : 1, 'b' : 2},
             dictkey_apply=lambda k,v: k+'test',
             key_predicate=lambda k: k=='a') == {'atest': 1, 'b': 2}
assert _apply_recursively_([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 8}, [2, 3]]
assert _apply_recursively_([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v<5,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 8}, [2, 3]]
assert _apply_recursively_([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v>5,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 4}, [2, 3]]
assert _apply_recursively_([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v>5,
             key_predicate=lambda k: k=='a') == [{'a' : 1, 'b' : 4}, [2, 3]]

# Apply functions
assert apply_on_values({'a' : 1, 'b' : 4}, str, key=lambda k:k=='b') == {'a' : 1, 'b' : '4'}
assert apply_on_keys({'a' : 1, 'b' : 4}, lambda k: k+k, key=lambda k:k=='b') == {'a' : 1, 'bb' : 4}


nested = {
    "h1" : {
        "h2"  : 'test1',
        "h22" : 'test2',
        "h3"  : {
            "h4" : 'test3'
        }
    }
}
assert apply_on_values(clone(nested), apply=lambda v: 'DONE', key=lambda k: k=='h3')\
                   == {'h1': {'h2': 'test1', 'h3': 'DONE', 'h22': 'test2'}}
assert transform_values(clone(nested), apply=lambda k,v: k+v['h4'], key=lambda k: k=='h3')\
                   == {'h1': {'h2': 'test1', 'h3': 'h3test3', 'h22': 'test2'}}
