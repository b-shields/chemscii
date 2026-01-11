[![CI](https://github.com/b-shields/chemscii/actions/workflows/ci.yml/badge.svg)](https://github.com/b-shields/chemscii/actions/workflows/ci.yml)

# chemscii

A Python package for rendering chemical structures as ASCII/Unicode art, optimized for display in LLM terminal interfaces and text-based environments.

Core Objectives:
- Parse common chemical structure formats (SMILES, SDF)
- Render 2D chemical structures as text-based visualizations
- Provide clean, readable output suitable for terminal display

## Installation

```bash
pip install chemscii
```

## Development

Build environment.
```bash
conda env create -f environment.yml
conda activate chemscii
```

Install `chemscii`.
```bash
poetry install
pre-commit install
```

## Package Structure

```bash
chemscii/
├── src/
│   └── chemscii/
│       ├── __init__.py
│       ├── parsers/         # Input format parsers
│       │   ├── __init__.py
│       │   ├── molecule.py  # SMILES and SDF formats
│       │   ├── name.py      # Molecule name to SMILES
│       │   └── chembl.py    # ChEMBL ID to SMILES
│       ├── layout/          # 2D coordinate generation
│       │   ├── __init__.py
│       │   ├── atoms.py     # Atoms
│       │   └── bonds.py     # Bonds
│       ├── renderers/       # Text rendering engines
│       │   ├── __init__.py
│       │   ├── ascii.py     # Basic ASCII renderer
│       │   └── unicode.py   # Enhanced Unicode renderer
│       └── cli.py           # Command-line interface built with rich
├── tests/
│   ├── __init__.py
│   ├── test_parsers.py
│   ├── test_layout.py
│   ├── test_renderers.py
│   └── fixtures/            # Test molecule SMILES and SDF
└── examples/
    ├── basic_usage.py
    └── claude_integration.py
```
