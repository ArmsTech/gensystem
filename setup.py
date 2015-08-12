#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import gzip
import os
import setuptools
from setuptools.command.install import install
import tempfile
import shutil
import urllib

import gensystem


SETUP_DIR = os.path.dirname(os.path.realpath(__file__))
GEOIP_URL = ('http://geolite.maxmind.com/download/geoip/'
             'database/GeoLiteCountry/GeoIP.dat.gz')

README = open(os.path.join(SETUP_DIR, 'README.rst')).read()
HISTORY = open(
    os.path.join(SETUP_DIR, 'HISTORY.rst')).read().replace(
    '.. :changelog:', '')
CLASSIFIERS = [
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities']


def add_requirement(line, requirements):
    """Add requirement to requirements lists.

    Args:
        line (str): A line in a requirements.txt file.
        requirements (list): Requirements for gensystem.

    """
    line = line.strip()
    if not line or line.startswith('#'):
        pass  # Ignore comments and blank lines
    else:
        requirements.append(line)

requirements = []
with open(os.path.join(SETUP_DIR, 'requirements.txt'), 'r') as file_:
    for line in file_:
        add_requirement(line, requirements)

test_requirements = []
with open(os.path.join(SETUP_DIR, 'test_requirements.txt'), 'r') as file_:
    for line in file_:
        add_requirement(line, test_requirements)


class InstallWithGeoIP(install):
    """Install GeoIP after setup install operations."""

    user_options = install.user_options + [
        ('no-geoip', None, "Do not install GeoIP with gensystem.")]

    boolean_options = install.boolean_options + ['no-geoip']

    def initialize_options(self):
        install.initialize_options(self)
        self.no_geoip = None

    def run(self):
        install.run(self)

        # Install GeoIP unless a dry run or user doesn't want it
        if not self.dry_run and not self.no_geoip:
            geoip_dir = tempfile.mkdtemp()
            zip_path = os.path.join(geoip_dir, 'GeoIP.dat')

            with gzip.open(zip_path, 'wb') as geoip_zip:
                geoip_zip.writelines(urllib.urlopen(GEOIP_URL).readlines())

            shutil.move(
                zip_path, os.path.join(self.build_lib, 'gensystem', 'data'))


setuptools.setup(
    cmdclass={'install': InstallWithGeoIP},
    name='gensystem',
    license='GPLv3',
    version=gensystem.__version__,
    description='Tool for downloading and installing Gentoo Linux.',
    long_description='\n\n'.join([README, HISTORY]),
    author=gensystem.__author__,
    author_email=gensystem.__email__,
    url='https://github.com/ArmsTech/gensystem',
    packages=setuptools.find_packages(),
    package_dir={'gensystem': 'gensystem'},
    scripts=glob.glob('bin/*'),
    install_requires=requirements,
    zip_safe=False,
    keywords='gensystem',
    classifiers=CLASSIFIERS,
    test_suite='gensystem.tests',
    tests_require=test_requirements
)
