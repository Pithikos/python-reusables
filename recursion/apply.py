# This uses real recursion so use carefully: don't use if the iteration
# depth is going to be big


def apply_recursively(fn, obj):
    """
    Apply recursively to each node of a mixed dict-list structure
    """
    if not obj:
        return obj
    if type(obj) is list:
        if len(obj)>1:
            return [apply_recursively(fn, obj[0])] + apply_recursively(fn, obj[1:])
        else:
            return [apply_recursively(fn, obj[0])]
    if type(obj) is dict:
        for k in obj:
            obj[k] = apply_recursively(fn, obj[k])
    return fn(obj)


def apply_recursively(fn, obj, predicate=lambda x: True):
    """
    Apply recursively to each node of a mixed dict-list structure
    if predicate evaluates to true
    """
    if not obj:
        return obj
    if type(obj) is list:
        if len(obj)>1:
            return [apply_recursively(fn, obj[0], predicate)] +\
                    apply_recursively(fn, obj[1:], predicate)
        else:
            return [apply_recursively(fn, obj[0], predicate)]
    if type(obj) is dict:
        for k in obj:
            obj[k] = apply_recursively(fn, obj[k], predicate)
            #return obj[k]
    if type(obj) is not dict and predicate(obj):
        return fn(obj)
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


def apply_leaves_by_key(struct, select=lambda k: k, apply=lambda v: v):
    """
    Apple to leaves only if they belong to a specific key
    ie. apply_leaves_by_key({'a' : 34, 'b' :  55 }, lambda k: k=='b', str)
                           => {'a' : 34, 'b' : '55'}
    """
    if type(struct) is list:
        if len(struct) > 1:
            return [apply_leaves_by_key(struct[0], select, apply)] + apply_leaves_by_key(struct[1:], select, apply)
        else:
            return [apply_leaves_by_key(struct[0], select, apply)]
    elif type(struct) is dict:
        for k,v in struct.items():
            if type(v) is not dict and type(v) is not list:
                if select(k):
                    struct[k] = apply(v)
            else:
                struct[k] = apply_leaves_by_key(v, select, apply)
    return struct



############################## Examples ################################

print(apply_recursively(str, [[1, {'a' : 2}], 3]))  # => [['1', "{'a': '2'}"], '3']
print(apply_recursively(int, [['1', {'a' : '2'}], '3'], str.isdigit)) # => [[1, {'a': 2}], 3]

print(apply_leaves([{'a' : 1, 'b' : 4}, [2, 3]], lambda x: 'TEST', lambda x: x>2))
# => [{'a': 1, 'b': 'TEST'}, [2, 'TEST']]
