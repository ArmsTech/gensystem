"""Utilities for dealing with Gentoo Linux and gensystem."""

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


def get_choices(items, sort=True):
    """Get choices for a given list of items.

    Args:
        items (list): items to get choices for.
        sort (bool, optional): whether to sort items.

    Returns:
        dict: choices for the specified items.
        format: {item1: 1, item2: 2, item3: 3, ...}
    """
    if sort:
        items = sorted(items)

    return {item: choice for choice, item in enumerate(items, 1)}


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
            choice = int(get_raw_input(prompt))
            assert choice in valid_choices
        except (ValueError, AssertionError):
            continue
        else:
            break

    return get_choice_value(choice, choices)


def get_raw_input(prompt):
    """Get raw input from user using raw_input.

    This function exists to wrap raw_input so that it can be mocked for
    unit testing.

    Arguments:
        prompt (str): message to prompt user with.

    Returns:
        str: raw input from user.
    """
    return raw_input(prompt)


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


def format_choice(choice, ten_or_more_choices=False):
    """Format a choice so that columns always line up.

    :param choice: a choice (e.g. 1, 2, 3)
    :type choice: int
    :param ten_or_more_choices: whether there are 10 or more choices
    :type choices_per_column: bool
    :return: formatted str [ %s] | [%s]
    :rtype: str

    """
    if choice < 10 and ten_or_more_choices:
        choice_format = "[ %s]"
    else:
        choice_format = "[%s]"

    return choice_format % str(choice)
