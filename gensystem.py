#!/usr/bin/env python
# encoding: utf-8

"""Control download and/or install of Gentoo Linux."""

import os
import sys

import gensystem.arch as arch
import gensystem.media as media
import gensystem.mirror as mirror

COLUMN_PADDING = 3


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


def download_interactively():
    """Download Gentoo installation media by prompting user for choices.

    :returns: None
    :rtype: None

    """
    print "\nGENTOO DOWNLOAD\n"

    # SELECT AN ARCHITECTURE
    arch_choices = print_choices(arch.SUPPORTED_ARCH.keys())
    arch_chosen = get_user_choice(
        "\nSELECT ARCHITECTURE (e.g. 1 for amd64/x86_64): ", arch_choices)
    arch_chosen = arch.SUPPORTED_ARCH[arch_chosen]

    # SELECT A COUNTRY
    country_choices = print_columnized_choices(mirror.GENTOO_MIRRORS.keys())
    country = get_user_choice(
        "\nSELECT COUNTRY (e.g. 29 for USA): ", country_choices)

    print

    # SELECT A MIRROR
    mirrors = mirror.GENTOO_MIRRORS[country]
    mirror_choices = print_choices(mirrors.keys())
    mirror_chosen = get_user_choice(
        "\nSELECT MIRROR (Note: * indicates mirrors that support IPv6): ",
        mirror_choices)

    print

    # SELECT AN INSTALLATION MEDIA
    media_choices = print_choices(media.GENTOO_MEDIA.keys())
    media_chosen = get_user_choice(
        "\nSELECT INSTALLATION MEDIA: ",
        media_choices)
    media_chosen = getattr(arch_chosen, media.GENTOO_MEDIA[media_chosen])

    releases_url = mirror.GENTOO_RELEASES_TEMPLATE % (
        arch_chosen.name, media_chosen)
    media_folder_and_regex = os.path.join(
        mirrors[mirror_chosen], releases_url[:-1])
    media_url = media.get_media_file_url(*media_folder_and_regex.split('::'))
    print media_url

    # DOWNLOAD THE MEDIA FILE


def main():
    """Control the download of a gentoo installation media.

    :return: exit code 0 (success) | >0 (failure)
    :rtype: int

    """
    download_interactively()
    return 0


if __name__ == '__main__':
    sys.exit(main())
