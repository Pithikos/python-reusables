'''
A generic tracing class that can be used to trace packages.
This can be very helpful for trying to understand the flow
of a program or a package.

Usage:
tracer = Tracer()
tracer.watch_package('pyOCD')
sys.settrace(tracer.trace)

'''
import inspect
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
        found = False
        for to_trace in self.tracing_packages:
            if modpath.startswith(to_trace):
                found = True
                break
        if not found:
            return self.trace

        # Other info
        fn_name = frame.f_code.co_name
        src_lines = inspect.getsource(frame).split('\n')
        src_line_start = src_lines[0]
        src_line_end = src_lines[-1]
        lineno = frame.f_lineno
        ws = self.whitespace


        '''
        Gives arguments passed to method or function
        in a printable form
        '''
        def beautify_args():
            arg_names = inspect.getargs(frame.f_code).args
            local_vals = inspect.getargvalues(frame).locals 
            arg_dict = { name: frame.f_locals[name] for name in arg_names}
            text = ''
            for name, value in arg_dict.items():
                text += beautify_variable(name, value) + ', '
            return text[:-2]


        '''
        Makes a printable string out of a variable
        '''
        def beautify_variable(name, value):
            return "%s=%s" % (name, beautify_value(value))


        '''
        Gives return value/values of method or function
        in a printable form
        '''
        def beautify_value(var):
            if isinstance(var, int)   or\
               isinstance(var, float) or\
               var == None:
                return str(var)
            elif isinstance(var, str):
                return "'%s'" % str(var)
            else:
                t = type(var)
                if t.__module__ == '__builtin__':
                    return '<%s>' % t.__name__
                else:
                    return '<%s.%s>' % (t.__module__, t.__name__)


        # Print call
        if event == 'call':
            self.indent_lvl += 1
            fn_name   = frame.f_code.co_name
            arg_names = inspect.getargs(frame.f_code).args
            local_vals = inspect.getargvalues(frame).locals 
            arg_dict = { name: frame.f_locals[name] for name in arg_names}
            text = ''
            for name, value in arg_dict.items():
                if isinstance(value, str):
                    text += "%s='%s', " % (name, value)
                elif isinstance(value, int) or isinstance(value, float):
                    text += "%s=%s, "   % (name, value)
                else:
                    text += "%s=%s, " % (name, str(type(value)))
            print('%scallin: %s %s(%s)' % (self.indent_lvl*ws, modpath, fn_name, beautify_args()))


        # Print return
        elif event == 'return':
            print('%sreturn: %s' % (self.indent_lvl*ws, beautify_value(arg)))
            self.indent_lvl -= 1


        return self.trace


    '''
    Watch for a specific package
    '''
    def watch_package(self, packname):
        self.tracing_packages.append(packname)





# ------------------------------ Example -------------------------------

import sys, pyOCD

tracer = Tracer()
tracer.watch_package('pyOCD')
sys.settrace(tracer.trace)

boards = pyOCD.board.MbedBoard.getAllConnectedBoards() # will print call chain for this
