# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'FedTools'
AUTHOR = 'David Woroniuk'
AUTHOR_EMAIL = 'david.j.woroniuk@durham.ac.uk'
URL = 'https://github.com/David-Woroniuk/FedTools'

LICENSE = 'MIT License'
DESCRIPTION = 'An open source library for the extraction of Federal Reserve Data.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'bs4',
      'pandas',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )