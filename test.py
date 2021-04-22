from cli import Cli

cli = Cli()
@cli.add_command
def f(a, b):
    '''docstring of f'''
    return a + b

# print(f(1, 1))
