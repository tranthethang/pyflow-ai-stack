# Publishing Guide

This guide explains how to publish the **PyFlow AI Stack** to PyPI and share it with the community.

## 📦 Publishing to PyPI

### 1. Prerequisites
Ensure you have `build` and `twine` installed:
```bash
pip install build twine
```

### 2. Update Version
Update the version number in `pyproject.toml`:
```toml
[project]
version = "1.0.1"
```

### 3. Build the Package
Run the following command to generate distribution archives:
```bash
python -m build
```
This will create a `dist/` directory with `.tar.gz` and `.whl` files.

### 4. Upload to PyPI
Use `twine` to upload the package to PyPI:
```bash
python -m twine upload dist/*
```
*Note: You will need a PyPI account and an API token.*

---

## 🤝 Sharing with the Community

### 1. GitHub Repository
- Ensure your `README.md` is up-to-date.
- Create a new [Release](https://github.com/your-repo/releases) on GitHub.
- Add descriptive tags (e.g., `fastapi`, `ai-boilerplate`, `gemini`, `workflow-node`).

### 2. Dify Community
If you are submitting this as a custom node for **Dify**:
- Document the API endpoints clearly in `docs/`.
- Export your Dify DSL if applicable.
- Share the repository link in the [Dify Discord](https://discord.gg/dify) or GitHub Discussions.

### 3. Social Platforms
- Share on **LinkedIn** or **X (Twitter)** using the hashtag `#FastAPI #GenerativeAI #Python`.
- Submit to **Awesome-FastAPI** or similar curated lists.

## 🛠️ Maintenance
- Regularly update dependencies in `requirements.txt` and `pyproject.toml`.
- Monitor GitHub Issues and Pull Requests for community feedback.
