"""Gentoo Linux media and related functions."""

from collections import namedtuple
import os
import re

import gensystem.mirror as gensystem_mirror
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


def get_media_file_url(mirror, arch, media):
    """Get the URL path to gentoo media.

    To get the media file URL, this function builds the releases folder URL
    that houses the downloads. Then using a regular expression, it matches
    the specified media file in that folder and returns the URL path to the
    file.

    Args:
        mirror (str): Gentoo (base) mirror.
        arch (str): The name of the architecture download is for.
        media (str): The name of the media download is for.

    Returns:
        str: URL path to the specified media.

    """
    releases = gensystem_mirror.GENTOO_RELEASES_TEMPLATE % (arch, media)
    folder, regex = os.path.join(mirror, releases[:-1]).split('::')

    soupified_folder = gensystem_utils.soupify(folder)
    links = soupified_folder.find_all(href=re.compile(regex))
    try:
        # Use -1 index to avoid image links
        return os.path.join(folder, links[-1]['href'])
    except (IndexError, KeyError):
        raise RuntimeError("Gentoo media file not found in %s." % folder)
