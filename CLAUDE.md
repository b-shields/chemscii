# chemscii development

## general guidelines

YOU MUST follow Python best practices and modern development standards. It is IMPORTANT to NOT DEVIATE from these principles:
1. YOU MUST use conda for virtual environment management
2. YOU MUST use poetry for python dependency management
3. YOU MUST write unit tests for all modules
4. YOU MUST use CI/CD (GitHub Actions) with pytest (unit testing), black (formatting), ruff (linting), and optionally mypy (type checking)
5. YOU MUST use type hints for all code
6. YOU MUST otherwise follow google code and docstring conventions
7. YOU MUST write code that is minimal, simple, reusable, and easy to understand

## project scope

YOU MUST focus entirely on building a python package for rendering chemical structures as ASCII/Unicode art, optimized for text-based environments.
