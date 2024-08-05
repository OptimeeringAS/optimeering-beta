# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os

# This resloves the /src directory and adds to the python path so sphinx can find optimeering.client etc.
import pathlib
import sys

sys.path.insert(0, pathlib.Path(__file__).parents[3].resolve().as_posix())


from optimeering_beta import __version__

version = "v" + __version__.split(".")[0]

project = "Beta Python SDK"
copyright = "2024, Optimeering AS"
author = "Scott Melhop"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosectionlabel"]

templates_path = ["_templates"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "logo_transparent.svg"
html_favicon = "favicon.ico"

html_js_files = [
    "js/versions.js",
]


autodoc_typehints = "none"
