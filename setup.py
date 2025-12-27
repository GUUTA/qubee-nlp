#!/usr/bin/env python3
"""
Setup script for Qubee NLP package.

This file is maintained for compatibility with older build tools.
Modern builds should use pyproject.toml.
"""

import os
import re
from pathlib import Path

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Static version - removed dynamic version reading
VERSION = "0.1.0"

def get_requirements(filename="requirements.txt"):
    """Read requirements from file."""
    requirements = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                requirements.append(line)
    return requirements


setup(
    name="qubee-nlp",
    version=VERSION,  # Use static version
    author="Qubee NLP Team",
    author_email="contact@qubeenlp.org",
    maintainer="Afaan Oromoo NLP Community",
    maintainer_email="community@qubeenlp.org",
    description="Natural Language Processing tools for Afaan Oromoo (Oromo language) using Qubee script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afaanoromoo/qubee-nlp",
    project_urls={
        "Homepage": "https://github.com/afaanoromoo/qubee-nlp",
        "Documentation": "https://qubee-nlp.readthedocs.io",
        "Repository": "https://github.com/afaanoromoo/qubee-nlp",
        "Changelog": "https://github.com/afaanoromoo/qubee-nlp/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/afaanoromoo/qubee-nlp/issues",
        "Discussions": "https://github.com/afaanoromoo/qubee-nlp/discussions",
        "Funding - Open Collective": "https://opencollective.com/qubee-nlp",
        "Funding - GitHub Sponsors": "https://github.com/sponsors/afaanoromoo",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Oromo",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "qubee_nlp": [
            "corpus/*.txt",
            "data/*.json",
            "py.typed",
        ]
    },
    python_requires=">=3.7",
    install_requires=get_requirements("requirements.txt"),
    extras_require={
        "dev": get_requirements("requirements-dev.txt"),
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.0.0",
            "myst-parser>=2.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xdist>=3.0.0",
            "pytest-mock>=3.0.0",
            "hypothesis>=6.0.0",
        ],
        "full": [
            "numpy>=1.21.0",
            "scikit-learn>=1.0.0",
            "pandas>=1.3.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "requests>=2.28.0",
            "tqdm>=4.64.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qubee-nlp=qubee_nlp.cli:main",
        ],
        "qubee_nlp.plugins": [
            "alphabet=qubee_nlp.alphabet:QubeeAlphabet",
            "tokenizer=qubee_nlp.tokenizer:QubeeTokenizer",
            "stemmer=qubee_nlp.stemmer:QubeeStemmer",
        ],
    },
    zip_safe=False,
)