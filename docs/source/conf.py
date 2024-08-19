# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import toml
pyproject = toml.load("../../pyproject.toml")

project = pyproject["tool"]["poetry"]["description"]
copyright = "2024, Optimeering AS"
author = pyproject["tool"]["poetry"]["authors"][0]
release = pyproject["tool"]["poetry"]["version"]

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
