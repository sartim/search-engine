# Development

## Install development tools

```bash
uv sync --all-groups
```

## Branch naming

Use a standard type prefix followed by a short lowercase kebab-case description:

```text
feature/add-vector-search
fix/connection-timeout
docs/update-installation
chore/refresh-dependencies
```

Do not use a `codex/` prefix. Keep branches focused and open pull requests against `main`.

Build the documentation locally with:

```bash
uv run mkdocs serve
```

Then open the local URL printed by MkDocs. To check the same rules used in CI:

```bash
uv run mkdocs build --strict
```

## Documentation layout

Markdown source files live in `docs/`. `mkdocs.yml` controls navigation, theme, and site metadata. The generated `site/` directory is disposable build output and should not be committed. `uv.lock` records the resolved dependency versions used by local development and CI.

## GitHub Pages deployment

The workflow at `.github/workflows/docs.yml` builds the site on pushes to `main`, uploads the generated artifact, and deploys it with GitHub's Pages deployment action.

In the repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**. After the first successful workflow run, the site is available at the `site_url` configured in `mkdocs.yml`.

## Package build

The project uses the PEP 517 build interface through `pyproject.toml` and Hatchling:

```bash
uv build
```

## Releases

Release commits and tags are managed by `python-semantic-release`. Use Conventional Commit prefixes such as `feat:`, `fix:`, and `docs:` so the next version can be calculated from the commit history. The release workflow creates a GitHub release and explicitly dispatches the package-publishing workflow for a newly created tag. Configure the repository as a [PyPI trusted publisher](https://pypi.org/manage/account/publishing/) with this repository, the `publish.yml` workflow, and the `pypi` environment before publishing packages.
