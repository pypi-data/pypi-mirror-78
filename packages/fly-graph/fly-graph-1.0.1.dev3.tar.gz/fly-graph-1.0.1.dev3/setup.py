#! python3
# -*- coding: utf-8 -*-

# Credits: github.com/navdeep-G/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev
"""
setup.py for human
"""

import io
import os
import sys
from shutil import rmtree

from setuptools import find_namespace_packages, setup

# Package meta-data
NAME = 'fly-graph'
DESCRIPTION = 'A graph library for FLY language, written in Python'
URL = 'https://github.com/bissim/FLY-graph'
EMAIL = 's.bisogno90@gmail.com'
AUTHOR = 'Simone Bisogno'
REQUIRES_PYTHON = '~=3.6'

# Required packages
REQUIRED = [
    'networkx'
]

# Optional packages
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

HERE = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION
f.close()
del f

PARENT = os.path.dirname(HERE)

# Import the VERSION and use it as the version
with io.open(os.path.join(PARENT, 'VERSION'), encoding='utf-8') as f:
    VERSION = f.readline().rstrip('\n')
f.close()
del f

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_namespace_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Other",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='FLY graph management',
    project_urls={
        'Source': 'https://github.com/bissim/FLY-graph',
        'Tracker': 'https://github.com/bissim/FLY-graph/issues'
    },
)
