# Standard Library
from dataclasses import dataclass
from typing import Union, List
import errno # For error handling
import os # For error handling
from pathlib import Path # For manuplating filesystem paths


# Third party
import pandas as pd

# Local
from rewrite.problem import Problem
from rewrite.problemset import ProblemSet
from rewrite.pdfpages import PdfPages


@dataclass(frozen=True)
class Assessment():
    """An assessment written in LaTeX with randomly generated parameters."""
    kind: str
    number: int
    fullpoints: Union[int, float]
    problemset: object = None

    @property
    def maxpoints(self):
        return self.problemset.maxpoints

    @classmethod
    def from_excel(cls, filename: str, names: List[str] = None) -> object:
        """Constructs a dictionary of assessments using `Assessment.from_series()` from an Excel workbook. The keys are `assessment.name`"""

        # Append '.xlsx' if necessary
        if isinstance(filename, str):
            if '.xlsx' not in filename:
                filename += '.xlsx'
        else:
            raise ValueError("The filename must be a string naming an Excel workbook.")

        # Load the data
        xls = pd.read_excel(filename, sheet_name=None)

        # Create the list of assessment names to create
        if names is None:
            names = list(assessments_df['name'])
        elif not isinstance(names, list):
            names = [names]
        # Filter out unwanted assessments
        df = xls['assessments']
        assessments_df = df[df.name.isin(names)]
        # Make a dictionary of assessments keyed by name
        assessments = {}
        for index, assessment_series in assessments_df.iterrows():
            name = assessment_series['name']
            problemset_df = xls[name]
            assessments[name] = Assessment.from_series(assessment_series, problemset_df)

        return assessments

    @classmethod
    def from_series(cls, series: object, problemset_df: object) -> object:
        """Constructs an assessment from a Pandas series and its problems from a Pandas dataframe."""

        # Set the parent path
        parent = series['path']

        # Create the problemset
        problems_path = cls.get_full_path(parent, series['problems'])
        problemset = ProblemSet.from_df(problemset_df, parent, problems_path)

        # Create the assessment
        assessment = cls(
            series['kind'],
            series['number'],
            series['fullpoints'],
            problemset=problemset,
        )

        return assessment

    @classmethod
    def get_full_path(cls, parent: str,  relative: str = ''):
        """Validates and returns the full path as a PathLib object."""

        # Create the full path
        parent = Path(parent)
        relative = Path(relative)
        full_path = parent / relative

        if full_path.exists():
            return full_path
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), full_path)