# Tech Stack

- Language: Python 3 only (CKAN 2.10/2.11). `python_requires>=3.8`. NOTE: six and
  Python 2 support were removed in 2.0.0 — use stdlib `urllib.parse`.
- Framework: CKAN extension. Uses `ckan.plugins` (`p`) and
  `ckan.plugins.toolkit` (aliased `tk`) for config, `aslist`, `asbool`,
  translations (`tk._`), template/resource registration, and
  `tk.blanket.config_declarations`.
- Config: declared in `ckanext/officedocs/config_declaration.yaml` (schema
  version 1), wired by the `@tk.blanket.config_declarations` class decorator.
- Packaging: setuptools (`setup.py`). `long_description_content_type=text/markdown`.
  Entry point `officedocs_view` under `[ckan.plugins]`. MANIFEST.in must keep
  `*.yaml` in the recursive-include so the config declaration ships in the wheel.
- CI: GitHub Actions in `.github/workflows/` — `test.yml` (flake8 lint +
  CKAN 2.10/2.11 matrix using ckan/ckan-dev containers + solr/postgres/redis;
  uses `test.ini`) and `publish.yml` (build + PyPI Trusted Publishing on `v*`
  tag push; needs a PyPI trusted-publisher configured for the repo).
- Dev dep: `pytest-cov` (`dev-requirements.txt`); pytest/factories come from
  CKAN's own dev-requirements.
- Not runnable standalone — needs a working CKAN install + its test harness.
