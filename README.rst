Gensystem
=========

.. image:: https://coveralls.io/repos/brenj/gensystem/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/brenj/gensystem?branch=master

.. image:: https://img.shields.io/travis/brenj/gensystem/master.svg
    :target: https://travis-ci.org/brenj/gensystem

Tool for downloading and installing `Gentoo Linux <http://www.gentoo.org>`_.

Quick start
-----------
To start using gensystem:

* ``git clone https://github.com/brenj/gensystem.git && cd gensystem``
* ``pip install -r requirements.txt``
* ``python setup.py install``
* ``gensystem --help``

Configuration
-------------

All configuration is accomplished by environmental variables.
The following variables are available:

GEOIP_FILE
  File path for the GeoIP.dat file used by pygeoip.
  Use the *--exclude-geoip* install option to exclude GeoIP installation
  (e.g. python setup.py install --exclude-geoip).

Usage
-----
Gensystem is a command-line tool used to simplify the installation of a
Gentoo Linux system, including the download of installation media. There are
two (mutually exclusive) download usage-paths, one interactive and the other
non-interactive.

Here are some ``download`` usage examples:

* ``gensystem download -i``
     Download interactively (make ALL choices manually via the command line).
     Choices include: platform, media, country, and mirror.
* ``gensystem download -f stage3``
     Download latest stage3 tarball with no interaction. Choices for platform,
     country, and mirror will be made automatically based on defaults and on
     the location of the machine using ``gensystem``.
* ``gensystem download -f stage3 --select-mirror``
     Download latest stage3 tarball, but manually select a mirror. Given the
     choice of mirror is determined randomly from mirrors available in your
     country, selecting a mirror manually will likely yield the fastest
     download speed.
* ``gensystem download -f minimal -m http://www.gtlib.gatech.edu/pub/gentoo/``
     Download latest minimal iso from the Georgia Tech mirror.

Please note that ``install`` functionality is not yet implemented. This
functionality will be added in future months.
