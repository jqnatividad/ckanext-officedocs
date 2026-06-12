# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`ckanext-officedocs` is a CKAN extension that registers an `IResourceView` plugin
(`officedocs_view`). It renders MS Office and OpenOffice documents in the browser by
embedding the [Microsoft Office Web Viewer](https://view.officeapps.live.com/op/view.aspx)
in an iframe. It has no runtime dependencies of its own — it relies entirely on CKAN's
plugin toolkit and Microsoft's hosted viewer service.

## Architecture

The entire plugin is `ckanext/officedocs/plugin.py` (~70 lines). Key points:

- `OfficeDocsPlugin` implements `IConfigurer` (registers template/public/fanstatic dirs)
  and `IResourceView` (the preview behavior).
- `can_view()` is the gate. It returns `True` only when the package is **public** AND the
  resource format is in the supported list. Private packages always return `False` because
  Microsoft's viewer fetches the document from a public URL — it cannot reach private/
  authenticated resources. This public/private check is the most important invariant; the
  `preview.html` template branches on `private_package` to show an explanatory message
  instead of a broken iframe.
- Supported formats are configurable via `ckanext.officedocs.supported_formats` (space-
  separated, matched case-insensitively, uppercased on read). `get_supported_formats()`
  reads config with `DEFAULT_SUPPORTED_FORMATS` as fallback. When changing the default
  list, update it in three places that must stay in sync: `DEFAULT_SUPPORTED_FORMATS` in
  `plugin.py`, and the two format lists in `README.md`.
- `setup_template_variables()` URL-encodes the resource URL with `quote_plus` before it is
  interpolated into the Office viewer `src` — preserve this encoding.

Templates live in `ckanext/officedocs/templates/officedocs/`: `preview.html` (the iframe +
fullscreen JS) and `form.html` (intentionally empty — no view configuration options).

## Commands

This is a CKAN extension and is not runnable standalone; tests require a working CKAN
install with its test harness. Within an activated CKAN virtualenv:

```sh
# Install for development (run from repo root)
python setup.py develop
pip install -r dev-requirements.txt

# Run the test suite (tests use CKAN factories + pytest fixtures like ckan_config)
pytest --ckan-ini=test.ini ckanext/officedocs/tests

# Run a single test
pytest --ckan-ini=test.ini ckanext/officedocs/tests/test_view.py::test_can_view_uses_default_supported_formats
```

Note: there is no `test.ini` checked into this repo; supply CKAN's test config (typically
`test-core.ini` from your CKAN source tree, or a project `test.ini`).

## Conventions

- Targets CKAN 2.10. Uses `ckan.plugins.toolkit` (aliased `tk`) for config access,
  `aslist`, translations (`tk._`), and template/resource registration.
- Python 2.7 and 3.8 are both declared as supported; `six` (via `six.moves.urllib.parse`)
  is used for cross-version compatibility — keep new code 2/3 compatible.
- The plugin entry point is declared in `setup.py` under `[ckan.plugins]` as
  `officedocs_view=ckanext.officedocs.plugin:OfficeDocsPlugin`. Bump `version` in
  `setup.py` for releases.
- `can_view()` wraps its logic in a broad `try/except` returning `False` — view detection
  must never raise into CKAN's resource page rendering.
