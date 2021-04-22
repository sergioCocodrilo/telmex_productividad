
'''
What to control:
    commands
        arguments
        docstring

    STRUCTURE OF A COMMAND:
    name: function_name,
    args: its arguments,
    docstring: its docstring,

    So, commands could be lists of dictionaries with that structure.
'''

import inspect

class Cli:
    def __init__(self):
        self.commands = []

    def command(f):
        def wrapper(*args, **kwargs):
            print('making registry')
            new_command = {
                    'name': f.__name__,
                    'args': instpect.getargs(f.__code__)[0],
                    'docstring': f.__doc__,
                    }
            self.commands.append(new_command)
            return f(*args, **kwargs)
        return wrapper


