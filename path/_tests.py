from cmd import *
from file import *

# find_cmd_abspath
assert find_cmd_abspath('ls') == '/bin/ls'
assert find_cmd_abspath('fsdfasdfasdfas') == None
assert find_cmd_abspath('/bin/ls') == '/bin/ls'
assert find_cmd_abspath('/bin/ls.py') == None
print(find_cmd_abspath('_tests.py'))

