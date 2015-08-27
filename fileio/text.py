import re

def prepend_text(file, text, after=None):
    ''' Prepend file with given raw text '''
    f_read = open(file, 'r')
    buff = f_read.read()
    f_read.close()
    f_write = open(file, 'w')
    inject_pos = 0
    if after:
        pattern = after
        inject_pos = buff.find(pattern)+len(pattern)
    f_write.write(buff[:inject_pos] + text + buff[inject_pos:])
    f_write.close()

def append_line(file, line):
    ''' Append a line to a file '''
    if not os.path.exists(file):
        print("Can't append to file '%s'. File does not exist." % file)
        return
    f = open(file, 'a')
    f.write(line + '\n')
    f.close()

def replace_line(file, line, replacement):
    ''' Replace a single line '''
    f_read = open(file, 'r')
    lines = f_read.readlines()
    f_read.close()
    for i in range(len(lines)):
        if line.rstrip() == lines[i].rstrip():
            lines[i] = replacement.rstrip() + '\n'
            break
    f_write = open(file, 'w')
    f_write.write(''.join(lines))
    f_write.close()

def replace_all(file, match, replacement):
    ''' Replaces all occurences of matching string with the replacement string '''
    f_read = open(file, 'r')
    buff = f_read.read()
    f_read.close()
    f_write = open(file, 'w')
    f_write.write(buff.replace(match, replacement))
    f_write.close()


def make_file(file, content):
    ''' Creates a new file with specific content '''
    f = open(file, 'a')
    f.write(content)
    if not content.endswith('\n'):
        f.write('\n')
    f.close()
