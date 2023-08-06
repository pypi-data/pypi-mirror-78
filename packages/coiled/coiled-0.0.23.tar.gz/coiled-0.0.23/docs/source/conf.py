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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "Coiled"
copyright = "2020, Coiled Computing Inc."
author = "Coiled"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_panels",
    "sphinx_click.ext",
]
autosummary_generate = True
panels_add_boostrap_css = False
copybutton_prompt_text = "$ "

intersphinx_mapping = {
    "distributed": ("https://distributed.dask.org/en/latest/", None),
    "dask_kubernetes": ("https://kubernetes.dask.org/en/latest/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo-horizontal.svg"

html_theme_options = {
    "github_url": "https://github.com/coiled",
    "twitter_url": "https://twitter.com/CoiledHQ",
    "show_prev_next": True,
    "external_links": [
        {"name": "Coiled.io", "url": "https://coiled.io/"},
        {"name": "Sign in", "url": "https://beta.coiled.io/accounts/login/"},
        {
            "name": "Feedback",
            "url": "https://github.com/coiled/coiled-issues/issues/new",
        },
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def setup(app):
    app.add_stylesheet("custom.css")
