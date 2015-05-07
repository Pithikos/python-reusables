from command import *

assert find_cmd_abspath('ls') == '/bin/ls'
assert find_cmd_abspath('fsdfasdfasdfas') == None
assert find_cmd_abspath('/bin/ls') == '/bin/ls'
print(find_cmd_abspath('_tests.py'))
