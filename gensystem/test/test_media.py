"""Unit tests for gensystem media."""

import bs4
import mock
import pytest

import gensystem.media as gensystem_media


@mock.patch('gensystem.utils.soupify')
def test_get_media_file_url_success(m_soupify):
    """Test get_media_file_url sucessfully gets a gentoo media URL."""
    fake_soupified = mock.MagicMock()
    fake_soupified.find_all.return_value = [
        bs4.BeautifulSoup('<a href="stage3-20151225.tar.bz2">test</a>').a]
    m_soupify.return_value = fake_soupified

    media_url = gensystem_media.get_media_file_url(
        'http://test.com/mirror', 'amd64', 'stage3')
    assert media_url == (
        'http://test.com/mirror/releases/amd64/'
        'autobuilds/current-stage3-amd64/stage3-20151225.tar.bz2')


@mock.patch('gensystem.utils.soupify')
def test_get_media_file_url_fail(m_soupify):
    """Test get_media_file_url failing to get a gentoo media URL."""
    fake_soupified = mock.MagicMock()

    # No links were found
    fake_soupified.find_all.return_value = []
    m_soupify.return_value = fake_soupified
    assert pytest.raises(
        RuntimeError, gensystem_media.get_media_file_url,
        'http://test.com/mirror', 'amd64', 'stage3')

    # Something besides a link was somehow captured
    fake_soupified.find_all.return_value = [
        bs4.BeautifulSoup('<b>This is not a link.</b>').b]
    m_soupify.return_value = fake_soupified
    assert pytest.raises(
        RuntimeError, gensystem_media.get_media_file_url,
        'http://test.com/mirror', 'amd64', 'stage3')
