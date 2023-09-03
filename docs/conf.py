"""Sphinx configuration."""
project = "SaturnScrape"
author = "Parker Wahle"
copyright = "2023, Parker Wahle"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
