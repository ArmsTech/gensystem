#!/usr/bin/env python
# encoding: utf-8

"""Control download and/or install of Gentoo Linux."""

import os
import re
import sys
import urllib2

from bs4 import BeautifulSoup

import gensystem.arch as arch

COLUMN_PADDING = 3

GENTOO_MIRRORS = {}
GENTOO_MIRRORS_URL = 'http://www.gentoo.org/main/en/mirrors.xml'
GENTOO_RELEASES_TEMPLATE = 'releases/%s/autobuilds/%s/'
GENTOO_MEDIA = {
    'Minimal (iso)': 'minimal',
    'Hardened (tar.gz)': 'hardened',
    'Stage3 (tar.gz)': 'stage3',
    'No-Multi-Lib (tar.gz)': 'nomultilib',
    'Live DVD (iso)': '12.1'}

SUPPORTED_ARCH = {'amd64': arch.AMD64}


def get_gentoo_mirrors_by_country(mirrors_soup, country=None):
    """Get gentoo.org mirrors from GENTOO_MIRRORS_URL by country.

    Given a BeautifulSoup representation of GENTOO_MIRRORS_URL, get all
    gentoo mirrors by country, or just for a specified country. We assume
    a particular HTML layout and will explode horribly if it isn't right.

    :param mirrors_soup: soupified GENTOO_MIRRORS_URL
    :type mirrors_soup: bs4.BeautifulSoup
    :param country: the only country name to return
    :type country: str
    :return: all or one gentoo mirror(s) by country
    :rtype: dict

    :Example:

    Expected HTML format of GENTOO_MIRRORS_URL:

        <p class="secthead">
            <a name="Canada"></a>
            <a name="doc_chap2_sect1">Canada</a>
        </p>
        <p>
            <a href="http://gentoo.arcticnetwork.ca/">
                Arctic Network Mirrors (http)
            </a>
            <br>
            <a href="http://gentoo.gossamerhost.com">
                Gossamer Threads (http)
            </a>
            ...
        </p>
        <p class="secthead">
            <a name="USA"></a>
            <a name="doc_chap2_sect1">Canada</a>
        </p>

    Return format:

        {'Netherlands': [
            Mirror(
                name=u'Universiteit Twente (rsync)*',
                link='rsync://ftp.snt.utwente.nl/gentoo'),
            ...
            ]
        }

    """
    mirrors_by_country = {}

    country_name = None
    for tag in mirrors_soup.find_all(True):

        try:
            tag_class = tag['class'][0]
        except (KeyError, IndexError):
            tag_class = None

        # Hit country section heading
        if tag_class == 'secthead':
            country_name = list(tag.children)[0]['name']
            mirrors_by_country[country_name] = {}
            continue

        # Hit <p> tag after our country section heading
        if country_name is not None and tag.name == 'p':

            # Get all the mirror names and links
            for child in tag.children:
                if child.name == 'a':
                    mirror_name = child.string
                    mirror_link = child['href']
                    mirrors_by_country[
                        country_name][mirror_name] = mirror_link

            if country_name == country:
                return mirrors_by_country
            else:
                # Reset country_name
                country_name = None

    return mirrors_by_country


def print_columnized_choices(items):
    """Print choices in a three-column format.

    :param items: items to print in columns of three
    :type items: list
    :return: None
    :rtype: None

    :Example:

    Input:
        [A, B, C, D, E, F, G, H, I]

    Output:
        [1] A   [4] D   [7] G
        [2] B   [5] E   [8] H
        [3] C   [6] F   [9] I

    """
    column_length, placeholders_needed = divmod(len(items), 3)
    middle_index = 2 * column_length

    items.sort()
    choices = {item: choice for choice, item in enumerate(items, 1)}
    items.extend(['' for placeholder in range(placeholders_needed)])

    columnized_rows = zip(
        items[0:column_length],
        items[column_length:middle_index],
        items[middle_index:])

    column_width = max(len(item) for item in items) + COLUMN_PADDING
    for row in columnized_rows:
        print "".join([
            '%s %s' % (
                _format_choice(choices[item], column_length),
                item.ljust(column_width))
            for item in row])

    return choices


def print_choices(items):
    """Print choices in a one-column format.

    :param items: items to print in a single column
    :type items: list
    :return: None
    :rtype: None

    :Example:

    Input:
        [A, B, C, D, E, F, G, H, I]

    Output:
        [1] A
        [2] B
        [3] C
        [4] D
        [5] E
        [6] F
        [7] G
        [8] H
        [9] I

    """
    items.sort()
    choices = {item: choice for choice, item in enumerate(items, 1)}
    column_length = len(choices)

    for item in items:
        print "".join(['%s %s' % (
            _format_choice(choices[item], column_length), item)])

    return choices


