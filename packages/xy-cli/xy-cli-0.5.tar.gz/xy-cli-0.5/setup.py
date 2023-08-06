#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of xy-cli.
# https://github.com/exiahuang/xy-cli

# Licensed under the Apache License 2.0:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2020, exiahuang <exia.huang@outlook.com>

import sys
from setuptools import setup, find_packages
from xy_cli import __version__
from os import path

try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print('Cannot import py2exe', file=sys.stderr)
        exit(1)

DESCRIPTION = 'xy command tools'
LONG_DESCRIPTION = '''
xy command tools
'''
# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    py2exe_console = [{
        'script': './xy_cli/__main__.py',
        'dest_base': 'xy command tools',
        'version': __version__,
        'description': DESCRIPTION,
        'comments': DESCRIPTION,
        'product_name': 'xy-cli',
        'product_version': __version__,
    }]
    py2exe_options = {
        'bundle_files': 1,
        'compressed': 1,
        'optimize': 2,
        'dist_dir': '.\\dist\\win',
        'includes': ["xy_cli", "xy_cli.commands", "xy_cli.libs"]
    }
    params = {
        'console': py2exe_console,
        'options': {
            'py2exe': py2exe_options
        },
        'zipfile': None
    }
else:
    params = {
        'long_description_content_type': 'text/markdown',
        'packages': find_packages(),
        'include_package_data': True,
        'entry_points': {
            'console_scripts': [
                # add cli scripts here in this form:
                'xy=xy_cli.__main__:main',
            ],
        }
    }

setup(
    name='xy-cli',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords='xy-cli command line',
    author='exiahuang',
    author_email='exia.huang@outlook.com',
    url='https://github.com/exiahuang/xy-cli',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'xlrd'
    ],
    extras_require={
        'tests': tests_require,
    },
    **params)
