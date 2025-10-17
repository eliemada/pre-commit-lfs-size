# Complete Release Guide

## Pre-Release Checklist

✅ All tasks completed:
- [x] Code follows best practices
- [x] All ruff linting passes
- [x] 22 unit tests with 98% coverage
- [x] Comprehensive README with examples
- [x] MIT LICENSE file
- [x] CHANGELOG.md with version history
- [x] GitHub Actions CI/CD configured
- [x] .gitignore properly configured
- [x] pyproject.toml fully configured

## Step-by-Step Release Process

### 1. Initialize Git Repository

```bash
cd /Users/eliebruno/Desktop/code/pre-commit-lfs-size

# Initialize git if not already done
git init

# Add all files
git add .

# Check what will be committed (should exclude .venv, __pycache__, etc.)
git status

# Create initial commit
git commit -m "Initial commit: pre-commit hook for LFS file size checking

- Checks Git LFS-tracked files against configurable size limits
- Comprehensive test suite with 98% coverage
- Full documentation and examples
- GitHub Actions CI/CD pipeline
- MIT licensed"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `pre-commit-lfs-size`
   - **Description**: `Pre-commit hook to check Git LFS file sizes before commit`
   - **Visibility**: Public (recommended for pre-commit hooks)
   - **Do NOT check**: Initialize with README, .gitignore, or license (you have these)
3. Click "Create repository"

### 3. Connect Local Repository to GitHub

```bash
# Add GitHub remote
git remote add origin https://github.com/eliemada/pre-commit-lfs-size.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Verify GitHub Actions

After pushing, your GitHub Actions workflow should automatically run:

1. Go to https://github.com/eliemada/pre-commit-lfs-size/actions
2. You should see the CI workflow running
3. Wait for it to complete (green checkmark = success)
4. If tests fail, fix issues and push again

### 5. Configure Repository Settings

#### Enable Issues & Discussions

1. Go to: https://github.com/eliemada/pre-commit-lfs-size/settings
2. Under "Features":
   - ✅ Check "Issues"
   - ✅ Check "Discussions" (optional but recommended)

#### Add Repository Topics

1. Go to repository homepage
2. Click ⚙️ (gear icon) next to "About"
3. Add topics:
   ```
   pre-commit
   pre-commit-hook
   git-lfs
   git-hooks
   file-size
   python
   python3
   developer-tools
   ```
4. Update description if needed
5. Add website (optional): https://pre-commit.com

### 6. Create Your First Release (v0.1.0)

#### Option A: Using GitHub Web Interface (Recommended)

1. Go to: https://github.com/eliemada/pre-commit-lfs-size/releases/new
2. Fill in the release form:
   - **Choose a tag**: Type `v0.1.0` and click "Create new tag: v0.1.0 on publish"
   - **Target**: `main`
   - **Release title**: `v0.1.0 - Initial Release`
   - **Description**: Copy the content below
3. Click "Publish release"

**Release Description:**

```markdown
## 🎉 Initial Release

First stable release of pre-commit-lfs-size hook!

### Features

- ✅ Check Git LFS-tracked files against configurable size limits
- ✅ Clear error messages showing oversized files with their sizes
- ✅ Easy integration with pre-commit framework
- ✅ Default 50 MB limit, customizable via `--max-size` argument
- ✅ Comprehensive test suite (22 tests, 98% coverage)
- ✅ Full documentation and examples

### Installation

Add to your `.pre-commit-config.yaml`:

\`\`\`yaml
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
        args: ['--max-size', '100']  # Optional: customize size limit (default: 50)
\`\`\`

Then run:

\`\`\`bash
pre-commit install
\`\`\`

### Usage Example

When a file exceeds the limit:

\`\`\`
Error: The following LFS-tracked files exceed the size limit:
  assets/video.mp4: 75.23 MB (limit: 50.0 MB)
  models/large_model.pkl: 120.5 MB (limit: 50.0 MB)
\`\`\`

### Documentation

- 📖 [README](https://github.com/eliemada/pre-commit-lfs-size#readme) - Full documentation
- 📝 [CHANGELOG](https://github.com/eliemada/pre-commit-lfs-size/blob/main/CHANGELOG.md) - Version history
- 🐛 [Issues](https://github.com/eliemada/pre-commit-lfs-size/issues) - Report bugs or request features

### Requirements

- Python 3.9 or higher
- Git with LFS installed
- pre-commit framework

---

**What's Changed**
- Initial implementation of LFS file size checking
- Full test suite with pytest
- GitHub Actions CI/CD pipeline
- MIT License
```

#### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if not already installed
# macOS: brew install gh
# Or download from: https://cli.github.com/

# Authenticate with GitHub
gh auth login

