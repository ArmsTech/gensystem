"""Manage Gentoo Linux media."""

import os
import re

import gensystem.utils as gensystem_utils

GENTOO_MEDIA = {
    'Minimal (iso)': 'minimal',
    'Hardened (tar.gz)': 'hardened',
    'Stage3 (tar.gz)': 'stage3',
    'No-Multi-Lib (tar.gz)': 'nomultilib',
    'Live DVD (iso)': '12.1'}


def get_media_file_url(folder_url, file_regex):
    """Get the path to gentoo media.

    :param folder_url: gentoo media folder url
    :type folder_url: str
    :param file_regex: regex to match media file
    :type file_regex: str
    :return: url path to the specified media
    :rtype: str

    """
    links = gensystem_utils.soupify(folder_url).find_all(
        href=re.compile(file_regex))
    try:
        # Use -1 index to avoid image links
        return os.path.join(folder_url, links[-1]['href'])
    except (IndexError, KeyError):
        raise RuntimeError("Gentoo media file not found in %s" % folder_url)
