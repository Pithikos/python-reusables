import re


def uniq(text):
	""" Keep unique lines from text without sorting! """
	lines = text.splitlines()
	new_lines = []
	for line in lines:
		if line not in new_lines:
			new_lines.append(line)
	return '\n'.join(new_lines)


# --------------------------------- Tests --------------------------------------

assert uniq('a\na') == 'a\n' or uniq('a\na') == 'a'
assert uniq('a\nb\na\nc') == 'a\nb\nc'