def _format_choice(choice, choices_per_column=None):
    """Format a choice so that columns always line up.

    :param choice: a choice (e.g. 1, 2, 3)
    :type choice: int
    :param choices_per_column: number of choices in each column
    :type choices_per_column: int
    :return: formatted str [ %s] | [%s]
    :rtype: str

    """
    if choice < 10 and choices_per_column >= 10:
        choice_format = "[ %s]"
    else:
        choice_format = "[%s]"

    return choice_format % str(choice)


def get_user_choice(prompt, choices):
    """Prompt user for a choice and ensure user input is valid.

    Input for a choice will always be presented as an integer. Prompt the
    user until valid input is received.

    :param prompt: message to prompt the user with
    :type prompt: str
    :param valid_choices: valid choices a user can make
    :type valid_choices: dict
    :return: valid user choice
    :rtype: int

    """
    valid_choices = choices.values()

    while True:
        try:
            choice = int(raw_input(prompt))
            assert choice in valid_choices
        except (ValueError, AssertionError):
            continue
        else:
            break

    return get_choice_value(choice, choices)


def get_choice_value(user_choice, choices):
    """Get value associated with user choice.

    :param user_choice: valid user choice
    :type user_choice: int
    :param choices: valid choices a user can make
    :type choices: dict
    :return: choice
    :rtype: int

    """
    choice_value = None
    for name, choice in choices.iteritems():
        choice_value = name if user_choice == choice else choice_value

    return choice_value


def get_media_file_url(folder_url, file_regex):
    """Get the path to gentoo media.

    :param folder_url: gentoo media folder url
    :type folder_url: str
    :param file_regex: regex to match media file
    :type file_regex: str
    :return: url path to the specified media
    :rtype: str

    """
    links = soupify(folder_url).find_all(href=re.compile(file_regex))
    try:
        # Use -1 index to avoid image links
        return os.path.join(folder_url, links[-1]['href'])
    except (IndexError, KeyError):
        raise RuntimeError("Gentoo media file not found in %s" % folder_url)


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


def main():
    """Control the download of a gentoo installation media.

    :return: exit code 0 (success) | >0 (failure)
    :rtype: int

    """
    with open('mirrors.xml') as response:
        mirrors_soup = BeautifulSoup(response.read())

    try:
        #GENTOO_MIRRORS = get_gentoo_mirrors_by_country(
        #    soupify(GENTOO_MIRRORS_URL))
        GENTOO_MIRRORS = get_gentoo_mirrors_by_country(mirrors_soup)
    except Exception:
        raise ("Could NOT parse %s." % GENTOO_MIRRORS_URL)

    print "\nGENTOO DOWNLOAD\n"

    # SELECT AN ARCHITECTURE
    arch_choices = print_choices(SUPPORTED_ARCH.keys())
    arch = get_user_choice(
        "\nSELECT ARCHITECTURE (e.g. 1 for amd64/x86_64): ", arch_choices)
    arch = SUPPORTED_ARCH[arch]

    # SELECT A COUNTRY
    country_choices = print_columnized_choices(GENTOO_MIRRORS.keys())
    country = get_user_choice(
        "\nSELECT COUNTRY (e.g. 29 for USA): ", country_choices)

    print

    # SELECT A MIRROR
    mirrors = GENTOO_MIRRORS[country]
    mirror_choices = print_choices(mirrors.keys())
    mirror = get_user_choice(
        "\nSELECT MIRROR (Note: * indicates mirrors that support IPv6): ",
        mirror_choices)

    print

    # SELECT AN INSTALLATION MEDIA
    media_choices = print_choices(GENTOO_MEDIA.keys())
    media = get_user_choice("\nSELECT INSTALLATION MEDIA: ", media_choices)
    media = getattr(arch, GENTOO_MEDIA[media])

    media_folder_and_regex = os.path.join(
        mirrors[mirror], GENTOO_RELEASES_TEMPLATE % (arch.name, media))[:-1]
    media_url = get_media_file_url(*media_folder_and_regex.split('::'))
    print media_url

    # DOWNLOAD THE MEDIA FILE

    return 0


if __name__ == '__main__':
    sys.exit(main())
