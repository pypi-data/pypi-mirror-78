# Standard Library
from dataclasses import dataclass
from pathlib import Path
import errno # For error handling
import os # For error handling
import ast # For parsing arguments

# Third party

# Local

@dataclass(frozen=True)
class PdfPages():
    """Represents a multipage PDF that will appear in an assessment."""

    path: object

    @classmethod
    def from_series(cls, series: object, pdf_path: str = '') -> object:
        """Constructs a PdfPages cell from a Pandas series."""

        # Get the relative path
        path = series['path']
        # Convert kwargs string to dictionary
        if series.isnull()['arguments']:
            kwargs = dict()
        else:
            kwargs = ast.literal_eval(series['arguments'])

        pdf = cls.from_dir(path, pdf_path, **kwargs)

        return pdf

    @classmethod
    def from_dir(cls, path: str, parent: str = None, **kwargs) -> object:
        """Constructs a PdfPages cell from a directory."""

        if parent:
            # Create the full path
            path = cls.get_full_path(path, parent)

        pdf = cls(path)

        return pdf

    @classmethod
    def get_full_path(cls, path: str, parent: str = ''):

        # Create the full path
        relative = Path(path)
        path = parent / relative
        cls.validate_path(path)

        return path

    @staticmethod
    def validate_path(path: object):
        """Confirms that the image file exists."""

        # Ensure that the image exists at `path`
        if not path.is_file():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), 'File does not exist: ' + str(path))