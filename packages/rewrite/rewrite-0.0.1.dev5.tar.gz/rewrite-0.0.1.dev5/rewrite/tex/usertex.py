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

class UserTex(AssessmentSection):
    """LaTeX representation of a section title followed by user tex."""

    def __init__(self, cell: object):

        # Create a pylatex.sections.Subsubsection object
        super().__init__(cell.title)
        self.append(cell.code)

