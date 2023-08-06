# Standard Library
from dataclasses import dataclass
from typing import Union, List

# Third party
import pandas as pd
#from pylatex import NewPage

# Local
from rewrite.nameline import NameLine
from rewrite.usertex import UserTex
from rewrite.problem import Problem
from rewrite.image import Image
from rewrite.pdfpages import PdfPages
from rewrite.newpage import NewPage
from rewrite.blankpage import BlankPage
from rewrite.message import Message


@dataclass(frozen=True)
class ProblemSet():
    """Represents a list of objects that appear in an Assessment."""

    cells: tuple

    @property
    def maxpoints(self):
        return sum(
            [sum(item.points) for item in self.cells if isinstance(item, Problem)]
        )

    @classmethod
    def from_df(cls, problemset_df: object, parent: str, problems_path: str) -> object:
        """Constructs a problem set from a Pandas dataframe."""

        # Read the problemset data
        if problemset_df is None:
            problemset_df = pd.DataFrame(columns=['class', 'path', 'points', 'arguments'])

        # Create the list of assessment objects
        cells = []
        for index, row in problemset_df.iterrows():
            class_name = row['class'].strip()
            if class_name == 'NameLine':
                nameline = NameLine.from_series(row)
                cells.append(nameline)
            elif class_name == 'UserTex':
                user_tex = UserTex.from_series(row, parent)
                cells.append(user_tex)
            elif class_name == 'Problem':
                problem = Problem.from_series(row, problems_path)
                cells.append(problem)
            elif class_name == 'NewPage':
                newpage = NewPage.from_series(row)
                cells.append(newpage)
            elif class_name == 'Message':
                message = Message.from_series(row)
                cells.append(message)
            elif class_name == 'Image':
                image = Image.from_series(row, parent)
                cells.append(image)
            elif class_name == 'PdfPages':
                pdf = PdfPages.from_series(row, parent)
                cells.append(pdf)
            elif class_name == 'BlankPage':
                blank_page = BlankPage(row)
                cells.append(blank_page)
                pass
            else:
                raise NameError(f"{row['class']} is not a recognized class name")

        # Convert the problemset to an immutable type
        cells = tuple(cells)

        # Create the problemset
        problemset = cls(cells)

        return problemset