# Standard Library
from dataclasses import dataclass
from pathlib import Path
import errno # For error handling
import os # For error handling

# Third party

# Local
#from rewrite import tex # For appending tex.NewPage to problemset

@dataclass(frozen=True)
class Image():
    """Represents an image that will appear in an assessment."""

    path: object

    @classmethod
    def from_series(cls, series: object, image_path: str = '') -> object:
        """Constructs a image cell from a Pandas series."""

        # Get the relative path
        path = series['path']
        # Convert kwargs string to dictionary
        if series.isnull()['arguments']:
            kwargs = dict()
        else:
            kwargs = ast.literal_eval(series['arguments'])

        image = cls.from_dir(path, image_path, **kwargs)

        return image

    @classmethod
    def from_dir(cls, path: str, parent: str = '', **kwargs) -> object:
        """Constructs a image cell from a directory."""

        # Create the full path
        path = cls.get_full_path(path, parent)

        image = cls(path)

        return image

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