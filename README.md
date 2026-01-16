# chemscii [![CI](https://github.com/b-shields/chemscii/actions/workflows/ci.yml/badge.svg)](https://github.com/b-shields/chemscii/actions/workflows/ci.yml)

A Python package for rendering chemical structures as ASCII/Unicode art in terminal interfaces and text-based environments.

Core Objectives:
- Parse common chemical structure formats (e.g., SMILES, SDF), names, and ChEMBL IDs
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

## Examples

### Render Colchicine (by name)
```bash
$ chemscii colchicine --columns 100
```
![colchicine.png](examples/images/colchicine.png)


### Use chemscii as a Claude code tool
![claude_code_example.png](examples/images/claude_code_example.png)
