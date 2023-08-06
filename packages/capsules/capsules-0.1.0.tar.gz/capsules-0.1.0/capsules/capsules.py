"""Library for temporarily storing functions as modules.

Python library for depositing a function definition inside
a temporary module file.
"""

import doctest
import importlib
import os
import types
import inspect

def capsules(function):
    """
    Save supplied function definition to a module file,
    load that module file, and returned the function from
    the loaded module.
    """
    if not isinstance(function, types.FunctionType):
        raise TypeError('input is not a function')

    if function.__name__ == '<lambda>':
        raise ValueError('lambda functions are not supported')

    try:
        source = inspect.getsource(function)
    except:
        raise

    context_qualified_module = __name__
    context_qualified_path = __name__.replace(".", "/")
    directory = '/__capsules__/' + context_qualified_path
    module_name = '__capsules__.' + context_qualified_module + '.' + function.__name__

    if not os.path.exists('.' + directory):
        os.makedirs('.' + directory)

    path_file = '.' + directory + '/' + function.__name__ + '.py'
    with open(path_file, 'w') as file:
        definition = source
        lines = definition.split('\n')
        if lines[0] == '@capsules':
            definition = '\n'.join(lines[1:])
        file.write(definition)

    spec = importlib.util.spec_from_file_location(module_name, path_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function.__name__)

if __name__ == "__main__":
    doctest.testmod()  # pragma: no cover
