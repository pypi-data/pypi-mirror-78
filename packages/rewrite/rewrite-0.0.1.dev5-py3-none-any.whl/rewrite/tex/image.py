from pylatex import Figure
from pylatex.utils import NoEscape
from pylatex.base_classes import Command
import pathlib

class Image(Figure):
    """LaTeX representation of an image."""

    _latex_name = 'figure'
    #filename = pathlib.Path(__file__).parent / 'Images' / 'FiniteTiles.png'
    #filename = str(filename)

    def __init__(self, image, position='h', width=NoEscape(r'\linewidth')):
        self.path = str(image.path)
        self.position = position
        self.width = width
        super().__init__(position=self.position)
        self.add_image(self.path, width=self.width)

class FiniteTiles(Figure):
    """Inserts the finite tiles image."""

    _latex_name = 'figure'
    filename = pathlib.Path(__file__).parent / 'Images' / 'FiniteTiles.png'
    filename = str(filename)

    def __init__(self):
        super().__init__(position='h!')
        self.add_image(self.filename, width=NoEscape(r'\linewidth'))