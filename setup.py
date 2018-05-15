#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='sanic-validation',
    version='0.1.0',
    description='Validation for sanic endpoints',
    url='https://github.com/piotrb5e3/sanic-validation',
    author='Piotr Bakalarski',
    author_email='piotrb5e3@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    install_requires=[
        'sanic',
        'cerberus',
    ],
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
        'Programming Language :: Python :: 3.7',
    ],
)
