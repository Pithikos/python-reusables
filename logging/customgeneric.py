'''
This design let's someone have a Logger class with a single configuration.
Even if the uses erroneously instantiates a class and uses the instance,
the same configuration and state will be used.
'''



# The centralized logger
class Logger:


	# Global configuration for Logger instances and class
	config = {
	}

	# Messages
	WARN    = '\033[93m' + 'WARN:  %s'  + '\033[0m'
	ERROR   = '\033[91m' + 'ERROR: %s'  + '\033[0m'
	INFO    = 'INFO: %s'

	# Generic
	@classmethod
	def warn(self, text):
		print(self.WARN % text)
	@classmethod
	def error(self, text):
		print(self.ERROR % text)
	@classmethod
	def info(self):
		print(self.INFO % text)

	# Relaid
	@classmethod
	def precall_log(self, fn, *args):
		print('PRECALL:  %s called with %s' % (fn.__name__, str(args)))
	@classmethod
	def postcall_log(self, fn, retval):
		print('POSTCALL: %s returned %s' % (fn.__name__, retval))



# Decorator that relays to Logger
def loggable(fn):
	def wrapper(*args):
		Logger.precall_log(fn, args)
		return_value = fn(*args)
		Logger.postcall_log(fn, return_value)
		return return_value
	return wrapper





################################ EXAMPLE ###############################


if __name__ == "__main__":
	
	# Usage 1
	@loggable
	def sum(a, b):
		return a+b
	sum(2, 4)
	
	# Usage 2
	Logger.warn('Computer might get destroyed')
	Logger.error('Computer destroyed')
