# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import re

# This resloves the /src directory and adds to the python path so sphinx can find optimeering.client etc.
import pathlib
import sys

sys.path.insert(0, pathlib.Path(__file__).parents[3].resolve().as_posix())

version = re.search(r'^__version__\s*=\s*"(.*)"', open("../../optimeering_beta/__init__.py").read(), re.M).group(1)

project = "Beta Python SDK"
copyright = "2024, Optimeering AS"
author = "Scott Melhop"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosectionlabel"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "logo_transparent.svg"
html_favicon = "favicon.ico"

autodoc_typehints = "none"
