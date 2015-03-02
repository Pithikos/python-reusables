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
nested structures.
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
            if isinstance(container, list):
                for item in container:
                    items.append(use_key(key[1:], item))
            elif isinstance(container, dict):
                for k in container:
                    items.append(use_key(key[1:], container[k]))
            return items
        # case: index or key and still many keys
        elif len(key)>1:
            return use_key(key[1:], container[key[0]])
        # case: single index or key
        else:
            return container[key[0]]
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
