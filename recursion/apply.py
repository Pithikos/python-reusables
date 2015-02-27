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



############################## Examples ################################

apply_recursively(str, [[1, 2], 3])                      # => [['1', '2'], '3']
apply_recursively(int, [['1', 'a'], '2'], str.isdigit)   # => [[1, 'a'], 2]
