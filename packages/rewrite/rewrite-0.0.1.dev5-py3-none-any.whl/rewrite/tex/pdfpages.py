# Standard Library
None

# Third Party
from pylatex import Command, NewPage, Package
from pylatex.base_classes import Arguments, Options

# Local
from rewrite.tex import TexList


class PdfPages(TexList):
    """LaTex representation of a multipage PDF."""

    packages = [Package('pdfpages')]

    def __init__(self, pdf, include_in_page_count=False):
        self.path = str(pdf.path)
        self.include_in_page_count = include_in_page_count

        pdf_path = Arguments(self.path)
        pdf_path.escape = False
        # Ensure that the PDF has a blank headfoot and does not increase the page count.
        options = Options(pages=r'{-}', pagecommand=r'\addtocounter{page}{{-}1}\thispagestyle{empty}')
        options.escape = False
        super().__init__(
            data=[
                NewPage(),
                Command('includepdf', pdf_path, options),
            ]
        )