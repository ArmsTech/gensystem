"""Unit tests for gensystem utils."""

import gensystem.utils as gensystem_utils


def test_get_choices():
    """Test get_choices."""
    test_items = ['B', 'A', 'D', 'C']

    # Sorted by default
    choices = gensystem_utils.get_choices(test_items)
    assert choices == {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    unsorted_choices = gensystem_utils.get_choices(test_items, sort=False)
    assert unsorted_choices == {'A': 2, 'B': 1, 'C': 4, 'D': 3}
