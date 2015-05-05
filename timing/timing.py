from time import sleep, time
from timeit import default_timer as timer


'''
Run function in the given interval
until it gives success.

fn      - the function to run
args    - an iterable of arguments
timeout - max time for retries
retry_interval - how much to sleep between tries
'''
def timed_retry(fn, args=None, timeout=30, retry_interval=1):

	def run_fn():
		if args:
			return fn(*args)
		else:
			return fn()

	start   = timer()
	elapsed = lambda: timer() - start
	ret = run_fn()
	
	while not ret and elapsed() < timeout:
		sleep(retry_interval)
		ret = run_fn()
	
	return ret
