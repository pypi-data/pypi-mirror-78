#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from version import __version__
#
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

exec(open('version.py').read())


setup(
    name="notifator",
    description="Automatically created environment for python package",
    author="jaromrax",
    author_email="jaromrax@gmail.com",
    license="GPL2",
    version=__version__,
    packages=find_packages(),
    package_data={'notifator': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/notifator'],
    install_requires = ['numpy==1.16.2'],
)
#
#   To RECOVER AND ACCESS THE Data later in module: :
#  X DATA_PATH = pkg_resources.resource_filename('notifator', 'data/')
#  X DB_FILE =   pkg_resources.resource_filename('notifator', 'data/file')
#   DB_FILE = pkg_resources.resource_filename(
#       pkg_resources.Requirement.parse('nuphy2'),
#       'data/nubase2016.txt'
#   )
#   pip install -e .
#   bumpversion patch minor major release
#      release needed for pypi
