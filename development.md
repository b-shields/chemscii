# CHEMSCII Project

This project was developed in part as a test exercise for using Claude Code. This document logs the workflow and observations made along the way. The general approach was to iteratively build the package step-by-step, running Claude Code, reviewing and modifying the output, and committing changes manually.

## Getting Started

1. **Set up CLAUDE.md**
   - Written manually to establish project guidelines

2. **Build the package structure in README.md**
   - Used prompts to generate initial stubs

3. **Build conda environment.yml**
   - Configured with Python 3.9+ and Poetry as requirements

4. **Build pyproject.toml**
   - Dependencies: rdkit 2025+, numpy 2.0+, pillow, rich
   - Dev dependencies: pytest, black, ruff, mypy
   - Made slight modifications and tested environment build and install

5. **Set up pre-commit hooks**
   - Configuration worked as expected

6. **Add installation instructions to README.md**
   - Made minor modifications

7. **Add initial test fixtures**
   - Created molecule SMILES and SDF fixtures

8. **Configure CI/CD (GitHub Actions)**
   - Added GitHub Actions test status badge to README.md

9. **Commit initial structure to main**
   - Required patching to pass pre-commit hooks
   - Example fix: using modern Python type hints (e.g., `list` instead of `typing.List`)

## Development

The following example prompts were used, iterating until pre-commit hooks passed.
1. Generate `molecule.py` parsers and unit tests based on stub
2. Generate `name.py` parser and unit tests based on stub
3. Generate `chembl.py` parser and unit tests based on stub
4. Generate `atoms.py` and `bonds.py` layouts based on stub
   - Unit tests were generated automatically, likely based on history and CLAUDE.md
5. Generate `ascii.py` renderer and unit tests based on stub
6. Generate `unicode.py` renderer and unit tests based on stub, matching `ascii.py` patterns
7. Add `magic.py` renderer using the ascii-magic package and PNG from RDKit
   - Clause wasn't able to accomplish this. Implemented manually.
   - Format and add docstrings to `magic.py`, consistent with other modules and project guidelines
   - Update `basic_usage.ipynb` to include `AsciiMagicRenderer`
   - Generate unit tests for `magic.py`
11. Generate a CLI for rendering molecules with chemscii
   - CLI should automatically identify and parses SMILES, files, names, and ChEMBL IDs
   - Silenced RDKit warnings manually

### Observations

- Providing a project tree structure, generating code stubs (with the desired schema), and then generating code based on stubs worked well.
- All steps required some editing / iterating.
