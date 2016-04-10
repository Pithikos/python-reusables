# This uses real recursion so use carefully: don't use if the iteration
# depth is going to be big


# Simple
def apply_recursively(fn, iterable):
    if not iterable:
        return iterable
    if not hasattr(iterable, '__iter__'):
        return fn(iterable)
    if len(iterable)>1:
        return [apply_recursively(fn, iterable[0])] + apply_recursively(fn, iterable[1:])
    else:
        return [apply_recursively(fn, iterable[0])]


# With predicate
def apply_recursively(fn, iterable, predicate=lambda x: True):
    if not iterable:
        return iterable
    if not hasattr(iterable, '__iter__'):
        if predicate(iterable):
           return fn(iterable)
        else:
            return iterable
    if len(iterable)>1:
        return [apply_recursively(fn, iterable[0], predicate)] +\
                apply_recursively(fn, iterable[1:], predicate)
    else:
        return [apply_recursively(fn, iterable[0], predicate)]


# Apply to leaves of a mixed structure (dict + list)
def apply_leaves(struct, fn=lambda x: x, predicate=lambda x: True):
    if type(struct) is list:
        if len(struct) > 1:
            return [traverse_struct(struct[0], fn, predicate)] + traverse_struct(struct[1:], fn, predicate)
        else:
            return [traverse_struct(struct[0], fn, predicate)]
    elif type(struct) is dict:
        for k,v in struct.iteritems():
            struct[k] = traverse_struct(v, fn, predicate)
    else:
        if predicate(struct):
            return fn(struct)
        else:
            return struct
    return struct


############################## Examples ################################

apply_recursively(str, [[1, 2], 3])                      # => [['1', '2'], '3']
apply_recursively(int, [['1', 'a'], '2'], str.isdigit)   # => [[1, 'a'], 2]

traverse_struct([{'a' : 1, 'b' : 4}, [2, 3]], lambda x: 'TEST', lambda x: x>2)
# => [{'a': 1, 'b': 'TEST'}, [2, 'TEST']]
