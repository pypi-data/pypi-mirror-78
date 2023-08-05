#!/usr/bin/env python
# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import sys

# 3rd party
from setuptools import setup

sys.path.append('.')

# this package
from __pkginfo__ import *  # pylint: disable=wildcard-import



setup(
		description='Customised "sphinx_rtd_theme" used by my Python projects.',
		extras_require=extras_require,
		install_requires=install_requires,
		py_modules=[],
		version=__version__,
		entry_points={"sphinx.html_themes": ["domdf_sphinx_theme = domdf_sphinx_theme"]},
		)
