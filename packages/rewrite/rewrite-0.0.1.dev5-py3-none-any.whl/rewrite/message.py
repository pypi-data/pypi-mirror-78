# Standard Library
from dataclasses import dataclass
import errno # For error handling
import os # For error handling
import ast # For parsing arguments

# Third party

# Local

@dataclass(frozen=True)
class Message():
    """Represents a message in the center of the footer."""

    message: str

    @classmethod
    def from_series(cls, series: object) -> object:
        """Constructs a message cell from a Pandas series."""

        # Convert kwargs string to dictionary
        kwargs = ast.literal_eval(series['arguments'])
        message = kwargs['message']

        footer_message = cls(message)

        return footer_message