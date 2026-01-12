[![CI](https://github.com/b-shields/chemscii/actions/workflows/ci.yml/badge.svg)](https://github.com/b-shields/chemscii/actions/workflows/ci.yml)

# chemscii

A Python package for rendering chemical structures as ASCII/Unicode art, optimized for display in LLM terminal interfaces and text-based environments.

Core Objectives:
- Parse common chemical structure formats (SMILES, SDF)
- Render 2D chemical structures as text-based visualizations
- Provide clean, readable output suitable for terminal display

## Installation

Install via pip.
```bash
pip install chemscii
```

Development installation.
```bash
conda env create -f environment.yml
conda activate chemscii
poetry install
pre-commit install
```
