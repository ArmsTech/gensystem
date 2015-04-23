# -*- coding: utf-8 -*-

"""Unit tests for gensystem mirror."""

import bs4

import gensystem.mirror as gensystem_mirror

TEST_GENTOO_ORG = """
    <!DOCTYPE html>
    <html>
        <head>
        <title>Gentoo Test Mirrors – Gentoo Linux</title>
        </head>
        <body class="">
        <header>
        <h2>North America</h2>
        <h3 id="CA">CA &ndash; Canada</h3>
        <table class="table table-condensed">
          <tr>
            <th style="width: 30%;">Name</th>
            <th style="width: 10%;">Protocol</th>
            <th style="width: 10%;">IPv4/v6</th>
            <th style="width: 50%;">URL</th>
          </tr>
          <tr>
            <td rowspan="1">Arctic Network Mirrors</td>
            <td>
                <span class="label label-primary">http</span>
            </td>
            <td>
                <span class="label label-info">IPv4 only</span>
            </td>
            <td>
                <a href="http://test/canada"><code>test/canada</code></a>
            </td>
          </tr>
        </table>
        <h3 id="US">US &ndash; USA</h3>
        <table class="table table-condensed">
          <tr>
            <th style="width: 30%;">Name</th>
            <th style="width: 10%;">Protocol</th>
            <th style="width: 10%;">IPv4/v6</th>
            <th style="width: 50%;">URL</th>
          </tr>
          <tr>
            <td rowspan="1">OSU Open Source Lab</td>
            <td>
              <span class="label label-primary">http</span>
            </td>
            <td>
              <span class="label label-info">IPv4 only</span>
            </td>
            <td>
              <a href="http://test/usa"><code>test/usa</code></a>
          </tr>
        </table>
        </body>
    </html>
"""


def test_get_gentoo_mirrors_all():
    """Test get_gentoo_mirrors get all mirrors."""
    mirrors = gensystem_mirror.get_gentoo_mirrors(
        bs4.BeautifulSoup(TEST_GENTOO_ORG))
    assert mirrors == {
        u'Canada': {u'Arctic Network Mirrors (http)': u'http://test/canada'},
        u'USA': {u'OSU Open Source Lab (http)': u'http://test/usa'}}


def test_get_gentoo_mirrors_one_country():
    """Test get_gentoo_mirrors get mirrors for one country."""
    mirrors = gensystem_mirror.get_gentoo_mirrors(
        bs4.BeautifulSoup(TEST_GENTOO_ORG), country='USA')
    assert mirrors == {
        u'USA': {u'OSU Open Source Lab (http)': u'http://test/usa'}}
