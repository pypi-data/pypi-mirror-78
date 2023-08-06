# Standard Library
from dataclasses import dataclass, asdict, field
from typing import List

# Thrid Party
import pandas as pd


@dataclass(frozen=True)
class Subterm():
    name: str
    start: object
    end: object

@dataclass(frozen=True)
class NoClasses():
    date: object
    message: str

@dataclass(frozen=True)
class Term():
    """A school term during which courses can occur."""

    tid: int
    name: str
    short_name: str
    subterms: dict = field(default_factory=dict)
    no_classes: pd.DataFrame = pd.DataFrame(columns=['date', 'message'])

    def dates(self, subterm_name: str, days: list) -> List[object]:
        """Return a list of section meeting dates accounting for school closings."""

        subterm = self.subterms[subterm_name]

        # Range of dates in the term
        term_dates = pd.date_range(subterm.start, subterm.end)

        # List of class meetings
        dates = [date for date in term_dates if date.weekday() in days]

        # Remove no_classes
        no_classes = self.no_classes['date'].tolist()
        dates = [date for date in dates if date not in no_classes]

        return dates

    @classmethod
    def from_excel(cls, filename: str) -> object:
        """Constructs a term and its subterms from an Excel workbook."""

        # Append '.xlsx' if necessary
        if isinstance(filename, str):
            if '.xlsx' not in filename:
                filename += '.xlsx'
        else:
            raise ValueError("The filename must be a string naming an Excel workbook.")

        # Load the data
        xls = pd.read_excel(filename, sheet_name=None)

        # Make a dictionary of subterms keyed by its name
        subterms = {}
        for index, subterm in xls['subterms'].iterrows():
            name = subterm['name']
            subterms[name] = Subterm(**subterm)

        # Create the term
        tid, name, short_name = xls['term'].iloc[0]
        term = cls(
            tid,
            name,
            short_name,
            subterms=subterms,
            no_classes=xls['no_classes'],
        )

        return term