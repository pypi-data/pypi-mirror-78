# Standard Library

# Third Party
from pylatex import Package
from pylatex.base_classes import CommandBase

# Locals
None

class NameLine(CommandBase):
    """A LaTeX representation of a line for the student's name."""

    packages = [Package('assessments')]

    def __init__(self, cell: object):
        self.cell = cell

        super().__init__()

# Future tests
"""
# Test
NameLine().dumps()
# Result
'\\nameline'
"""
