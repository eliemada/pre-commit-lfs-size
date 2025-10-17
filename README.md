# pre-commit-lfs-size

[![CI](https://github.com/eliemada/pre-commit-lfs-size/workflows/CI/badge.svg)](https://github.com/eliemada/pre-commit-lfs-size/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pre-commit hook to ensure Git LFS-tracked files don't exceed a configurable size limit before committing.

## Why Use This Hook?

When using Git LFS (Large File Storage), it's important to maintain reasonable file sizes even for binary files. This hook helps you:

- Prevent accidentally committing oversized files to LFS
- Enforce size policies across your team
- Catch large files early in the development process
- Maintain repository performance and storage costs

## Installation

### Using pre-commit (Recommended)

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0  # Use the latest release
    hooks:
      - id: check-lfs-size
        args: ['--max-size', '100']  # Maximum size in MB (default: 50)
```

Then install the hook:

```bash
pre-commit install
```

### Manual Installation

1. Clone this repository or download `check_lfs_size.py`
2. Make it executable: `chmod +x check_lfs_size.py`
3. Copy it to your `.git/hooks/` directory as `pre-commit`

## Usage

### Basic Usage

By default, the hook checks for LFS files larger than 50 MB:

```bash
python check_lfs_size.py
```

### Custom Size Limit

Specify a custom maximum size in megabytes:

```bash
python check_lfs_size.py --max-size 100
```

### In Pre-commit Config

Configure the size limit using args:

```yaml
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
        args: ['--max-size', '200']  # 200 MB limit
```

## How It Works

The hook:

1. Identifies all staged files (added or modified)
2. Checks which files are tracked by Git LFS
3. Compares their sizes against the configured limit
4. Fails the commit if any LFS file exceeds the limit
5. Displays helpful error messages with file names and sizes

## Example Output

When a file exceeds the limit:

```
Error: The following LFS-tracked files exceed the size limit:
  assets/video.mp4: 75.23 MB (limit: 50.0 MB)
  models/large_model.pkl: 120.5 MB (limit: 50.0 MB)
```

## Requirements

- Python 3.9+ (tested on Python 3.9-3.14)
- Git with LFS installed and configured
- Files tracked by Git LFS (via `.gitattributes`)

## Configuration Examples

### For Different File Types

You can apply different size limits to different file types by creating multiple hook entries:

```yaml
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
        name: Check LFS videos (max 200MB)
        files: '.*\.(mp4|avi|mov)$'
        args: ['--max-size', '200']

      - id: check-lfs-size
        name: Check LFS models (max 500MB)
        files: '.*\.(pkl|h5|ckpt)$'
        args: ['--max-size', '500']
```

### With Other Pre-commit Hooks

Combine with other useful hooks:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=1000']  # Non-LFS files
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
        args: ['--max-size', '100']
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/eliemada/pre-commit-lfs-size.git
cd pre-commit-lfs-size

# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check check_lfs_size.py
```

### Automated Dependency Updates

This project uses [Renovate](https://github.com/apps/renovate) to automatically keep dependencies up to date. See [RENOVATE_SETUP.md](RENOVATE_SETUP.md) for configuration details.

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=check_lfs_size --cov-report=html

# Run specific test
uv run pytest tests/test_check_lfs_size.py::test_function_name
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Issues: [GitHub Issues](https://github.com/eliemada/pre-commit-lfs-size/issues)
- Discussions: [GitHub Discussions](https://github.com/eliemada/pre-commit-lfs-size/discussions)

## Related Projects

- [pre-commit](https://pre-commit.com/) - A framework for managing git hooks
- [Git LFS](https://git-lfs.github.com/) - Git Large File Storage
- [check-added-large-files](https://github.com/pre-commit/pre-commit-hooks#check-added-large-files) - Check for large files (non-LFS)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
