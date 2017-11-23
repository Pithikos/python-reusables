def investigate(obj, path='', accumulator=None):
    """
    Get information for an arbitrary structure.

    This can be expensive so don't use it in too big structures.

    Example:
        results = investigate({'names': ['John', 'Tom']})
        print('\n'.join(results))
        ['names'] list
        ['names'][0] John
        ['names'][1] Tom

    Takes:
        obj(iterable):            The structure that will be parsed

    Return:
        String with all information
    """
    if not accumulator:
        accumulator = []

    if type(obj) is list:
        line = '%s list' % path
        accumulator.append(line)
        for i,v in enumerate(obj):
            accumulator.extend(investigate(v, "%s[%d]" % (path, i), accumulator))
    elif type(obj) is dict:
        line = '%s dict' % path
        accumulator.append(line)
        for k,v in obj.items():
            accumulator.extend(investigate(v, path+"['%s']" % k))

    else:  # assume it's primate
        line = '%s %s' % (path, obj)
        return [line]

    uniq_list = list(set(accumulator))
    uniq_list.sort()
    return uniq_list


# --------------------------------- Tests --------------------------------------


# List
results = investigate({'names': ['John', 'Tom']})
assert('\n'.join(results)) == """ dict
['names'] list
['names'][0] John
['names'][1] Tom"""

# Dict
results = investigate({'person': [{'name': 'Fanny'}, {'name': 'Panny'}]})
assert('\n'.join(results)) in """ dict
['person'] list
['person'][0] dict
['person'][0]['name'] Fanny
['person'][1] dict
['person'][1]['name'] Panny"""

assert investigate([[1, {'a' : 2}], 3]) == [
    " list",
    "[0] list",
    "[0][0] 1",
    "[0][1] dict",
    "[0][1]['a'] 2",
    "[1] 3",
]
