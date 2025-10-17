# Publishing Guide for pre-commit-lfs-size

This guide will help you publish this pre-commit hook to GitHub and make it available for others to use.

## Pre-Publishing Checklist

- [x] All code follows best practices and passes linting (ruff)
- [x] Comprehensive test suite with 98% coverage
- [x] README with clear installation and usage instructions
- [x] LICENSE file (MIT)
- [x] CHANGELOG documenting all changes
- [x] GitHub Actions CI/CD pipeline configured
- [x] Example `.pre-commit-config.yaml` included
- [x] pyproject.toml fully configured

## Steps to Publish

### 1. Initialize Git Repository (if not done)

```bash
git init
git add .
git commit -m "Initial commit: pre-commit hook for LFS file size checking"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `pre-commit-lfs-size`
3. Description: "Pre-commit hook to check Git LFS file sizes before commit"
4. Public repository (recommended for pre-commit hooks)
5. **Do NOT** initialize with README, .gitignore, or license (you already have these)
6. Click "Create repository"

### 3. Push to GitHub

```bash
git remote add origin https://github.com/eliemada/pre-commit-lfs-size.git
git branch -M main
git push -u origin main
```

### 4. Create Your First Release

#### Option A: Using GitHub Web Interface

1. Go to https://github.com/eliemada/pre-commit-lfs-size/releases/new
2. Click "Choose a tag" and type `v0.1.0`
3. Release title: `v0.1.0 - Initial Release`
4. Description:
   ```markdown
   ## Initial Release

   First stable release of pre-commit-lfs-size hook.

   ### Features
   - Check Git LFS-tracked files against configurable size limits
   - Clear error messages showing oversized files
   - Easy integration with pre-commit framework
   - Default 50 MB limit, customizable via `--max-size` argument

   ### Installation
   Add to your `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/eliemada/pre-commit-lfs-size
       rev: v0.1.0
       hooks:
         - id: check-lfs-size
           args: ['--max-size', '100']  # Optional: customize size limit
   ```

   See [README](https://github.com/eliemada/pre-commit-lfs-size#readme) for full documentation.
   ```
5. Click "Publish release"

#### Option B: Using Git Command Line

```bash
# Create and push the tag
git tag -a v0.1.0 -m "v0.1.0 - Initial Release"
git push origin v0.1.0

# Then create the release on GitHub web interface as above
```

#### Option C: Using GitHub CLI

```bash
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "See CHANGELOG.md for details"
```

### 5. Enable GitHub Features

#### Enable Issues
1. Go to repository Settings → General → Features
2. Check "Issues"

#### Enable Discussions (Optional)
1. Go to repository Settings → General → Features
2. Check "Discussions"

#### Set Up Branch Protection (Recommended)
1. Go to Settings → Branches → Branch protection rules
2. Add rule for `main` branch:
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Select status checks: `test`, `lint`

### 6. Add Repository Topics/Tags

1. Go to your repository homepage
2. Click the gear icon next to "About"
3. Add topics:
   - `pre-commit`
   - `pre-commit-hook`
   - `git-lfs`
   - `git-hooks`
   - `file-size`
   - `python`
   - `python3`

### 7. Verify GitHub Actions

1. Push to GitHub triggers the CI workflow
2. Go to Actions tab to verify tests pass
3. Green checkmark means everything is working!

### 8. Test Installation

Test that others can use your hook:

```bash
# In a test repository
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/eliemada/pre-commit-lfs-size
    rev: v0.1.0
    hooks:
      - id: check-lfs-size
EOF

pre-commit install
pre-commit run --all-files
```

## Optional: Publish to PyPI

If you want to make it pip-installable:

```bash
# Install build tools
uv pip install build twine

# Build the package
python -m build

# Upload to PyPI (you'll need a PyPI account)
python -m twine upload dist/*
```

Then users can install via:
```bash
pip install pre-commit-lfs-size
```

## Announcing Your Hook

1. **pre-commit.com**: Submit a PR to add your hook to the [supported hooks list](https://pre-commit.com/hooks.html)
2. **Reddit**: Share on r/Python or r/git
3. **Twitter/X**: Tweet about it with #Python #Git #DevTools
4. **Dev.to**: Write a blog post about why you created it

## Maintenance

### For Future Releases

1. Update CHANGELOG.md with changes
2. Bump version in pyproject.toml
3. Commit changes
4. Create new tag and release:
   ```bash
   git tag -a v0.2.0 -m "v0.2.0 - Description"
   git push origin v0.2.0
   ```
5. Create GitHub release with notes

### Responding to Issues

- Enable GitHub notifications
- Respond to issues within a few days
- Label issues appropriately (bug, enhancement, question)
- Use issue templates to standardize reports

## Success Metrics

Track these to measure adoption:
- GitHub stars
- Number of clones/downloads
- Issues and PRs from community
- Mentions in other projects' `.pre-commit-config.yaml` files

## Support

If you need help:
- GitHub Discussions for questions
- GitHub Issues for bugs
- Consider adding a CONTRIBUTING.md for contributors

---

**Ready to publish?** Follow the steps above and your pre-commit hook will be available for the community to use!
