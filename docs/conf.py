"""Sphinx configuration for RobotFrameworkPGP documentation."""

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'RobotFrameworkPGP'
copyright = '2024, Robot Framework PGP Contributors'
author = 'Robot Framework PGP Contributors'
release = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = None
html_favicon = None

# Extension configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'robotframework': ('https://robot-framework.readthedocs.io/en/master/', None),
}

# Add any paths that contain custom static files (such as style sheets)
html_css_files = []

# The master toctree document
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use
pygments_style = 'sphinx'