"""Unit tests for gensystem utils."""

import StringIO
import urllib2

import mock
import pytest

import gensystem.utils as gensystem_utils


@mock.patch(
    'urllib2.urlopen', lambda url: StringIO.StringIO('<b>soupified</b>'))
def test_soupify_sucess():
    """Test soupify sucessfully soupifies a URL."""
    soupified = gensystem_utils.soupify('http://!FakeURL.com')
    assert soupified.text == 'soupified'


@mock.patch('urllib2.urlopen')
def test_soupify_raises_exception_on_failure(m_urlopen):
    """Test soupify raises an exception when urlopen fails."""
    m_urlopen.side_effect = urllib2.URLError("Forced URLError.")
    assert pytest.raises(
        RuntimeError, gensystem_utils.soupify, ('http://!FakeURL.com',))


def test_get_choices_sorted():
    """Test get_choices with sorting (default)."""
    choices = gensystem_utils.get_choices(['B', 'A', 'D', 'C'])
    assert choices == {'A': 1, 'B': 2, 'C': 3, 'D': 4}


def test_get_choices_not_sorted():
    """Test get_choices without sorting."""
    unsorted_choices = gensystem_utils.get_choices(
        ['B', 'A', 'D', 'C'], sort=False)
    assert unsorted_choices == {'A': 2, 'B': 1, 'C': 4, 'D': 3}


@mock.patch.object(gensystem_utils, 'get_raw_input', lambda prompt: 1)
def test_get_user_choice_valid_choice():
    """Test get_user_choice using a valid choice."""
    choice = gensystem_utils.get_user_choice("Test prompt:", {'A': 1, 'B': 2})
    assert choice == 'A'


@mock.patch.object(gensystem_utils, 'get_raw_input')
def test_get_user_choice_invalid_choice(m_get_raw_input):
    """Test get_user_choice using invalid choices."""
    # Test user choice valid type but not in valid choices
    m_get_raw_input.side_effect = [3, 1]
    choice = gensystem_utils.get_user_choice("Test prompt:", {'A': 1, 'B': 2})
    assert len(m_get_raw_input.mock_calls) == 2 and choice == 'A'

    # Test user choice is not a valid type (int)
    m_get_raw_input.side_effect = ['This should be an integer.', 2]
    choice = gensystem_utils.get_user_choice("Test prompt:", {'A': 1, 'B': 2})
    # 2 calls + the 2 from above should = 4
    assert len(m_get_raw_input.mock_calls) == 4 and choice == 'B'


def test_get_raw_input():
    """Test get_raw_input."""
    # get_raw_input is just a wrapper for raw_input
    pytest.skip("Built-in raw_input cannot be mocked and tested effectively.")


def test_get_choice_value_choice_found():
    """Test get_choice_value when the choice is found."""
    value_A = gensystem_utils.get_choice_value(1, {'A': 1, 'B': 2})
    value_B = gensystem_utils.get_choice_value(2, {'A': 1, 'B': 2})
    assert value_A == 'A' and value_B == 'B'


def test_get_choice_value_choice_not_found():
    """Test get_choice_value when the choice is not found."""
    value = gensystem_utils.get_choice_value(3, {'A': 1, 'B': 2})
    assert value is None


def test_format_choice_10_choices_or_less():
    """Test format_choice when there are <= 10 choices."""
    # ten_or_more_choices default is False
    formatted_choice = gensystem_utils.format_choice(3)
    assert formatted_choice == '[3]'

    formatted_choice = gensystem_utils.format_choice(10)
    assert formatted_choice == '[10]'


def test_format_choice_more_than_10_choices():
    """Test format_choice when there are > 10 choices."""
    formatted_choice = gensystem_utils.format_choice(
        3, ten_or_more_choices=True)
    assert formatted_choice == '[ 3]'

    formatted_choice = gensystem_utils.format_choice(
        11, ten_or_more_choices=True)
    assert formatted_choice == '[11]'


@mock.patch('urllib.urlretrieve')
@mock.patch('os.path.exists', lambda path: True)
def test_download_file_success(m_urlretrieve):
    """Test download_file succeeding."""
    m_urlretrieve.return_value = ('/tmp/fake/path', 'HTTPMessage Object')
    downloaded, _ = gensystem_utils.download_file(
        'http://!FakeURL.com/file.tar.gz', '/tmp/fake/path')
    assert downloaded
    m_urlretrieve.assert_called_once_with(
        'http://!FakeURL.com/file.tar.gz', '/tmp/fake/path')


@mock.patch('urllib.urlretrieve')
def test_download_file_failure(m_urlretrieve):
    """Test download_file failing."""
    m_urlretrieve.side_effect = IOError('Forced IOError')
    downloaded, error = gensystem_utils.download_file(
        'http://!FakeURL.com/file.tar.gz', '/tmp/fake/path')
    assert not downloaded
    assert error == 'Forced IOError'
