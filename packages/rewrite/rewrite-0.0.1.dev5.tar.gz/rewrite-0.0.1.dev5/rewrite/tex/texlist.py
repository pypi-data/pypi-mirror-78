# Standard Library
None

# Third Party
from pylatex.base_classes import Container

# Local
#from rewrite import tex

class TexList(Container):

    content_separator = '\n'

    def dumps(self):
        return self.dumps_content()


# Depreciated on 20200205
'''
from pylatex.base_classes import Command, Arguments, Options
from pylatex import SmallText, NewPage
from pylatex.utils import NoEscape

class NewPageMessage(TexList):

    def __init__(self, message=r'Please continue on the next page.'):
        r"""
        Parameters
        ----------
        message: str
            The message to display before starting a new page.
        """

        self.message = message
        arg = Arguments(NoEscape(f'\small{tex.Bold(message).dumps()}'))
        footer_message = Command('fancyfoot', arguments=arg, options=Options('C'))
        super().__init__(
            data=[
                SmallText(tex.Bold(self.message)),
                footer_message,
                NewPage(),
            ]
        )
'''