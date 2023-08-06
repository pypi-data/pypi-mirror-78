# Standard Library
from dataclasses import dataclass
import ast # For parsing arguments

# Third party

# Local

@dataclass(frozen=True)
class BlankPage():
    """Represents a blank page in an assessment."""

    kwargs: dict

    @classmethod
    def from_series(cls, series: object) -> object:
        """Constructs a blank page cell from a Pandas series."""

        # Convert kwargs string to dictionary
        if series.isnull()['arguments']:
            kwargs = dict()
        else:
            kwargs = ast.literal_eval(series['arguments'])

        blankpage = cls(kwargs)

        return blankpage