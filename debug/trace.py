'''
A generic tracing class that can be used to trace packages.
This can be very helpful for trying to understand the flow
of a program or a package.

Usage:
tracer = Tracer()
tracer.watch_package('pyOCD')
sys.settrace(tracer.trace)

'''
class Tracer(object):
	
	
    def __init__(self):
        self.tracing_packages = []
        self.whitespace = '    '
        self.indent_lvl = 0

	'''
	This method should be set by sys.settrace
	'''
    def trace(self, frame, event, arg):

        # Module info
        mod = inspect.getmodule(frame)
        if mod:
            modpath = mod.__name__
        else:
            modpath = '<no module>'

        # Just return if not interested in package
        for to_trace in self.tracing_packages:
            if not modpath.startswith(to_trace):
                return self.trace

        # Other info
        fn_name = frame.f_code.co_name
        src_lines = inspect.getsource(frame).split('\n')
        src_line_start = src_lines[0]
        src_line_end = src_lines[-1]
        lineno = frame.f_lineno
        ws = self.whitespace

        # Printing
        if event == 'call':
            self.indent_lvl += 1
            print('%scallin: %s %s %s' % (self.indent_lvl*ws, modpath, fn_name, str(arg)))
        elif event == 'return':
            if isinstance(arg, object):
                ret = type(arg)
            else:
                ret = str(arg)
            print('%sreturn: %s' % (self.indent_lvl*ws, ret))
            self.indent_lvl -= 1
        return self.trace

	'''
	Watch for a specific package
	'''
    def watch_package(self, packname):
        self.tracing_packages.append(packname)





# ------------------------------ Example -------------------------------

import sys, inspect, pyOCD

tracer = Tracer()
tracer.watch_package('pyOCD')
sys.settrace(tracer.trace)

pyOCD.board.MbedBoard.listConnectedBoards() # will print call chain for this
