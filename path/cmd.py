import os
from .file import barename


def cmd_paths():
    """ Returns a list of paths found in PATH environment variable.
    """
    if not 'PATH' in os.environ:
        return False
    PATH = os.environ['PATH']
    PATH = os.path.normpath(PATH)
    return PATH.split(os.path.pathsep)
    


""" Returns the absolute path to a command. Notice that no checking
    is being made to see if the file is executable or not.
"""
def find_cmd_abspath(cmd):
    if not cmd_paths():
        raise Exception("Can't find command path for current platform ('%s')" % sys.platform)
    if os.path.isabs(cmd) and os.path.exists(cmd):
        return cmd
    cmd_filename = os.path.basename(cmd)
    for path in cmd_paths():
        if not os.path.exists(path):
            continue
        for entry in os.listdir(path):
            if not os.path.isfile(os.path.join(path, entry)):
                continue
            filename = entry
            if '.' in cmd_filename and filename == cmd_filename:
                return os.path.join(path, filename)
            elif barename(filename) == cmd_filename:
                return os.path.join(path, filename)
    return None


############## TESTS (linux) #############

assert find_cmd_abspath('ls')    == '/bin/ls'
assert find_cmd_abspath('ls.sh') != '/bin/ls'




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
