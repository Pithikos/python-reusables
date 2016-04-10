# This uses real recursion so use carefully: don't use if the iteration
# depth is going to be big


# Simple
def apply_recursively(fn, obj):
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


# With predicate
def apply_recursively(fn, obj, predicate=lambda x: True):
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


# Apply to leaves of a mixed structure (dict + list)
def apply_leaves(struct, fn=lambda x: x, predicate=lambda x: True):
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



############################## Examples ################################

print(apply_recursively(str, [[1, {'a' : 2}], 3]))  # => [['1', "{'a': '2'}"], '3']
print(apply_recursively(int, [['1', {'a' : '2'}], '3'], str.isdigit)) # => [[1, {'a': 2}], 3]

print(apply_leaves([{'a' : 1, 'b' : 4}, [2, 3]], lambda x: 'TEST', lambda x: x>2))
# => [{'a': 1, 'b': 'TEST'}, [2, 'TEST']]
