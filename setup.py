#!/usr/bin/env python
import os
import re
import codecs
from setuptools import setup, find_packages
from pygit2 import Repository

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def get_version_string():
    try:
        s = read('sanic_validation', '__init__.py')
        return re.findall(r"^__version__ = '([^']+)'\r?$", s, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_version():
    repo = Repository('.')
    branch_name = repo.head.shorthand
    commit_hash = repo.head.hex
    version_suffix = '-devel-' + commit_hash if branch_name != 'master' else ''

    version_string = get_version_string()

    return version_string + version_suffix


setup(
    name='sanic-validation',
    version=get_version(),
    description='Validation for sanic endpoints',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/piotrb5e3/sanic-validation',
    author='Piotr Bakalarski',
    author_email='piotrb5e3@gmail.com',
    license='GPLv3',
    install_requires=['sanic>=0.6.0', 'cerberus'],
    setup_requires=['pytest-runner', 'pytest-flake8', 'pygit2'],
    tests_require=['pytest', 'aiohttp', 'flake8'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
