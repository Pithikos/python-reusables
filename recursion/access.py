'''
This implementation is a fast way to access specific elements in a complex
nested structure. Keystring is a simple string that holds keys and indice
separated by semicolons. A semicolon without a key or index will end in going
through all the elements in that context.

Example:
  access('0:0', lst)         # Is the same as lst[0][0]
  access('squares:0', lst)   # Is the same as lst['squares'][0]
  access('squares::0', lst)  # This will loop through lst['squares'] and for every item will give item[0]

As you might notice, this function is most useful when used with complex
nested structures. A second observation that to be made is that all output
of the function depends highly in the context. So some times you get back
a single list and sometimes a list of lists, etc.

'''
def access(keystring, container):
    key_sequence = keystring.rstrip(':').split(':')
    for i in range(len(key_sequence)):
        if key_sequence[i].isdigit():
            key_sequence[i] = int(key_sequence[i])
    def use_key(key, container):
        # case: empty str
        if key[0]=='':
            items = []
            if isinstance(container, dict):
                for k in container:
                    if len(key)>1:
                        items.append(use_key(key[1:], container[k]))
                    else:
                        items.append(container[k])
            elif hasattr(container, '__iter__'):
                for item in container:
                    items.append(use_key(key[1:], item))
            return items
        # case: index or key and still many keys
        elif len(key)>1:
            return use_key(key[1:], container[key[0]])
        # case: single index or key
        else:
            #print(type(container))
            if (isinstance(container, dict) and key[0] in container) or\
                (hasattr(container, '__iter__') and key[0]<len(container)):
                return container[key[0]]
            else:
                return None
    return use_key(key_sequence, container)





################################# EXAMPLE ##############################

devices = [

  {'classes':  [('2', 'Communications'),
                ('255', 'Vendor Specific Class'),
                ('10', 'CDC Data'),
                ('8', 'Mass Storage')],
   'idProduct': ('0x374b', ''),
   'idVendor':  ('0x0483', 'STMicroelectronics'),
   'serial':    ('3', 'ap67')},
   
  {'classes':  [('3', 'Human Interface Device'),
                ('2', 'Communications'),
                ('10', 'CDC Data'),
                ('8', 'Mass Storage')],
  'idProduct':  ('0x0204', 'LPC1768'),
  'idVendor':   ('0x0d28', 'NXP'),
  'serial':     ('3', 'ap68')}
  
]

print(access(':classes::1', devices))   # => [['Communications', 'Vendor Specific Class', 'CDC Data', 'Mass Storage'], ['Human Interface Device', 'Communications', 'CDC Data', 'Mass Storage']]
print(access(':serial:1', devices))     # => ['ap67', 'ap68']
print(access(':idVendor:1', devices))   # => ['STMicroelectronics', 'NXP']
print(access('idVendor:1', devices[0])) # => 'STMicroelectronics'





################################# TESTS ################################
nums = [
    [3, 5, 7, 1],
    [3, 2, 1]
]
assert access(':3', nums)  == [1, None]
assert access(':10', nums) == [None, None]


nums = {
    'a': [1, 2, 3],
    'b': [5, 2, 1],
}
assert access(':', nums) == [[1, 2, 3], [5, 2, 1]]
assert access(':0', nums) == [1, 5]


nums = [
    {'a':1, 'b':2, 'c':3},
    {'a':5, 'b':2, 'c':1},
    {'x':2, 'y':1, 'z':1},
]
assert access(':a', nums) == [1, 5, None]
assert access(':c', nums) == [3, 1, None]
