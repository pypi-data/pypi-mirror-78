# Standard Library
None

# Third Party
from pylatex.base_classes import Command, Arguments, Options
from pylatex import SmallText
from pylatex import NewPage as pylatex_NewPage #### Ugly
from pylatex.utils import NoEscape

# Local
#from rewrite.tex import TexList
from rewrite import tex


class NewPage(tex.TexList):
    """LaTeX representation of a page break in an assessment with a message in the center of the footer."""

    def __init__(self, cell: object):
        r"""
        Parameters
        ----------
        message: str
            The message to display before starting a new page.
        """

        self.message = cell.message

        if self.message:
            # Replace the default newpage message
            arg = Arguments(SmallText(tex.Bold(self.message)).dumps())
            arg.escape = False
            footer_message = Command('fancyfoot', arguments=arg, options=Options('C'))
            super().__init__(
                data=[
                    #SmallText(tex.Bold(self.message)),
                    footer_message,
                    pylatex_NewPage(),
                ]
            )
        else:
            # Use the default newpage message
            super().__init__(data=[pylatex_NewPage()])