"""Manage Gentoo Linux mirrors."""

from bs4 import BeautifulSoup

GENTOO_MIRRORS = {}
GENTOO_MIRRORS_URL = 'http://www.gentoo.org/main/en/mirrors.xml'
GENTOO_RELEASES_TEMPLATE = 'releases/%s/autobuilds/%s/'


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

with open('gensystem/mirrors.xml') as response:
    mirrors_soup = BeautifulSoup(response.read())
    GENTOO_MIRRORS = get_gentoo_mirrors_by_country(mirrors_soup)

#try:
#    #GENTOO_MIRRORS = get_gentoo_mirrors_by_country(
#    #    soupify(GENTOO_MIRRORS_URL))
#    GENTOO_MIRRORS = get_gentoo_mirrors_by_country(mirrors_soup)
#except Exception:
#    raise ("Could NOT parse %s." % GENTOO_MIRRORS_URL)
