# Standard Library
from dataclasses import dataclass
import ast # For parsing arguments

# Third party

# Local

@dataclass(frozen=True)
class NewPage():
    """Represents a page break in an assessment with a message in the center of the footer."""

    message: str

    @classmethod
    def from_series(cls, series: object) -> object:
        """Constructs a new page cell from a Pandas series."""

        # Convert kwargs string to dictionary
        if series.isnull()['arguments']:
            message = None
        else:
            kwargs = ast.literal_eval(series['arguments'])
            message = kwargs['message']

        newpage = cls(message)

        return newpage