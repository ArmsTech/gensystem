"""Utilities for dealing with all things Gentoo Linux."""

import urllib2

from bs4 import BeautifulSoup


def soupify(url_path):
    """Get BeautifulSoup representation of a web page.

    :param url_path: full path to url to soupify
    :type url_path: str
    :return: soup representation of url_path
    :rtype: bs4.BeautifulSoup

    """
    try:
        response = urllib2.urlopen(url_path)
    except urllib2.URLError:
        raise RuntimeError("Could NOT talk to %s." % url_path)

    return BeautifulSoup(response.read())
