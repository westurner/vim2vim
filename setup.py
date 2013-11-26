#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='vim2vim',
    version='0.1.0',
    description='Utility for working with vim colorschemes.',
    long_description=readme + '\n\n' + history,
    author='Wes Turner',
    author_email='https://github.com/westurner',
    url='https://github.com/westurner/vim2vim',
    packages=[
        'vim2vim',
    ],
    package_dir={'vim2vim': 'vim2vim'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='vim2vim',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    entry_points="""
    [console_scripts]
    vim2vim = vim2vim.vim2vim:main
    """
)
