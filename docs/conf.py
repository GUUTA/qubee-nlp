import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # project root relative to source/

# -- Project information -----------------------------------------------------
project = 'qubee-nlp'
author = 'Guta Tesema Tufa'
copyright = '2025, Guta Tesema Tufa'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
