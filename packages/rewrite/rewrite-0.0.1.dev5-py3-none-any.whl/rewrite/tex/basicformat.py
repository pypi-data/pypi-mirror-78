# Standard Library
None

# Third Party
from pylatex.base_classes import CommandBase

# Local
None

class Bold(CommandBase):

    _latex_name = 'textbf'

    # Overriding the __init__ is not necessary, but it produces a more succinct __repr__
    def __init__(self, text: str):
        self.text = text
        super().__init__(text)

class Italic(CommandBase):

    _latex_name = 'textit'

    # Overriding the __init__ is not necessary, but it produces a more succinct __repr__
    def __init__(self, text: str):
        self.text = text
        super().__init__(text)

class Underline(CommandBase):

    _latex_name = 'underline'

    # Overriding the __init__ is not necessary, but it produces a more succinct __repr__
    def __init__(self, text: str):
        self.text = text
        super().__init__(text)

class Emph(CommandBase):

    # Overriding the __init__ is not necessary, but it produces a more succinct __repr__
    def __init__(self, text: str):
        self.text = text
        super().__init__(text)

#class Hrulefill(CommandBase):
#    """LaTeX representation of a horizonal line the fills the width of the page."""
#    pass