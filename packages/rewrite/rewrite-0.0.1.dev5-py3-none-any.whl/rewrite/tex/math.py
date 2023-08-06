# Standard Library
None

# Third Party
from pylatex.base_classes import Environment
from pylatex import Math
import sympy as sp

# Local
None

def separated_integer(integer):
    """Returns a LaTeX representation of an integer with 1000s separated by commas."""

    integer = int(integer)
    return f'{integer:,}'

def unaltered_rational(numerator, denominator):
    """Returns a LaTeX representation of a rational number without any simplification."""

    return fr'\dfrac{{ {numerator} }}{{ {denominator} }}'

def ProbRational(numerator, denominator):
    return sp.Mul(numerator, sp.Rational(1, denominator), evaluate=False)

def sympy_tuple(vector):
    entry = map(sp.latex, vector)
    entries = ', '.join(entry)
    tex = f'$\\left({entries} \\right)$'
    return tex

class Array(Environment):
    content_separator = '\n'
    escape = False

class System(Math):

    size = 2

    def __init__(self, K, R, B):
        self.K = K
        self.R = R
        self.B = B

        # Create list of latex symbols for new columns and rows
        new_column = ['&' for i in range(K.rows)]
        new_row = [r'\\' for i in range(K.rows)]
        # Convert the relations to their TeX representaitons
        relmap = {
            "==": "=",
            ">": ">",
            "<": "<",
            ">=": r"\geq",
            "<=": r"\leq",
            "!=": r"\neq",
        }
        relations = [relmap[r.rel_op] for r in R]

        nb_of_vars = K.shape[1]
        if nb_of_vars == 2:
            x, y = sp.symbols('x y')
            X = sp.Matrix([x, y])
        elif nb_of_vars == 3:
            x, y, z = sp.symbols('x y z')
            X = sp.Matrix([x, y, z])
        else:
            raise ValueError(f'Systems with {nb_of_vars} variables is not yet supported.')

        # Create the array environment for the system
        system = Array(arguments='rcr')
        for row in zip(K*X, new_column, relations, new_column, B, new_row):
            statement = ' '.join(map(sp.latex, row))
            system.append(statement)

        super().__init__()
        self.append(system)