import os


def find_cmd_abspath(cmd):
    """ Returns the absolute path to a command.
        None is returned if no absolute path was found.
    """
    if os.path.exists(cmd):
		return os.path.abspath(cmd)
    if not 'PATH' in os.environ:
        raise Exception("Can't find command path for current platform ('%s')" % sys.platform)
    PATH=os.environ['PATH']
    for path in PATH.split(os.pathsep):
        abspath = '%s/%s' % (path, cmd)
        if os.path.exists(abspath):
            return abspath
