# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of pre-commit-lfs-size hook
- Support for configurable file size limits via `--max-size` argument
- Automatic detection of Git LFS-tracked files
- Clear error messages showing oversized files with their sizes
- Comprehensive test suite with pytest
- GitHub Actions CI/CD pipeline
- MIT License
- Detailed README with usage examples

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2025-10-17

### Added
- Initial release
- Basic functionality to check LFS file sizes
- Pre-commit hook integration
- Command-line interface with argparse
- Support for custom size limits (default: 50 MB)

[Unreleased]: https://github.com/eliemada/pre-commit-lfs-size/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/eliemada/pre-commit-lfs-size/releases/tag/v0.1.0
