"""Functions for dealing with temporary files."""

import contextlib
import shutil
import tempfile


@contextlib.contextmanager
def temp_directory():
    """Supply, then clean up a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
