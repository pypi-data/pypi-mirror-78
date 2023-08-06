# Standard Library
from typing import Tuple

# Thrid Party
from pylatex import Enumerate, Package
from pylatex.base_classes import Options

# Local
from rewrite import nameline
from rewrite import usertex
from rewrite import problem
from rewrite import newpage
from rewrite import message
from rewrite import image
from rewrite import pdfpages
from rewrite import blankpage
from rewrite import tex

class ProblemSet(tex.TexList):
    """An enumerated environment for numbering problems"""

    #_latex_name = 'enumerate'
    packages = [Package('enumitem')]
    content_separator = ' \n' # The % in `\end{pycode}%` causes a TeX error

    def __init__(self, cells: Tuple[object], **kwargs) -> object:
        self._cells = cells
        self.problems = [] # For calling next() on all problems

        super().__init__(**kwargs)
        for cell in self.cells:
            if isinstance(cell, nameline.NameLine):
                tex_nameline = tex.NameLine(cell)
                self.append(tex_nameline)
            elif isinstance(cell, usertex.UserTex):
                tex_usertex = tex.UserTex(cell)
                self.append(tex_usertex)
            elif isinstance(cell, problem.Problem):
                tex_problem = tex.Problem(cell)
                self.problems.append(tex_problem)

                # Create a resumed enumeration environment
                enum_env = Enumerate(options=Options('resume'))
                enum_env._latex_name = 'enumerate'
                enum_env.packages.update([Package('enumitem')])
                enum_env.content_separator = ' \n' # The % in `\end{pycode}%` causes a TeX error

                enum_env.add_item(tex_problem.content)
                self.append(enum_env)

            elif isinstance(cell, newpage.NewPage):
                tex_newpage = tex.NewPage(cell)
                self.append(tex_newpage)
            elif isinstance(cell, message.Message):
                tex_message = tex.Message(cell)
                self.append(tex_message)
            elif isinstance(cell, image.Image):
                tex_image = tex.Image(cell)
                self.append(tex_image)
            elif isinstance(cell, pdfpages.PdfPages):
                tex_pdf = tex.PdfPages(cell)
                self.append(tex_pdf)
            elif isinstance(cell, blankpage.BlankPage):
                tex_blankpage = tex.BlankPage(cell)
                self.append(tex_blankpage)
            else:
                self.append(cell)

    @property
    def cells(self):
        return self._cells

    def __next__(self):
        # Call next() on each problem
        for problem in self.problems:
            next(problem)