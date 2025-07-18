# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

zrep is a simple Python command-line tool for replacing strings in files across directories. It's designed as a user-friendly alternative to sed for recursive string replacement across all files in a project.

## Architecture

The project follows an object-oriented architecture:

- `zrep/zrep.py`: Main module containing all functionality
  - `ZRep` class: Main functionality encapsulated in a class
    - `get_file_paths()`: Recursive directory traversal with configurable exclusions
    - `replace_in_directory()`: Orchestrates the replacement process
  - `main()`: Entry point with argparse-based command-line interface
  - `replace_in_file()`: Core replacement logic with atomic file operations
  - `is_binary_file()`: Uses python-magic to detect binary files with fallback
  - `check_pattern_in_file()`: Verifies if pattern exists before replacement
  - `create_parser()`: Creates the argument parser with comprehensive options

## GitHub Actions

The project includes comprehensive CI/CD workflows:

- **CI Pipeline**: Multi-platform testing (Ubuntu, Windows, macOS) across Python 3.10-3.12
- **Release Pipeline**: Automated releases and PyPI publishing on version tags
- **Security Scanning**: CodeQL analysis for vulnerability detection
- **Dependabot**: Automated dependency updates

### Development Environment Setup

Before contributing, ensure you can run the full test suite locally:

```bash
# Install dependencies
poetry install

# Run the complete test suite
poetry run pytest tests/ -v --cov=zrep --cov-report=html

# Run all quality checks (same as CI)
poetry run black --check zrep/ tests/
poetry run ruff check zrep/ tests/
poetry run mypy zrep/ --ignore-missing-imports
```

## Common Commands

### Development
```bash
# Install dependencies (including dev dependencies)
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=zrep --cov-report=html

# Format code
poetry run black zrep/ tests/

# Lint code
poetry run ruff check zrep/ tests/

# Type check
poetry run mypy zrep/

# Run the tool
poetry run zrep "old_string" "new_string"

# Alternative after installation
python -m zrep.zrep "old_string" "new_string"
```

### Building and Distribution
```bash
# Build the package
poetry build

# Install locally
pip install dist/zrep-*.whl
```

## Key Implementation Details

- **Object-oriented design**: Main functionality encapsulated in `ZRep` class
- **Type hints**: Full type annotation for better code quality
- **Robust error handling**: Comprehensive exception handling for file operations
- **UTF-8 encoding**: Consistent UTF-8 encoding with error handling
- **Binary file detection**: Uses `python-magic` with fallback detection
- **Atomic file operations**: Safe replacement using temporary files
- **Configurable exclusions**: Customizable directory and file exclusion patterns
- **Comprehensive CLI**: argparse-based interface with dry-run mode
- **Extensive testing**: Unit tests for all major functionality

## New Features (v0.2.0)

- **Dry-run mode**: Preview changes before applying them
- **Custom exclusions**: Add additional directories and files to exclude
- **Better error messages**: Detailed error reporting and validation
- **Directory specification**: Process specific directories instead of just current
- **Improved safety**: Better binary file detection and encoding handling

## Dependencies

- `python-magic`: For MIME type detection to identify binary files
- Standard library: `tempfile`, `shutil`, `os`, `sys`, `argparse`, `pathlib`, `typing`

## Development Dependencies

- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `ruff`: Fast Python linter
- `mypy`: Static type checker

## Entry Point

The package is configured in `pyproject.toml` with console script entry point:
```toml
[tool.poetry.scripts]
zrep = "zrep.zrep:main"
```