import re


def grep(pattern, text):
	""" Grep in text with regex or simple string """
	lines = text.splitlines()
	new_lines = []
	for line in lines:
		if re.match(pattern, line) or pattern in line:
			new_lines.append(line)
	return '\n'.join(new_lines)


# --------------------------------- Tests --------------------------------------


assert grep('this', 'this is cool') == 'this is cool'
assert grep('cool', 'this is cool') == 'this is cool'
assert grep('is', 'this is cool') == 'this is cool'

assert not grep(r'^is', 'this is cool') == 'this is cool'
assert grep(r'^this', 'this is cool') == 'this is cool'
assert not grep(r'$this', 'this is cool')
