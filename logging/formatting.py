'''
These formaters can be used with the logging module to
alter the way things look
'''


LPURPPLE = '\033[95m'
LYELLOW  = '\033[93m'
LBLUE    = '\033[94m'
GREEN    = '\033[92m'
RED      = '\033[91m'
ENDC     = '\033[0m'
BOLD     = '\033[1m'



# -------------------------- Formatters --------------------------------

# Color messages depending on their levels
class LogColorer(logging.Formatter):
	def format(self, record):
		if record.levelno == logging.WARNING:
			record.msg = LYELLOW + record.msg + ENDC
		elif record.levelno == logging.ERROR:
			record.msg = RED + record.msg + ENDC
		return logging.Formatter.format(self, record)
