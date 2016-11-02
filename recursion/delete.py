def delete_keys(obj, key=None, value=None):
    """
    Remove all dict keys recursively in an arbitrary structure.

    Takes:
        obj(iterable):   structure to be parsed
        value(function): predicate that needs matching against a value
        key(function):   predicate that needs matching against a key

    Return:
        Updated object
    """
    if type(obj) is list:
        if len(obj)>1:
            return [delete_keys(obj[0], key, value)] + delete_keys(obj[1:], key, value)
        else:
            return [delete_keys(obj[0], key, value)]
    elif type(obj) is dict:
        for k,v in obj.items():
            if type(v) is dict or type(v) is list:
                obj[k] = delete_keys(v, key, value)
            if key and key(k) or value and value(v):
                del obj[k]
        return obj
    else:
        return obj





# --------------------------------- Tests --------------------------------------
from copy import deepcopy as clone

nested = {
    "h1" : {
        "h2"  : 'test1',
        "h22" : 'test2',
        "h3"  : {
            "h4" : 'test3'
        }
    }
}
assert delete_keys([1]) == [1]
assert delete_keys(clone(nested), key=lambda k: k=='h22') == {'h1': {'h2': 'test1', 'h3': {'h4': 'test3'}}}
assert delete_keys(clone(nested), key=lambda k: k=='h3') == {'h1': {'h2': 'test1', 'h22': 'test2'}}
assert delete_keys(clone(nested), value=lambda v: v=='test2') == {'h1': {'h2': 'test1', 'h3': {'h4': 'test3'}}}
