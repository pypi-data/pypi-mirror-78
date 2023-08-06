"""
Subclasses that can be used to create classes represeting LaTeX objects.
"""
###### Possible packages
'bm' # for bold math
# Package('euscript', options='mathscr'), # For printing the script U symbol for the universal set
'standalone' # For problems
# Package('pythontex', options='rerun=always'), # For accessing python variables from tex
from pylatex import Package
PACKAGES = [
    Package('assessments'),
    Package('myvenndiagram'), # For creating Venn diagrams % I had to edit the venndiagram package, because it did not recognize the version number of the PGF package
    Package('rewrite'), ##### TeX commands that should be replaced by PyLaTeX
    Package('amsmath'),
    Package('multicol'), # For multiple columns
    Package('euscript', options='mathscr'), # For the universal set script U
    Package('kbordermatrix'), # For labeling the rows and columns of a matrix
    Package('array'), # For vertical alignment of text in the cell of a tabular environment
    Package('linegoal'), # For extending answerlines for the remainder of the line length
]

from . import utils
from .pyvars import PyVars, Points, Parameters
from .bools import ProvideBool, SetBool, IfBool
from .assessment import Assessment
from .problem import Problem
from .nameline import NameLine
from .usertex import UserTex
from .image import Image
from .message import Message
from .texlist import TexList
from .newpage import NewPage ## Must be below TexList
from .blankpage import BlankPage ## Must be below TexList
from .pdfpages import PdfPages ## Must be below TexList
from .custom import AssessmentSection
from .basicformat import Bold, Italic, Underline, Emph
from .problemset import ProblemSet
from .math import System, sympy_tuple, Array