# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
#

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, "../..")

import whatsbyapi  # noqa: E402

# -- Project information -----------------------------------------------------

project = "whatsbyapi"
copyright = f"{date.today().year}, David Lev"
author = "David Lev"

version = whatsbyapi.__version__
release = whatsbyapi.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxext.opengraph",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_togglebutton",
    "sphinx.ext.autosectionlabel",
    "m2r",
]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []
pygments_style = "friendly"
html_theme = "sphinx_book_theme"
suppress_warnings = ["image.not_readable"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["../static"]
html_favicon = "favicon.ico"

# sphinx.ext.autodoc
autodoc_member_order = "bysource"
# autodoc_typehints = "none"  # show type hints in doc signature
# autodoc_typehints = "description"  # show type hints in doc body instead of signature

# sphinx.ext.napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_ivar = True

# sphinx-copybutton
copybutton_prompt_text = (
    r">>> |\.\.\. |> |\$ |\# | In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True

# sphinx_book_theme
html_theme_options = {
    "use_sidenotes": True,
    "repository_url": "https://github.com/abdelhak-zaaim/whatsbyapi",
    "repository_branch": "master",
    "path_to_docs": "docs/source",
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_issues_button": True,
    "use_source_button": True,
    "logo": {
        "text": "whatsbyapi",
        "link": "https://whatsbyapi.readthedocs.io/",
        "alt_text": "whatsbyapi logo",
        "image_light": "whatsbyapi-logo.png",
        "image_dark": "whatsbyapi-logo.png",
    },
    "icon_links_label": "Quick Links",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/abdelhak-zaaim/whatsbyapi",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/whatsbyapi/",
            "icon": "fab fa-python",
        },
        {
            "name": "Updates",
            "url": "https://t.me/py_wa",
            "icon": "fa-solid fa-bullhorn",
        },
        {
            "name": "Chat",
            "url": "https://t.me/whatsbyapichat",
            "icon": "fa-solid fa-comment-dots",
        },
        {
            "name": "Issues",
            "url": "https://github.com/abdelhak-zaaim/whatsbyapi/issues",
            "icon": "fas fa-bug",
        },
    ],
    "use_download_button": True,
}

# sphinx.ext.intersphinx
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# sphinxext.opengraph
ogp_site_url = "https://whatsbyapi.readthedocs.io/"
ogp_site_name = "whatsbyapi Documentation"
ogp_image = "https://whatsbyapi.readthedocs.io/en/latest/_static/whatsbyapi-ogp.png"
ogp_image_alt = "whatsbyapi Logo"
ogp_description_length = 300
ogp_type = "website"

html_extra_path = ["google898e98a538257a96.html"]

# sphinx.ext.todo
todo_include_todos = True
