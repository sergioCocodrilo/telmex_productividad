
import inspect
import typing

import rda_v2

commands = [f for f in inspect.getmembers(rda_v2) if inspect.isfunction(f[1])]

for c in commands:
    print(c[0])
    # print('\t', inspect.getargs(c[1].__code__)[0])
    print('\tDocstring:', c[1].__doc__)
    print('\tArguments and types:')
    for arg, arg_type in typing.get_type_hints(c[1]).items():
        print(f'\t\t{arg}: {arg_type}')
    print()
