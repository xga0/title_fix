# Deployment Guide

## Overview

This project uses GitHub Actions for automatic deployment to PyPI. The deployment is triggered when you create a release on GitHub.

## Prerequisites

1. **PyPI API Token**: You need to set up a PyPI API token as a GitHub secret:
   - Go to PyPI.org and create an API token for your account
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add a new repository secret named `PYPI_API_TOKEN` with your PyPI token

## Deployment Process

### 1. Update Version

Before creating a release, ensure the version in `pyproject.toml` matches your intended release version:

```toml
version = "0.0.1"  # Update this to your target version
```

### 2. Create and Push Git Tag

```bash
# Create an annotated tag
git tag -a 0.0.1 -m "Release version 0.0.1"

# Push the tag to GitHub
git push origin 0.0.1
```

### 3. Create GitHub Release

1. Go to your GitHub repository
2. Click on "Releases" → "Create a new release"
3. Select the tag you just created (e.g., `0.0.1`)
4. Add release title and description
5. Click "Publish release"

### 4. Automatic Deployment

Once you publish the release, the GitHub Actions workflow will automatically:

1. **Test Phase** (runs on Python 3.8-3.12):
   - Install dependencies
   - Run all 33 test cases
   - Test all citation styles and case types
   - Test edge cases (empty strings, Unicode, emojis, etc.)
   - Verify package installation

2. **Build and Deploy Phase**:
   - Verify version consistency between tag and pyproject.toml
   - Build the package (wheel and source distribution)
   - Test the built package
   - Check package metadata
   - Deploy to PyPI
   - Verify the deployment

## Workflow Features

### Comprehensive Testing

The workflow tests:
- All supported Python versions (3.8-3.12)
- All citation styles (APA, Chicago, AP, MLA, NYT)
- All case types (title, sentence, upper, lower, first, alt, toggle)
- Edge cases: empty strings, single characters, acronyms, Roman numerals, Unicode, emojis
- Package installation and import

### Safety Checks

- Version consistency verification (tag must match pyproject.toml)
- Package metadata validation
- Built package testing before deployment
- Post-deployment verification

### Manual Release Control

- Deployment only happens when you manually create a GitHub release
- No automatic deployments on every commit
- Full control over when new versions are published

## Troubleshooting

### Version Mismatch Error

If you get a version mismatch error:
1. Update the version in `pyproject.toml`
2. Commit the change
3. Delete and recreate the tag with the correct version

### PyPI Token Issues

If deployment fails with authentication errors:
1. Verify your PyPI API token is correct
2. Check that the `PYPI_API_TOKEN` secret is properly set in GitHub
3. Ensure the token has upload permissions

### Test Failures

If tests fail:
1. Run tests locally: `python -m pytest tests/ -v`
2. Fix any issues
3. Commit and push changes
4. Delete and recreate the tag

## Next Release

For the next release (e.g., 0.0.2):

1. Update version in `pyproject.toml`
2. Commit changes
3. Create and push new tag
4. Create GitHub release
5. Workflow automatically deploys to PyPI

The deployment system is now fully automated and ready for production use! 