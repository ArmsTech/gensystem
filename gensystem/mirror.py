"""Collect Gentoo mirrors from gentoo.org."""

from urlparse import urlparse

from bs4 import BeautifulSoup

GENTOO_MIRRORS = {}
GENTOO_MIRRORS_URL = 'http://www.gentoo.org/main/en/mirrors.xml'
GENTOO_RELEASES_TEMPLATE = 'releases/%s/autobuilds/%s/'

SUPPORTED_COUNTRIES = [
    'CA', 'US', 'AR', 'BR', 'AT', 'BG', 'CZ', 'FI', 'FR', 'DE', 'GR', 'IE',
    'NL', 'PL', 'PT', 'RO', 'SE', 'SK', 'ES', 'CH', 'TR', 'UA', 'UK', 'AU',
    'CN', 'HK', 'JP', 'KR', 'RU', 'TW', 'IL', 'KZ']


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
                <a href="http://gentoo..."><code>http://gentoo...</code></a>
            </td>
        </tr>
        ...
        <h3 id="US">US &ndash; USA</h3>
        ...

    Return format:

        {'Netherlands':
            {u'LeaseWeb (ftp)': u'ftp://mirror.leaseweb.com/gentoo/',
             u'LeaseWeb (http)': u'http://mirror.leaseweb.com/gentoo/',
            ...
            }
         ...
        }

    """
    mirrors_by_country = {}

    country_name = None
    for tag in mirrors_soup.find_all(True):

        if tag.name == 'h3' and tag.get('id') in SUPPORTED_COUNTRIES:
            # Assumes format "ID SEPARATOR COUNTRY" e.g. (CA - Canada)
            country_name = tag.string.split()[2]
            mirrors_by_country[country_name] = {}
            continue

        # Hit <table> tag after our country section heading
        if country_name is not None and tag.name == 'table':

            # Get all the mirror names and links in table
            for descendant in tag.descendants:
                # Assumes the name column spans rows
                if descendant.name == 'td' and descendant.get('rowspan'):
                    mirror_name = descendant.string
                if descendant.name == 'a':
                    mirror_link = descendant['href']
                    name_with_protocol = '%s (%s)' % (
                        mirror_name, urlparse(mirror_link).scheme)
                    mirrors_by_country[
                        country_name][name_with_protocol] = mirror_link

            if country_name == country:
                return mirrors_by_country
            else:
                # Reset country_name
                country_name = None

    return mirrors_by_country

with open('gensystem/mirrors.xml') as response:
    mirrors_soup = BeautifulSoup(response.read())
    GENTOO_MIRRORS = get_gentoo_mirrors_by_country(mirrors_soup)

#try:
#    #GENTOO_MIRRORS = get_gentoo_mirrors_by_country(
#    #    soupify(GENTOO_MIRRORS_URL))
#    GENTOO_MIRRORS = get_gentoo_mirrors_by_country(mirrors_soup)
#except Exception:
#    raise ("Could NOT parse %s." % GENTOO_MIRRORS_URL)
