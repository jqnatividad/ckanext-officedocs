# Conventions

## Config flags
Three options, each with a module-level `<NAME>_CONFIG` constant + `DEFAULT_<NAME>`
+ a reader helper in `plugin.py`, AND a declaration entry in
`ckanext/officedocs/config_declaration.yaml` (loaded via the
`@tk.blanket.config_declarations` decorator on the plugin class):
- `ckanext.officedocs.supported_formats` — space-separated, case-insensitive,
  uppercased on read. Helper `get_supported_formats()`.
- `ckanext.officedocs.enable_private_fallback` — bool (default False). Helper
  `private_fallback_enabled()`. Opt-in; off → private packages get no view.
- `ckanext.officedocs.iframe_height` — CSS length (default "400px"). Helper
  `get_iframe_height()`; passed to preview.html for the public iframe.
- Helpers keep an inline `tk.config.get(KEY, DEFAULT)` fallback ON PURPOSE: unit
  tests instantiate the plugin directly without loading the declaration, so the
  inline default must still apply. Don't remove it.
- Pattern for a new flag: constant + DEFAULT + helper + yaml entry.

## Default-value sync rule
A default lives in several places that must stay consistent:
- supported_formats default: `DEFAULT_SUPPORTED_FORMATS` (plugin.py),
  `config_declaration.yaml`, and the README (intro example lists + the
  "Configuration reference" table). Keep all in sync when changing it.
- Other defaults: the `DEFAULT_*` constant, the yaml, and the README table.

## Private-package fallback (preview.html private branch)
- MS viewer can't reach private resources; the logged-in user's own browser can.
- Browser extensions CANNOT be reliably detected from a web page (third-party),
  so NO auto-render / no install detection — best-effort only.
- JS UA-detects Chromium (prefer `navigator.userAgentData.brands` containing
  "Chromium"; fallback UA-string check for Chrome/Chromium/Edg/OPR, excluding
  Firefox). Chromium → "Open document" link (target=_blank top-level nav) +
  install tips. Non-Chromium → explanatory message. Default-visible block is the
  non-Chromium one (degrades without JS).
- User-facing template strings are wrapped in `{{ _(...) }}` for i18n.

## Style
- Python 3 only (CKAN 2.10/2.11). `urllib.parse` (NOT six — six was removed in
  2.0.0). `python_requires>=3.8`.
- `tk` = `ckan.plugins.toolkit`, `p` = `ckan.plugins`.
- `info()` sets `always_available: False` (no auto-create), `iframed: False`
  (template manages its own iframe).
- `setup_template_variables` uses defensive `.get()` (never index data_dict).
- Tests use `monkeypatch` + `ckan_config` fixture to set/delete config keys;
  assert `can_view()` / `setup_template_variables()` directly with hand-built
  data_dicts (see `mem:tests`-style cases in tests/test_view.py).
