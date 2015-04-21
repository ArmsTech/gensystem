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
