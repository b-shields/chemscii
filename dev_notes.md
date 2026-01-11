# CHEMSCII Project

This project was developed in part as a test exercise for using Claude code. In this document I log the workflow I used and observations made along the way. The general approach is to micro manage Claude and build the package step-by-step. I did this by iteratively running Claude code, checking / modifiying the output, and committing the changes myself.

## Getting Started

1. Set up CLAUDE.md
- I wrote this one myself
2. Build the package structure in README.md
- Followed prompts to generate stubs
3. Build a conda environment.yml with python 3.9+ and poetry as requirments
- Looked good
4. Build pyproject.toml with rdkit 2025+, numpy 2.0+, pillow, and rich as requirements and pytest, black, ruff, mypy as development dependencies
- Slight modifications
- Tested environment build and install
5. Set up pre-commit hooks
- Looked good
6. Add installation instructions to README.md
- Slightly modified
7. Add initial test fixtures for a molecule SMILES and SDF
- Looked good
8. Configure CI/CD (GitHub Actions)
- Add GitHub Actions test status to README.md
9. Commit initial structure to main
- I did this myself
- It required a lot of patching to get the pre-commit hooks to pass. Example "Only use modern python type hints. Modules should use built in types instead of Types (e.g.,
list instead of Typing.List).

## Development

The following prompts were used and iteration was carried out until precommit hooks passed.

**Parsers**
1. Generate molecule.py parsers and unit tests based on stub
2. Generate name.py parser and unit tests based on stub

## Claude Integration Example

## Write Blog Post