# Create the release
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "See CHANGELOG.md for details. Full documentation at https://github.com/eliemada/pre-commit-lfs-size#readme"
```

#### Option C: Using Git Tags + Manual Release

```bash
# Create annotated tag
git tag -a v0.1.0 -m "v0.1.0 - Initial Release

Initial release of pre-commit-lfs-size hook with:
- LFS file size checking
- Comprehensive test suite
- Full documentation"

# Push the tag
git push origin v0.1.0

# Then go to GitHub web interface to create the release from the tag
```

### 7. Test the Installation

Verify that others can use your hook:

```bash
# Create a test directory
cd /tmp
mkdir test-lfs-hook
cd test-lfs-hook

# Initialize git and LFS
git init
git lfs install

# Create .gitattributes for LFS
echo "*.bin filter=lfs diff=lfs merge=lfs -text" > .gitattributes

# Add pre-commit config
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
        args: ['--max-size', '10']  # 10 MB for testing
EOF

# Install pre-commit
pre-commit install

# Test with a small file (should pass)
echo "small file" > small.bin
git add .
git commit -m "Test: small file"

# Test with a large file (should fail)
dd if=/dev/zero of=large.bin bs=1m count=15  # 15 MB
git add large.bin
git commit -m "Test: large file"  # Should be rejected!
```

### 8. Set Up Branch Protection (Optional but Recommended)

1. Go to: https://github.com/eliemada/pre-commit-lfs-size/settings/branches
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select checks: `test` and `lint`
   - ✅ Require linear history (optional)
5. Click "Create"

### 9. Announce Your Hook

#### Pre-commit Community

The pre-commit framework has a list of hooks. Consider submitting yours:
- Documentation: https://pre-commit.com/
- Hooks list: https://pre-commit.com/hooks.html

#### Social Media & Communities

1. **Dev.to** - Write a blog post:
   - Title: "Building a Pre-commit Hook to Enforce LFS File Size Limits"
   - Tags: python, git, devtools, tutorial

2. **Reddit**:
   - r/Python
   - r/git
   - r/programming

3. **Twitter/X**:
   ```
   🎉 Just released pre-commit-lfs-size v0.1.0!

   A pre-commit hook to keep your Git LFS files under control.

   ✅ Configurable size limits
   ✅ Clear error messages
   ✅ Easy integration

   Check it out: https://github.com/eliemada/pre-commit-lfs-size

   #Python #Git #DevTools #OpenSource
   ```

4. **Hacker News** - Show HN:
   - Title: "Show HN: Pre-commit hook to enforce Git LFS file size limits"
   - URL: https://github.com/eliemada/pre-commit-lfs-size

### 10. Maintenance & Future Releases

#### Responding to Issues

- Enable GitHub notifications
- Try to respond within 24-48 hours
- Label issues appropriately: `bug`, `enhancement`, `question`, `good first issue`
- Be friendly and welcoming to contributors

#### Creating Future Releases

When you make improvements:

1. **Update CHANGELOG.md**:
   ```markdown
   ## [0.2.0] - 2025-XX-XX

   ### Added
   - New feature description

   ### Fixed
   - Bug fix description
   ```

2. **Bump version in pyproject.toml**:
   ```toml
   version = "0.2.0"
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   git push
   ```

4. **Create new tag and release**:
   ```bash
   git tag -a v0.2.0 -m "v0.2.0 - Description"
   git push origin v0.2.0
   ```

5. **Create GitHub release** (same as step 6)

#### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.2.0): New features, backwards compatible
- **PATCH** (0.1.1): Bug fixes, backwards compatible

## Optional: Publish to PyPI

If you want to make it pip-installable:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Test upload to TestPyPI first (optional)
python -m twine upload --repository testpypi dist/*

# Upload to real PyPI
python -m twine upload dist/*
```

Then users can install via:
```bash
pip install pre-commit-lfs-size
```

## Success Metrics

Track these to measure adoption:

1. **GitHub Stars**: Star count on your repository
2. **Downloads**: Check GitHub Insights → Traffic
3. **Issues/PRs**: Community engagement
4. **Forks**: How many people are forking
5. **Dependents**: Who's using your hook (check "Used by" on GitHub)

## Need Help?

- GitHub Docs: https://docs.github.com/
- Pre-commit Docs: https://pre-commit.com/
- Packaging Tutorial: https://packaging.python.org/tutorials/packaging-projects/

---

## Quick Reference Commands

```bash
# Check everything is ready
uv run pytest
uvx ruff check .
uvx ruff format --check .

# Initialize and push
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/eliemada/pre-commit-lfs-size.git
git push -u origin main

# Create release
git tag -a v0.1.0 -m "v0.1.0 - Initial Release"
git push origin v0.1.0

# Future updates
git add .
git commit -m "Description"
git push
git tag -a v0.2.0 -m "v0.2.0 - Description"
git push origin v0.2.0
```

---

**You're all set! 🚀**

Your pre-commit hook is production-ready and ready to help the community!
