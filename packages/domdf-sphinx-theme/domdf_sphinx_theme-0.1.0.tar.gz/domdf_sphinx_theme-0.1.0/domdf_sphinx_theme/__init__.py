#!/usr/bin/env python3
#
#  __init__.py
"""
Customised "sphinx_rtd_theme" used by my Python projects.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import os.path

# 3rd party
import sphinx_rtd_theme  # type: ignore
from sphinx.application import Sphinx

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

__version_full__ = __version__

__all__ = ["setup"]


def setup(app: Sphinx):
	"""
	Setup Sphinx extension.

	:param:
	"""

	# add_html_theme is new in Sphinx 1.6+
	sphinx_rtd_theme.setup(app)

	if hasattr(app, "add_html_theme"):
		theme_path = os.path.abspath(os.path.dirname(__file__))
		app.add_html_theme("domdf_sphinx_theme", theme_path)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}
