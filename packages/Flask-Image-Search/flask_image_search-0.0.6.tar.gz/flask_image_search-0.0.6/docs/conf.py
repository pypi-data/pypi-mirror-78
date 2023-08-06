# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from pallets_sphinx_themes import ProjectLink
from pallets_sphinx_themes import get_version

# Project --------------------------------------------------------------

project = "Flask-Image-Search"
copyright = "2020 Hanan Fokkens"
author = "Hanan Fokkens"

release, version = get_version("flask_image_search")

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "pallets_sphinx_themes"
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "flask": ("http://flask.pocoo.org/docs/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/latest/", None),
    "flask_sqlalchemy": ("https://flask-sqlalchemy.palletsprojects.com/", None),
    "pillow": ("https://pillow.readthedocs.io/en/latest", None),
}

# HTML -----------------------------------------------------------------

html_theme = "flask"
html_context = {
    "project_links": [
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask-Image-Search/"),
        ProjectLink("Source Code", "https://github.com/hananf11/flask_image_search"),
        ProjectLink("Issue Tracker", "https://github.com/hananf11/flask_image_search/issues"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
html_static_path = ["_static"]
html_css_files = ["sticky.css"]
html_show_sourcelink = True
