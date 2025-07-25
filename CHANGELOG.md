# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2025-01-18

### Changed
- **Removed Windows support**: Focus on Unix-like systems (Linux, macOS) only
- Simplified CI/CD workflows by removing Windows-specific complexity
- Removed python-magic-bin dependency for Windows
- Streamlined GitHub Actions matrix to ubuntu-latest and macos-latest only

### Rationale
zrep is primarily designed for Unix/Linux development environments where
text replacement tools are commonly used. Removing Windows support allows
for simpler, more reliable CI/CD workflows and reduces maintenance overhead.

## [0.2.4] - 2025-01-18

### Fixed
- Improved Windows Poetry installation by using pip method instead of snok/install-poetry
- Use pip install poetry for Windows runners to avoid PATH issues
- Keep snok/install-poetry for non-Windows platforms (Linux/macOS)
- Add proper Poetry configuration for Windows environments

## [0.2.3] - 2025-01-18

### Fixed
- Fix Poetry installation and PATH configuration on Windows in GitHub Actions
- Add Poetry verification step for better debugging
- Improve PowerShell PATH handling for Windows runners
- Enable installer-parallel option for better performance

## [0.2.2] - 2025-01-18

### Fixed
- Fix libmagic dependency issue in GitHub Actions CI/CD
- Add system dependency installation for Ubuntu, macOS, and Windows
- Add python-magic-bin dependency for Windows support
- Improve CI/CD reliability across all platforms

## [0.2.1] - 2025-01-18

### Added
- Comprehensive GitHub Actions CI/CD pipeline
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Multi-version Python testing (3.10, 3.11, 3.12)
  - Automated code quality checks (Black, Ruff, MyPy)
  - Test coverage reporting
  - Security scanning with CodeQL
- Automated dependency updates with Dependabot
- Issue and PR templates for better contribution workflow
- Status badges in README
- Comprehensive documentation for GitHub Actions setup

### Changed
- Updated development dependencies to latest versions
- Improved project metadata and classifiers
- Enhanced documentation with GitHub Actions information

### Fixed
- Code formatting and linting issues
- Type annotation improvements using modern Python syntax

## [0.2.0] - 2025-01-18

### Added
- Object-oriented architecture with `ZRep` class
- Comprehensive command-line interface using argparse
- Dry-run mode for previewing changes (`--dry-run`)
- Custom directory specification (`--dir`)
- Configurable file and directory exclusions
- Type hints throughout the codebase
- Comprehensive test suite with pytest
- Code quality tools (Black, Ruff, MyPy)
- Poetry for dependency management

### Changed
- Migrated from procedural to object-oriented design
- Improved error handling and validation
- Better encoding handling (UTF-8 with error handling)
- Enhanced binary file detection with fallback
- Atomic file operations for safety

### Fixed
- Encoding issues with mixed character sets
- Global variable usage
- Lack of error handling in file operations
- Inconsistent code style

## [0.1.1] - Previous Release

### Added
- Basic string replacement functionality
- Recursive directory traversal
- Binary file detection
- Basic exclusion of .git and node_modules directories

### Features
- Simple command-line interface
- Chinese language support
- Basic file safety measures