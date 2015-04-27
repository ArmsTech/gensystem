"""Gentoo Linux media and related functions."""

from collections import namedtuple
import os
import re

import gensystem.utils as gensystem_utils

GENTOO_MEDIA = {
    'Minimal (iso)': 'minimal',
    'Hardened (tar.gz)': 'hardened',
    'Stage3 (tar.gz)': 'stage3',
    'No-Multi-Lib (tar.gz)': 'nomultilib',
    'Live DVD (iso)': '12.1'}

Arch = namedtuple('Arch', 'name minimal stage3 hardened nomultilib')
AMD64 = Arch(
    'amd64',
    'current-install-amd64-minimal::install-amd64-minimal-\d{8}.iso$',
    'current-stage3-amd64::stage3-amd64-\d{8}.tar.bz2$',
    'current-stage3-amd64-hardened::stage3-amd64-hardened-\d{8}.tar.bz2$',
    'current-stage3-amd64-nomultilib::stage3-amd64-nomultilib-\d{8}.tar.bz2$')
SUPPORTED_ARCH = {'amd64': AMD64}


def get_media_file_url(folder_url, file_regex):
    """Get the URL path to gentoo media.

    Args:
        folder_url (str): Gentoo media folder url.
        file_regex (str): Regex to match media file.

    Returns:
        str: URL path to the specified media.

    """
    soupified_folder = gensystem_utils.soupify(folder_url)
    links = soupified_folder.find_all(href=re.compile(file_regex))
    try:
        # Use -1 index to avoid image links
        return os.path.join(folder_url, links[-1]['href'])
    except (IndexError, KeyError):
        raise RuntimeError("Gentoo media file not found in %s." % folder_url)
