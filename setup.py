#!/usr/bin/env python
import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def get_version():
    try:
        s = read('sanic_validation', '__init__.py')
        return re.findall(r"^__version__ = '([^']+)'\r?$", s, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


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
    setup_requires=['pytest-runner', 'pytest-flake8'],
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
