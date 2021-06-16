#!/usr/bin/env python

from setuptools import setup
import sys
import os

install_requires = [
    'beautifulsoup4',
    'requests',
    'python-dateutil'
    ]

test_requires = [
    'nose',
    'mock'
    ]

suggested = {
        }

setup(name='python-autocite',
    version='0.0.3',
    description='Scrape webpages and generate citations',
    author='Nate Levesque',
    author_email='public@thenaterhood.com',
    url='https://github.com/thenaterhood/python-autocite/archive/master.zip',
    install_requires=install_requires,
    tests_require=test_requires,
    test_suite='nose.collector',
    package_dir={'':'src'},
    package_data={
    },
    entry_points={
        'console_scripts': [
            'autocite = python_autocite.__main__:main',
            ]
    },
    packages=[
        'python_autocite',
        'python_autocite.lib'
        ],
    )
