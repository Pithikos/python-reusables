'''
Let's you use an expression to select an item, group of items,
or deselect from a collection.

Example:
select('-3', [1, 2, 3])          => [1, 2]
select('1-3,5', [1, 2, 3, 4, 5]) => [1, 2, 3, 5]
select('-1-3', [1, 2, 3, 4, 5])  => [4, 5]

'''
def select(expr, collection):
	selectors = expr.split(',')
	selectors = map(lambda s: s.strip(), selectors)

	def get_range(selector):
		if '-' in selector:
			a, b = map(int, selector.split('-'))
			return range(a, b+1)
		else:
			return [int(selector)]
	
	# reductive selection
	if filter(lambda sel: sel.startswith('-'), selectors):
		for selector in selectors:
			if selector.startswith('-'):
				selector = get_range(selector[1:])
				for n in selector:
					if n in collection:
						collection.remove(n)
		return collection
		
	# selective
	else:
		selected = []
		for selector in selectors:
			for n in get_range(selector):
				if n in collection:
					selected.append(n)
		return selected
