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


class BlankPage(tex.TexList):
    """LaTeX representation of a blank page in an assessment."""

    def __init__(self, cell: object):

        counter_args = Arguments(['page', r'{-}1'])
        counter_args.escape = False
        super().__init__(
            data=[
                pylatex_NewPage(),
                Command('null'),
                Command('thispagestyle', arguments='empty'),
                Command('addtocounter', arguments=counter_args),  #\addtocounter{page}{{-}1}
                pylatex_NewPage(),
            ]
        )