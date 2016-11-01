def collect_values(obj, val_fn, only_values=False):
    """
    Collect values in an arbitrary structure. Values can be strings or numbers.

    Takes:
        obj(iterable): arbitrary structure to scan
        val_fn(function): function to use against values
        include_key(bool): Collect the key as well

    Return:
        A list of found items.
    """
    found = []
    if type(obj) is list:
        for item in obj:
            if type(item) is list or type(item) is dict:
                found += collect_values(item, val_fn, only_values)
            elif val_fn(item):
                if only_values:
                    found += [item]
                else:
                    found += [obj]
    elif type(obj) is dict:
        for k,v in obj.items():
            if type(v) is dict or type(v) is list:
                found += collect_values(v, val_fn, only_values)
            elif val_fn(v):
                if only_values:
                    found += [v]
                else:
                    found += [obj]
    else:
        if val_fn(obj):
            found += [obj]
    return found


def collect_by_key(obj, key_fn, only_values=True):
    """
    Collect values based on a key in an arbitrary structure.

    Takes:
        obj(iterable): arbitrary structure to scan
        key_fn(function): fuction touse against keys
        include_key(bool): Collect the key as well

    Return:
        A list of found items.
    """
    found = []
    if type(obj) is list:
        for item in obj:
            if type(item) is list or type(item) is dict:
                found += collect_by_key(item, key_fn, only_values)
    elif type(obj) is dict:
        for k,v in obj.items():
            if key_fn(k):
                if only_values:
                    if not v in found:
                        found += [v]
                else:
                    if not obj in found:
                        found += [obj]
            elif type(v) is dict or type(v) is list:
                found += collect_by_key(v, key_fn, only_values)
    return found



# --------------------------------- Tests --------------------------------------
struct = [
    42,
    { 'a' : 2, 'b' : [5, 2, 1], 'c' : 3 },
    [4, 5, [7, 9, 1], 3]
]
nested = {
    "h1" : {
        "h2"  : 'test1',
        "h22" : 'test2',
        "h3"  : {
            "h4" : 'test3'
        }
    }
}

assert collect_values(     1, val_fn=lambda v: v==1, only_values=False) == [1]
assert collect_values([1, 2], val_fn=lambda v: v==1, only_values=False) == [[1, 2]]
assert collect_values([1, 2], val_fn=lambda v: v==1, only_values=True)  == [1]
assert collect_values(struct, val_fn=lambda v: v==3, only_values=True)  == [3, 3]
assert collect_values(struct, val_fn=lambda v: v==1, only_values=False) == [[5, 2, 1], [7, 9, 1]]
assert collect_values(struct, val_fn=lambda v: v==3, only_values=False) == [{ 'a' : 2, 'b' : [5, 2, 1], 'c' : 3 }, [4, 5, [7, 9, 1], 3]]

assert collect_by_key({'a' : 1}, key_fn=lambda k: k=='a', only_values=False) == [{'a' : 1}]
assert collect_by_key({'a' : 1}, key_fn=lambda k: k=='a', only_values=True)  == [1]
assert collect_by_key(struct, key_fn=lambda k: k=='b', only_values=False) == [{ 'a' : 2, 'b' : [5, 2, 1], 'c' : 3 }]
assert collect_by_key(struct, key_fn=lambda k: k=='b', only_values=True)  ==  [[5, 2, 1]]
assert collect_by_key(struct, key_fn=lambda k: True, only_values=False)   == [{ 'a' : 2, 'b' : [5, 2, 1], 'c' : 3 }]
assert collect_by_key(struct, key_fn=lambda k: True, only_values=True)    == [2, 3, [5, 2, 1]] # Order might change
assert collect_by_key(nested, key_fn=lambda k: k=='h4', only_values=True)  == ['test3']
assert collect_by_key(nested, key_fn=lambda k: k=='h4', only_values=False) == [{'h4' : 'test3'}]
assert collect_by_key(nested, key_fn=lambda k: k.startswith('h2'), only_values=True) == ['test1','test2']
