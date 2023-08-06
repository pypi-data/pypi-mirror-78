# Standard Library
None

# Third Party
from pylatex.base_classes import CommandBase, Arguments
from pylatex import SmallText

# Local
#from rewrite.tex import TexList
from rewrite import tex


class Message(CommandBase):
    """LaTeX representation of a message in the center of the footer."""

    _latex_name = 'cfoot'

    def __init__(self, cell: object):
        r"""
        Parameters
        ----------
        message: str
            The message to display
        """

        self.message = cell.message

        # Replace the default newpage message
        arg = Arguments(SmallText(tex.Bold(self.message)).dumps())
        arg.escape = False
        super().__init__(arguments=arg)