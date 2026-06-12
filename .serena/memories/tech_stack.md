# Tech Stack

- Language: Python; declares support for both 2.7 and 3.8 (keep new code 2/3
  compatible — `six` is used, esp. `six.moves.urllib.parse.quote_plus`).
- Framework: CKAN 2.10 extension. Uses `ckan.plugins` (`p`) and
  `ckan.plugins.toolkit` (aliased `tk`) for config, `aslist`, `asbool`,
  translations (`tk._`), template/resource registration.
- Packaging: setuptools (`setup.py`, find_packages). Plugin discovered via the
  `[ckan.plugins]` entry point.
- Dev dep: `six>=1.10.0` (`dev-requirements.txt`).
- Not runnable standalone — requires a working CKAN install + its test harness.
- No lint/format/type-check tooling configured in-repo.
