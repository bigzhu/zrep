# GitHub Actions & Automation

This directory contains GitHub Actions workflows and configuration files for automated testing, code quality checks, and releases.

## Workflows

### 🔄 CI Pipeline (`ci.yml`)
Runs on every push and pull request to main branches:
- **Multi-platform testing**: Ubuntu, Windows, macOS
- **Multi-version testing**: Python 3.10, 3.11, 3.12
- **Code quality checks**: Black formatting, Ruff linting, MyPy type checking
- **Test coverage**: Pytest with coverage reporting
- **Build verification**: Package building and installation testing

### 🚀 Release Pipeline (`release.yml`)
Triggers on version tags (e.g., `v0.2.0`):
- **Full test suite**: Runs across all platforms and Python versions
- **Automated building**: Creates wheel and source distributions
- **GitHub Release**: Automatically creates release with artifacts
- **PyPI Publishing**: Publishes to PyPI (requires `PYPI_TOKEN` secret)

### 🔍 Security Scanning (`codeql.yml`)
Runs weekly and on main branch changes:
- **CodeQL Analysis**: Automated security vulnerability scanning
- **Dependency scanning**: Identifies known security issues

## Dependabot (`dependabot.yml`)
Automatically updates dependencies:
- **Python dependencies**: Weekly updates on Mondays
- **GitHub Actions**: Weekly updates on Mondays
- **Auto-labeling**: Adds appropriate labels to PRs

## Issue & PR Templates
- **Bug reports**: Structured bug reporting with environment details
- **Feature requests**: Standardized feature request format
- **Pull request template**: Checklist for code review

## Setup Instructions

### For Repository Owners

1. **Enable GitHub Actions**: Ensure Actions are enabled in repository settings
2. **Set up PyPI publishing** (optional):
   ```bash
   # Create PyPI token and add as repository secret
   Settings → Secrets → Actions → New repository secret
   Name: PYPI_TOKEN
   Value: pypi-xxx...
   ```
3. **Configure Dependabot**: Enable Dependabot in repository settings
4. **Set up CodeQL**: Enable security scanning in repository settings

### For Contributors

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run tests locally**:
   ```bash
   poetry run pytest tests/ -v
   poetry run black --check zrep/ tests/
   poetry run ruff check zrep/ tests/
   poetry run mypy zrep/ --ignore-missing-imports
   ```
5. **Submit a pull request**

## Status Badges

Add these to your README.md:

```markdown
[![CI](https://github.com/username/zrep/workflows/CI/badge.svg)](https://github.com/username/zrep/actions/workflows/ci.yml)
[![CodeQL](https://github.com/username/zrep/workflows/CodeQL/badge.svg)](https://github.com/username/zrep/actions/workflows/codeql.yml)
[![Release](https://github.com/username/zrep/workflows/Release/badge.svg)](https://github.com/username/zrep/actions/workflows/release.yml)
```

## Release Process

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create and push a version tag**:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
4. **GitHub Actions will automatically**:
   - Run full test suite
   - Build packages
   - Create GitHub release
   - Publish to PyPI (if configured)

## Troubleshooting

### Common Issues

1. **Tests failing on Windows**: Check file path separators
2. **PyPI publishing fails**: Verify `PYPI_TOKEN` secret is set correctly
3. **CodeQL fails**: May need to exclude certain files or adjust configuration

### Getting Help

- Check the Actions tab for detailed logs
- Review the workflow files for configuration
- Open an issue if you encounter problems