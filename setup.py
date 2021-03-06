#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install
except:
    sys.exit("Error: missing python-setuptools library")

try:
    python_version = sys.version_info
except:
    python_version = (1, 5)
if python_version < (2, 7):
    sys.exit(
        "This application currently requires a minimum Python 2.7.x or 3.x"
        "Please update your Python version."
    )

from alignak_app import __description__, __version__, __license__, __author__, __project_url__
from alignak_app import __name__ as __pkg_name__

# Requirements
install_requires = [
    'alignak_backend_client',
    'configParser',
]

# Define paths
paths = {}
if 'linux' in sys.platform or\
        'sunos5' in sys.platform or\
        'bsd' in sys.platform:
    paths = {
        'app': __pkg_name__,
        'images': __pkg_name__ + '/images',
        'css': __pkg_name__ + '/css',
        'templates': __pkg_name__ + '/templates',
        'bin': __pkg_name__ + '/bin',
    }
elif 'win32' in sys.platform:
    paths = {
        'app': __pkg_name__,
        'images': __pkg_name__ + '/images',
        'css': __pkg_name__ + '/css',
        'templates': __pkg_name__ + '/templates',
        'bin': __pkg_name__ + '/bin',
    }
else:
    print("Unsupported platform, sorry!")
    exit(1)

# Fill [data_files]
dir_path = os.path.dirname(os.path.realpath(__file__))
data_files = []

# Images
images = os.listdir(dir_path + '/etc/images')
for image in images:
    data_files.append((paths['images'], ['etc/images/' + image]))

# StyleSheet
stylesheet = os.listdir(dir_path + '/etc/css')
for style in stylesheet:
    data_files.append((paths['css'], ['etc/css/' + style]))

# Etc
data_files.append((paths['app'], ['etc/settings.cfg']))
data_files.append((paths['app'], ['etc/app_workdir.ini']))
data_files.append((paths['app'], ['etc/images.ini']))

# Bin for Unix
data_files.append((paths['bin'], ['bin/unix/alignak-app']))
data_files.append((paths['bin'], ['bin/unix/alignak-app.py']))


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    END = '\x1b[0m'
    GREEN = '\x1b[32m'
    CYAN = '\x1b[36m'

    install_info = """\n
#########################################################################

        %s Alignak-App has been installed successfully :) %s
        
Please RUN %s ~/.local/alignak_app/bin/alignak-app %s to check installation.

    Usage: %s alignak-app {start|stop|status|restart} %s

#########################################################################\n
    """ % (GREEN, END, CYAN, END, GREEN, END)

    def run(self):
        install.run(self)
        os.system("echo '%s'" % self.install_info)


setup(
    name=__pkg_name__,
    version=__version__,

    license=__license__,

    # metadata for upload to PyPI
    author=__author__,
    author_email="ttamalfor@gmail.com",
    keywords="alignak applet notifier",
    url=__project_url__,
    description=__description__,
    long_description=open('README.rst').read(),

    cmdclass={
        'install': PostInstallCommand,
    },
    zip_safe=False,

    packages=find_packages(),
    include_package_data=True,

    data_files=data_files,

    install_requires=install_requires,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Desktop Environment'
    ]

)
