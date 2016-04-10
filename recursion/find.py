def find_values(obj, value, found=[]):
    """
    Multi-purporse finding in a complex structure of arbitrarily mixed
    dict and list.

    value  - the number or string we are looking for

    The return value is a list if found items. The items are the substructures
    that include the value. This gives some context as opposed to returning
    the single found value.
    """
    if obj == value:
        found.append(obj)
    if type(obj) is list:
        if value in obj:
            found.append(obj)
        for item in obj:
            if type(item) is list or type(item) is dict:
                find_values(item, value)
    if type(obj) is dict:
        for key in obj:
            if obj[key] == value:
                found.append(obj)
            if type(obj[key]) is list or type(obj[key]) is dict:
                find_values(obj[key], value)
    return found




############################## Examples ################################
struct = [
    42,
    { 'a' : 2, 'b' : [5, 2, 1], 'c' : 3 },
    [4, 5, [7, 9, 1], 3]
]
print(find_values(struct, value=1)) # => [[5, 2, 1], [7, 9, 1]]
