"""Install gensystem package."""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import gzip
import json
import os
import setuptools
from setuptools.command.install import install
import shutil
import urllib

import gensystem
import gensystem.mirror as gensystem_mirror
import gensystem.temp as temp


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


class InstallWithDependencies(install):

    """Install custom dependencies before normal setup install operations."""

    user_options = install.user_options + [
        ('exclude-geoip', None, "do not install GeoIP with gensystem.")]

    boolean_options = install.boolean_options + ['exclude-geoip']

    def initialize_options(self):
        """Initialize custom options."""
        install.initialize_options(self)
        self.exclude_geoip = None

    def install_geoip(self):
        """Install GeoIP dependency.

        Returns:
            bool: Whether GeoIP was installed successfully.

        """
        with temp.temp_directory() as geoip_dir:

            # Download zipped GeoIP.dat(.gz)
            geoip_dat_gz_path = os.path.join(geoip_dir, 'GeoIP.dat.gz')
            with open(geoip_dat_gz_path, 'wb') as geoip_zipped:
                geoip_zipped.writelines(
                    urllib.urlopen(GEOIP_URL).readlines())

            # Unzip and save as GeoIP.dat
            geoip_dat_path = os.path.join(geoip_dir, 'GeoIP.dat')
            with gzip.open(geoip_dat_gz_path, 'rb') as geoip_unzipped:
                with open(geoip_dat_path, 'w') as geoip_dat:
                    geoip_dat.write(geoip_unzipped.read())

            # Move dat file to build_lib path
            build_lib_path = os.path.join(self.build_lib, 'gensystem', 'data')
            shutil.move(geoip_dat_path, build_lib_path)

        return os.path.exists(os.path.join(build_lib_path, 'GeoIP.dat'))

    def install_mirrors(self):
        """Install mirrors.json dependency.

        Returns:
            bool: Whether mirrors.json was installed successfully.

        """
        try:
            mirrors = gensystem_mirror.get_mirrors_from_web()
        except Exception:
            return False  # Not installed.

        with temp.temp_directory() as mirrors_dir:
            mirrors_json_path = os.path.join(mirrors_dir, 'mirrors.json')
            with open(mirrors_json_path, 'w') as mirrors_json:
                json.dump(mirrors, mirrors_json, indent=4, sort_keys=True)
            shutil.copy(
                mirrors_json_path,
                os.path.join(self.build_lib, 'gensystem', 'data'))

        return True  # Safe to assume installed.

    def run(self):
        """Run the install, installing custom dependencies first."""
        # Make sure required dirs exist since we aren't starting install yet
        os.makedirs(os.path.join(self.build_lib, 'gensystem', 'data'), 0755)

        # Install GeoIP unless a dry run or user doesn't want it
        if not self.dry_run and not self.exclude_geoip:
            self.install_geoip()

        # Install latest mirrors.json
        self.install_mirrors()

        # Run the rest of the installer as usual
        install.run(self)


setuptools.setup(
    cmdclass={'install': InstallWithDependencies},
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
