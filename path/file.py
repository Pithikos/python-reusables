import os


def barename(filename):
    """ Returns the part of a filename without the file extension or/and path
        
        'a/b/c.exe' => 'c'
        'c.exe'     => 'c'
    """
    return os.path.splitext(os.path.basename(filename))[0]


def is_exec(path):
    return os.access(path, os.X_OK)
