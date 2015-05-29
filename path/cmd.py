import os
from .file import barename

"""
Returns the absolute path to a command. Notice that no checking
is being made to see if the file is executable or not.
"""
def find_cmd_abspath(cmd):
    if not 'PATH' in os.environ:
        raise Exception("Can't find command path for current platform ('%s')" % sys.platform)
    PATH = os.environ['PATH']
    PWD  = os.getcwd()
    lookup_paths = PWD + os.pathsep + PATH

    for path in lookup_paths.split(os.pathsep):
        for filename in os.listdir(path):
            if barename(filename) == barename(cmd):
                return path + os.sep + filename
    return None



from ..inspection.callers import get_caller_name

"""
Checks to see if the command given is a valid command.
"""
def is_cmd_valid(cmd):
    caller = get_caller_name()
    abspath = find_cmd_abspath(cmd)
    if not abspath:
        print("%s: Command '%s' can't be found" % (caller, cmd))
        return False
    if not is_exec(abspath):
        print("%s: Command '%s' resolves to file '%s' which is not executable" % (caller, cmd, abspath))
        return False
    return True
