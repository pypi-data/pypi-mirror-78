# Standard Library
import warnings # For raising security concerns

# Third Party
from pylatex import Package
from pylatex.base_classes import CommandBase
from pylatex.section import Subsubsection

# Locals
None


class AssessmentSection(Subsubsection):
    """This subclass is necessary because I do not yet (20191130) know how to allow users to import LaTeX packages for their custom instructions and formulas."""

    _latex_name = 'subsubsection'
    packages = [
        Package('titlesec', options='compact'), # Reduce the space before section titles
    ]
    escape = False

    def __init__(self, title: str, **kwargs) -> object:
        super().__init__(title, numbering=False)
        self.title = title

        # Raise a warning about compiling raw user TeX
        message = "Security vulnerability in `rewrite.pylatex_subclasses.custom.AssessmentSection`: User's TeX is compiled without being escaped because `cls.escape = False`"
        warnings.warn(message, Warning)

########################### DEPRECIATED
'''class NameLine(CommandBase):
    """A command that provides a line for the student's name."""

    packages = [Package('assessments')]

    def __init__(self):
        super().__init__()
'''
# Future tests
"""
# Test
NameLine().dumps()
# Result
'\\nameline'
"""
