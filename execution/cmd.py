import subprocess


def pid_to_cmd(pid):
    ''' Get the command to a process'''
    out = get_cmd_output('ps -o args %s' % pid)
    return out[0].split('\n')[1].strip()

def run_cmd(cmd):
	''' Run a command '''
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
	                                        stderr=subprocess.PIPE)
	return proc
	
def get_proc_output(proc):
	out, err = proc.communicate()
	return out.decode(), err.decode()

def get_cmd_output(cmd):
	''' Run a command and get its output'''
	return get_proc_output(run_cmd(cmd))
