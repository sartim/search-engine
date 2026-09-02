# Development

## Install development tools

```bash
python -m pip install -e .
python -m pip install -r requirements-docs.txt
```

Build the documentation locally with:

```bash
mkdocs serve
```

Then open the local URL printed by MkDocs. To check the same rules used in CI:

```bash
mkdocs build --strict
```

## Documentation layout

Markdown source files live in `docs/`. `mkdocs.yml` controls navigation, theme, and site metadata. The generated `site/` directory is disposable build output and should not be committed.

## GitHub Pages deployment

The workflow at `.github/workflows/docs.yml` builds the site on pushes to `main`, uploads the generated artifact, and deploys it with GitHub's Pages deployment action.

In the repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**. After the first successful workflow run, the site is available at the `site_url` configured in `mkdocs.yml`.

## Package build

The project uses the modern PEP 517 build interface through `pyproject.toml`, while keeping the metadata in `setup.py` for straightforward setuptools compatibility:

```bash
python -m pip install build
python -m build
```
