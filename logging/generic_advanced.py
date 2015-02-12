import sys
import time
import inspect


'''
This design let's someone have a Logger class with a single configuration.
Even if the uses erroneously instantiates a class and uses the instance,
the same configuration and state will be used.
'''





# ---------------------------- Functions -------------------------------

def err(text):
	caller = inspect.stack()[1][3].__name__
	Logger.error('%s(): %s' % (caller, text))
	Logger.warn('Stopping program')
	exit(1)

def info(text):
	Logger.info(text)

def warn(text):
	Logger.warn(text)
	str=args[0]

# Relay decorator
def loggable(fn):
	def wrapper(*args):
		Logger.precall_log(fn, args)
		return_value = fn(*args)
		Logger.postcall_log(fn, return_value)
		return return_value
	return wrapper





# ------------------------------- Logger -------------------------------


class Logger:

	config = {
		'to_log'    : ['warn', 'error', 'info'], # warn, error, info, precall, postcall
		'timestamp' : True
	}

	prev_log = {
		'type'  : None,
		'line'  : None,
		'count' : 1
	}


	# colors
	LPURPPLE = '\033[95m'
	LYELLOW  = '\033[93m'
	LBLUE    = '\033[94m'
	GREEN    = '\033[92m'
	RED      = '\033[91m'
	ENDC     = '\033[0m'
	BOLD     = '\033[1m'


	# Formats
	WARN     = RED     + '%s' + ENDC
	ERROR    = LYELLOW + '%s' + ENDC
	INFO     =           '%s'


	# Generic
	@classmethod
	def warn(self, text):
		if 'warn' in self.config['to_log']:
			text = self.WARN % text
		if self.config['timestamp']:
			text = self.timestamp(text)
		print(text)

	@classmethod
	def error(self, text):
		if 'error' in self.config['to_log']:
			text = self.ERROR % text
		if self.config['timestamp']:
			text = self.timestamp(text)
		print(text)

	@classmethod
	def info(self, text):
		if 'info' in self.config['to_log']:
			text = self.INFO % text
		if self.config['timestamp']:
			text = self.timestamp(text)
		print(text)

	@classmethod
	def timestamp(self, text):
		return self.LBLUE + '[%s] ' % time.ctime()[11:-5]  + self.ENDC + text



	# Relaid
	@staticmethod
	def precall_log(fn, *args):
		if 'precall' in Logger.config['to_log']:
			print('FUNCTION CALL %s(%s)' % (fn.__name__, str(args)))
		
		#
		# HERE YOU FURTHER PROCESS IF WANTED
		#
		
	
	@staticmethod
	def postcall_log(fn, retval):
		if 'postcall' in Logger.config['to_log']:
			print('FUNCTION CALL %s  ---->  %s' % (fn.__name__, str(retval)))
			
		#
		# HERE YOU FURTHER PROCESS IF WANTED
		#






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
