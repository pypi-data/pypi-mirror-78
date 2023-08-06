# Standard Library
from dataclasses import dataclass, field
from typing import Tuple
from functools import wraps # For easier debugging
import errno # For error handling
import os # For error handling
import warnings # For error handling
import ast # For safely evaluating a string containing a Python literal
from pathlib import Path # For manuplating filesystem paths

#Third Party

#Local
from rewrite import tex

@dataclass(frozen=True)
class Problem():
    r"""A problem written in LaTeX with randomly generated parameters.

    Problem objects must have the files `body.tex` and `next.py` in the path directory.
    An optional thrid file, `new.py` should also be in the path directory.
    The LaTeX template of the problem should be in `body.tex` with any dynamic TeX
    written inside environments from the `pythontex <https://ctan.org/pkg/pythontex>`_ package.
    A generator class `Parameters` will be defined and bound to the `Problem` instance.
    The class `problem_instance.Parameters()` will bind `new.py` as its `__inti__()` method and `next.py`
    as its `__next__()` method. Any variables inside of the files `new.py` and `next.py`
    that are prefix with `self.variable_name` will be assigned values inside of a `pycode`
    environment when the `parameters_instance.dumps()` method is called.

    """

    path: object
    points: tuple
    Parameters: type

    @property
    def name(self):
        """Returns the name of the problem."""

        # Make sure the path is not just '.'
        if self.path.stem == '':
            parent = self.path.absolute().stem
        else:
            parent = self.path.stem

        return parent

    @property
    def body(self):
        with open(self.path / 'body.tex', 'r') as f:
            body = f.read()
        return body

    @classmethod
    def example(cls, points: tuple, path: str = '.'):
        """Generates an PDF of the problem in the current directory."""

        # Confirm the a problem object can be created
        path = Path(path)
        cls.validate_path(path)

        # Create the problem and generate the tex
        problem = cls.from_dir(path, points)
        tex_problem = tex.Problem(problem)
        tex_problem.generate_pdf(['example'], clean_tex=False, clean=False)

    @classmethod
    def from_series(cls, series: object, problems_path: str = '') -> object:
        """Constructs a problem from a Pandas series."""

        # Get the relative path
        path = series['path']
        # Convert points string to a tuple
        points = ast.literal_eval(series['points'])
        # Convert kwargs string to dictionary
        if series.isnull()['arguments']:
            kwargs = dict()
        else:
            kwargs = ast.literal_eval(series['arguments'])

        problem = cls.from_dir(path, points, problems_path, **kwargs)

        return problem

    @classmethod
    def from_dir(cls, path: str, points: tuple, problems_path: str = '', **kwargs) -> object:
        """Constructs a problem from a directory."""

        # Create the full path
        full_path = cls.get_full_path(path, problems_path)

        '''
        THE LENGTH OF POINTS CANNOT BE CHECKED WHEN THE QUESTION PARTS ARE SHUFFLED
        # Ensure that the len(points) is correct
        #     Identify the required number of point values
        with open(path / 'body.tex', 'r') as f:
            body = f.read()
            length = body.count('\py{points')
        #     Warn the user if len(points) is not correct
        if length != len(points):
            message = f"The list of point values for '{path.stem}' " + f"must have exactly {length} elements."
            warnings.warn(message, Warning)'''

        # Create the Parameters class
        Parameters = cls.get_parameters(full_path, points, **kwargs)

        problem = cls(
            full_path,
            points,
            Parameters,
        )

        return problem

    @classmethod
    def get_parameters(cls, path: object, points: tuple, **kwargs) -> type:
        par_init = cls.make_method(path, 'init')
        par_next = cls.make_method(path, 'next')

        attributes = {
            '__init__': par_init,
            '__next__': par_next,
            'points': points,
        }
        attributes.update(kwargs)
        Parameters = type('Parameters', (), attributes)
        return Parameters

    @classmethod
    def make_method(cls, path: object, name: str) -> object:
        # Read the optional define.py module into a string
        try:
            with open(path / 'define.py', 'r', encoding='utf-8') as file:
                define = file.read()
        except:
            define = 'None'

        # Ensure that the module exists or do nothing for optional modules
        optional = ['init']
        try:
            # Set the module name
            module = path / (name + '.py')
            # Read the module into a string
            with open(module, 'r', encoding='utf-8') as file:
                contents = file.read()
            ins, code, outs = cls.parse_method(contents)
        except:
            if name in optional:
                ins = tuple()
                code = 'None'
                outs = tuple()
            else:
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), str(par_config))

        # Make the function code
        func = ''
        # Get the input variables
        for var in ins:
            func += f'''if hasattr(self, "{var}"): {var} = self.{var}\n'''
        # Run the function
        func += '\n' + code + '\n\n'
        # Set the output variables
        for var in outs:
            func += f'''if "{var}" in locals(): self.{var} = {var}\n'''
        func = func.strip()

        @wraps(func)
        def wrapped_func(self):
            # Import definitions from define.py
            try:
                exec(define, locals())
            except Exception as e:
                raise Exception(f'{str(e)} in module {module}').with_traceback(e.__traceback__)
            # Run the code
            try:
                exec(func, locals()) #<---- locals() is So that the functions defined in next.py have access to the imported packages like numpy
            except Exception as e:
                raise Exception(f'{str(e)} in module {module}').with_traceback(e.__traceback__)
            # Raise a warning about compiling raw user code
            message = f"Security vulnerability in `rewrite.Problem.make_method()`: User's Python code in `{name}.py` is executed without any security checks."
            warnings.warn(message, Warning)
            if name == 'next':
                return self

        wrapped_func.__name__ = name
        wrapped_func.__module__ = module
        return wrapped_func

    @staticmethod
    def parse_method(contents):
        """Methods must have three parts in order and separated by blank lines:
        - the names of instance attributes to load as local variables and their default values
        - the executable code
        - the names of the local variables to bind as instance attributes."""

        # Prepare the code for parsing by line numbers
        lines = contents.splitlines()
        total_lines = len(lines)
        line_nbs = range(total_lines)

        # Identify the indices of all of the blank lines
        blank_lines = [nb for nb in line_nbs if lines[nb].strip() == '']

        # Search the lines for the first block of code separated by blank lines
        for index, nb in enumerate(blank_lines):
            if index != nb:
                arg_start = index
                arg_end = nb
                break
        # Assume that the first block of code contains the arguments for the method
        ins = lines[arg_start:arg_end]
        # Remove the extra set of quotes
        ins = [s[1:-1] for s in ins if s != 'None']
        ins = tuple(ins)

        # Search the lines for the last block of code separated by blank lines
        total_lines = len(lines)
        reversed_blank_lines = [total_lines - nb for nb in blank_lines[::-1]]
        for index, nb in enumerate(reversed_blank_lines):
            if index != total_lines - nb:
                return_start = total_lines - nb + 1
                return_end = total_lines - index
                break
        # Assume that the last block of code contains the return values for the method
        outs = lines[return_start:return_end]
        # Remove the extra set of quotes
        outs = [s[1:-1] for s in outs if s != 'None']
        outs = tuple(outs)

        # Every line in between the first and last block of code is the method code
        code = '\n'.join(lines[arg_end:return_start - 1])

        return ins, code, outs

    @classmethod
    def get_full_path(cls, path: str, parent: str = ''):

        # Create the full path
        relative = Path(path)
        path = parent / relative
        cls.validate_path(path)

        return path

    @staticmethod
    def validate_path(path: object):
        """Confirms that the path includes the necessary files to generate a problem."""

        # Ensure that the problem exists at `path`
        if path.is_dir():
            par_config = path / 'next.py'
            if not par_config.is_file():
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), 'File does not exist: ' + str(par_config))
            body_config = path / 'body.tex'
            if not body_config.is_file():
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), 'File does not exist: ' + str(body_config))
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), 'Not a directory: ' + str(path))
