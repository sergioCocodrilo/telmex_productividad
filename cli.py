
import inspect

class Cli:
    def __init__(self):
        self.commands = []

    def add_command(self, f):
        def wrapper(*args, **kwargs):
            new_command = {
                    'name': f.__name__,
                    'args': inspect.getargs(f.__code__)[0],
                    'docs': f.__doc__,
                    }

            self.commands.append(new_command)
            return f(*args, **kwargs)
        return wrapper


# cli = Cli()
# @cli.add_command
# def f(a, b):
    # '''docstring of f'''
    # return a + b

# print(f(1, 1))
