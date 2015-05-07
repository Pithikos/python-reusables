import inspect

"""
When called inside a function, it returns the name
of the caller of that function. The steps going back
in the stack can be adjusted,
"""
def get_caller_name(steps=2):
	return inspect.stack()[steps][3]



# ---------------------------- Example ---------------------------------
def b():
	a()

def a():
	caller = get_caller_name()
	print(caller)

b() # --> a will print 'b'
