from threading import Thread


'''
Run a whole function as a seperate thread.

Usage:
  * Decorate a function and the function will run as a thread.

Notice that you will not get back any return value from the function
that you decorate.
'''
def threaded(fn):
	def wrapper(*args):
		t = Thread(target=fn, args=args)
		t.daemon = True
		t.start()
	return wrapper
