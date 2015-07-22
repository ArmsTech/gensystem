"""Functional tests for gensystem utils."""

import os

import gensystem.temp as temp
import gensystem.utils as gensystem_utils

MB = 1000000


def test_download_file():
    """Test download_file with an actual file."""
    url = 'http://mirror.internode.on.net/pub/test/1meg.test'
    with temp.temp_directory() as temp_dir:
        temp_file = os.path.join(temp_dir, '1meg.test')
        downloaded, _ = gensystem_utils.download_file(url, temp_file)

        # Assert file was downloaded and is exactly 1MB
        assert downloaded
        assert os.path.exists(temp_file)
        assert os.path.getsize(temp_file) == 1 * MB
