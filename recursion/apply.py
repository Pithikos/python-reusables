def apply(obj, val_apply=None, val_predicate=None, key_apply=None, key_predicate=None):
    """
    Apply recursively to keys and/or values that meet corresponding predicates.

    This will be applied to any elements of dictionaries and lists recursively.
    Notice that this has not been optimized in any way and should thus be used
    responsibly.

    Takes:
        obj(iterable):           the structure that will be parsed
        val_apply(function):     function that will be applied on values
        val_predicate(function): predicate that needs matching against a value
                                 for a value or key to be applied
        key_apply(function):     function that will be applied on keys
        key_predicate(function): predicate that needs matching against a key
                                 in order for a value or key to be applied

    Return:
        Updated object
    """
    val_predicate = val_predicate or (lambda v: True)
    val_apply     = val_apply     or (lambda v: v)
    key_apply     = key_apply     or (lambda k: k)
    if type(obj) is list:
        if len(obj)>1:
            return [apply(obj[0], val_apply, val_predicate, key_apply, key_predicate)] +\
                    apply(obj[1:], val_apply, val_predicate, key_apply, key_predicate)
        else:
            return [apply(obj[0], val_apply, val_predicate, key_apply, key_predicate)]
    elif type(obj) is dict:
        for k,v in obj.items():
            if not key_predicate or key_predicate(k):
                del obj[k]
                k = key_apply(k)
                if type(v) is dict or type(v) is list:
                    obj[k] = apply(v, val_apply, val_predicate, key_apply, key_predicate)
                elif val_predicate(v):
                    obj[k] = val_apply(v)
                else:
                    obj[k] = v
        return obj
    elif not key_predicate and val_predicate(obj):
        return val_apply(obj)
    else:
        return obj


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

assert apply([1], str) == ['1']
assert apply([[1, {'a' : 2}], 3], str) == [['1', {'a': '2'}], '3']
assert apply([['1', {'a' : '2'}], '3'], int, str.isdigit) == [[1, {'a': 2}], 3]
assert apply([['1', {'a' : '2'}], '3'], int, key_predicate=lambda k: k=='a') == [['1', {'a': 2}], '3']

assert apply([[1, {'a' : 2}], 3],
             key_apply=lambda k: 'test') == [[1, {'test' : 2}], 3]
assert apply({'a' : 1, 'b' : 2},
             key_apply=lambda k: k+'test',
             key_predicate=lambda k: k=='b') == {'a': 1, 'btest': 2}
assert apply({'a' : 1, 'b' : 2},
             key_apply=lambda k: k+'test',
             key_predicate=lambda k: k=='a') == {'atest': 1, 'b': 2}
assert apply([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 8}, [2, 3]]
assert apply([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v<5,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 8}, [2, 3]]
assert apply([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v>5,
             key_predicate=lambda k: k=='b') == [{'a' : 1, 'b' : 4}, [2, 3]]
assert apply([{'a' : 1, 'b' : 4}, [2, 3]],
             val_apply=lambda v: v*2,
             val_predicate=lambda v: v>5,
             key_predicate=lambda k: k=='a') == [{'a' : 1, 'b' : 4}, [2, 3]]
