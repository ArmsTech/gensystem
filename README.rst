Gensystem
=========

.. image:: https://coveralls.io/repos/ArmsTech/gensystem/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ArmsTech/gensystem?branch=master

.. image:: https://img.shields.io/travis/ArmsTech/gensystem/master.svg
    :target: https://travis-ci.org/ArmsTech/gensystem

Tool for downloading and installing `Gentoo Linux <http://www.gentoo.org>`_.

Quick start
-----------
To start using gensystem:

* git clone ``https://github.com/ArmsTech/gensystem.git`` && cd gensystem
* pip install -r requirements.txt
* python setup.py install
* gensystem --help

.. include:: CONFIGURATION.rst (Hopefully directives will be supported on Github one day.)
Configuration
-------------

All configuration is accomplished by environmental variables.
The following variables are available:

GEOIP_FILE
  File path for the GeoIP.bat file used by pygeoip.
  Use the *--exclude-geoip* install option to exclude GeoIP installation
  (e.g. python setup.py install --exclude-geoip).

