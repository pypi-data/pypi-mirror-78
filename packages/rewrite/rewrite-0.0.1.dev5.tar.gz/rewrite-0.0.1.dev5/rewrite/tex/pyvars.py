# Standard Library
None

# Third Party
from sympy import Basic as sympy_base_class
import sympy as sp
from pylatex.base_classes import LatexObject as pylatex_base_latex_class
from pylatex.base_classes import Environment
from pylatex import Package
from pylatex.utils import NoEscape

# Local
None

class PyVars(Environment):
    """A pycode environment that initializes pythontex variables.

    vars_dict: dict
        A dictionary with the key-value format `{variable_name : variable_value}`. Each dictionary key is the name of a variable that is assigned the value associtated with the key.
    """

    _latex_name = 'pycode'
    content_separator = '\n'
    packages = [Package('pythontex', options='rerun=always')]

    def __init__(self, vars_dict = None):
        if vars_dict:
            self.vars_dict = vars_dict
        else:
            self.vars_dict = dict()
        super().__init__()

    @staticmethod
    def _is_sympy(value):
        """Returns True if the object is a SymPy object."""

        if hasattr(value, '__module__'):
            if 'sympy' in value.__module__:
                return True
        return False

    def _use_sympy_latex(self, value):
        """Returns True if the object should be converted into a LaTeX string using SymPy's `latex` function."""

        if not self._is_sympy(value):
            return False
        # Matrices are not instances of sympy.Basic
        elif isinstance(value, sympy_base_class):
            if value.is_Number and not value.is_Rational:
                """Note that sp.Basic.is_number is True when the object fits the
                mathematical definition of a number, but we may still want to convert
                the object into a LaTeX string. For example, we want to use the LaTeX
                representation of the number 'pi':
                - pi.is_number = True
                - pi.is_Number = False
                """
                # Don't convert subclasses of Number into LaTeX strings
                return False
        return True

    @staticmethod
    def _is_multiline_str(value):
        if hasattr(value, 'count'):
            if value.count('\n') > 1:
                return True
        return False

    def dumps_content(self):
        """Append 'key = value' for every keyword argument"""

        pyvariables = []
        for key, value in self.vars_dict.items():
            # Convert `value` into its LaTeX representation
            if self._use_sympy_latex(value):
                try:
                    # Assume the object has a latex representation
                    pyvariables.append(f'{key} = r"\ensuremath{{{sp.latex(value)}}}"')
                except:
                    # Otherwise, use the objects string representation
                    pyvariables.append(f'{key} = r"""{value}"""')
            elif isinstance(value, pylatex_base_latex_class):
                try:
                    # Assume the object has a latex representation
                    pyvariables.append(f'{key} = r"""{value.dumps()}"""')
                except:
                    # Otherwise, use the objects string representation
                    pyvariables.append(f'{key} = r"""{value}"""')
            elif isinstance(value, str):
                if self._is_multiline_str(value):
                    # Use triple quotes for multiline strings
                    pyvariables.append(f'{key} = r"""{value}"""')
                else:
                    pyvariables.append(f'{key} = r"{value}"')
            else:
                pyvariables.append(f'{key} = {value}')

        return NoEscape(self.content_separator.join(pyvariables))

# Future tests
"""
# Setup
points_dict = {'pointsA': '(1 point)', 'pointsB': '(2 points)', 'pointsC': '(3 points)'}
points = PyVars(points_dict)

# Test
points.dumps()
# Result
'\\begin{pycode}\npointsA = "(1 point)"\npointsB = "(2 points)"\npointsC = "(3 points)"\n\\end{pycode}'
"""

from typing import Tuple, Union
from string import ascii_uppercase as uppercase # For naming pycode variables like pointsA

class Points(PyVars):
    """A pycode environment that assigns point values within LaTeX

    points : list of ints or floats, optional
        Point values for the each part of the problem.
    """

    def __init__(self, points: Union[Tuple[int], Tuple[float]]) -> object:
        self._points = points

        # Create a dictionary with the format:
        # {'pointsA':points[0], 'pointsB':points[1], ...}
        pairs = {}
        for index, value in enumerate(points):
            # Create key names points[A-Z]
            key = f'points{uppercase[index]}'
            # Set the value using points OR point
            unit = 'points' if value != 1 else 'point'
            value = f'({value} {unit})'
            # Update the pycode variables dictionary
            pairs.update({key: value})

        super().__init__(pairs)

    @property
    def points(self):
        return self._points

# Future tests
"""
# Setup
points = Points((1, 2, 3))

# Test total
points.total
# Result
6

# Test vars_dict
points.vars_dict
# Result
{'pointsA': '(1 point)', 'pointsB': '(2 points)', 'pointsC': '(3 points)'}

# Confirm that var_dict is a valid argument for PyVars
points.dumps()
# Result
'\\begin{pycode}\npointsA = "(1 point)"\npointsB = "(2 points)"\npointsC = "(3 points)"\n\\end{pycode}'

# Confirm that repr is properly formated
points
# Result
Points((1, 2, 3), [])
"""

class Parameters(PyVars):
    """A pycode environment that assigns parameter values within LaTeX"""

    def __init__(self, parameters):
        # Get a dictionary of the parameters attributes
        #all_vars = vars(parameters)
        # Only used attributes listed in pyvars, if it exists
        #if hasattr(parameters, 'pyvars'):
        #    pyvars = {key : all_vars[key] for key in parameters.pyvars}
        #    super().__init__(pyvars)
        #else:
        #    super().__init__(all_vars)
        # Keep the parameters object
        self.parameters = parameters
        super().__init__()

    def __next__(self):
        # Get the next parameters object
        next(self.parameters)
        # Get a dictionary of the parameters attributes
        all_vars = vars(self.parameters)
        # Only used attributes listed in pyvars, if it exists
        if hasattr(self.parameters, 'pyvars'):
            pyvars = {key : all_vars[key] for key in self.parameters.pyvars}
            self.vars_dict.update(pyvars)
        else:
            self.vars_dict.update(all_vars)

        return self