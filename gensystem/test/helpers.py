"""Helper functions to simplify writing unit tests."""

import contextlib
import StringIO


@contextlib.contextmanager
def mock_open(contents):
    """Mimic __builtin__.open functionality.

    Exists because mock.mock_open doesn't want to work properly with a
    context manager for some reason.
    """
    string_io = StringIO.StringIO(contents)
    try:
        yield string_io
    finally:
        string_io.close()
