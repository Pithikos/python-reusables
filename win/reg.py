import string
if sys.version_info[0]<3:
    from _winreg import *
else:
    from winreg import *



'''
Iterates over values of given key
'''
def iter_vals(key):
    for i in range(QueryInfoKey(key)[1]):
        yield EnumValue(key, i)

'''
Iterates over subkeys of given key
'''
def iter_keys(key):
    for i in range(QueryInfoKey(key)[0]):
        yield OpenKey(key, EnumKey(key, i))

'''
Iterates over subkeys of given key and returns each subkey as a string
'''
def iter_keys_as_str(key):
    for i in range(QueryInfoKey(key)[0]):
        yield EnumKey(key, i)

'''
Returns the ASCII from a garbled regbin value
'''
def regbin2str(regbin):
    return filter(lambda ch: ch in string.printable, regbin)



# ----------------------------- EXAMPLE --------------------------------


def get_mounted_devices():
    mounts = OpenKey(HKEY_LOCAL_MACHINE, 'SYSTEM\MountedDevices')
    return [(val[0], regbin2str(val[1])) for val in iter_vals(mounts)]
    
print(get_mounted_devices())
