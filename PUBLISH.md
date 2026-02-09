# Publishing Guide

This guide explains how to publish the **pyflow-ai-stack** package to [PyPI](https://pypi.org) and share it with the community.

## 📦 Publishing to PyPI

### 1. Prerequisites
Ensure you have the latest versions of `build` and `twine` installed:
```bash
pip install --upgrade build twine
```

### 2. Update Version
Before publishing, ensure the version number in [./pyproject.toml](./pyproject.toml) is correct:
```toml
[project]
name = "pyflow-ai-stack"
version = "1.0.0"
```

### 3. Build the Package
Run the following command from the project root to generate distribution archives:
```bash
python -m build
```
This will create a `dist/` directory containing:
- `pyflow_ai_stack-<version>.tar.gz` (Source Distribution)
- `pyflow_ai_stack-<version>-py3-none-any.whl` (Built Distribution)

### 4. Upload to PyPI
Use `twine` to upload the package to PyPI:
```bash
python -m twine upload dist/*
```
*Note: You will be prompted for your PyPI username (`__token__`) and password (your API token).*

---

## 🤝 Sharing with the Community

### 1. GitHub Repository
- Ensure your [./README.md](./README.md) is up-to-date.
- Create a new [Release](https://github.com/tranthethang/pyflow-ai-stack/releases) on GitHub.
- Add descriptive tags (e.g., `fastapi`, `gemini`, `ai-worker`, `workflow-node`).

### 2. Dify Community
If you are submitting this as a custom node or backend service for **Dify**:
- Document the API usage clearly in [./docs/](./docs/).
- Share the repository link in the [Dify Discord](https://discord.gg/dify) or GitHub Discussions.

---

## 🛠️ Maintenance
- **Update Dependencies**: Regularly check and update dependencies in [./pyproject.toml](./pyproject.toml).
- **Versioning**: Follow [Semantic Versioning](https://semver.org/) for new releases.
- **Support**: Monitor GitHub Issues and Pull Requests for community feedback.
