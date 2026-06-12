# Conventions

## Config flags (module-level in plugin.py, read via tk.config.get + fallback)
- `ckanext.officedocs.supported_formats` — space-separated, matched
  case-insensitively, uppercased on read. Helper `get_supported_formats()`,
  default `DEFAULT_SUPPORTED_FORMATS`.
- `ckanext.officedocs.enable_private_fallback` — bool (default False, read via
  `tk.asbool`). Helper `private_fallback_enabled()`. Opt-in; when off, private
  packages get no view (preserves legacy behavior).
- Pattern for any new flag: `<CONST>_CONFIG` name + `DEFAULT_<NAME>` + a small
  reader helper mirroring the above.

## Format-list sync rule
When changing the default supported formats, update in sync:
1. `DEFAULT_SUPPORTED_FORMATS` in `plugin.py`
2. the two format lists in `README.md`.

## Private-package fallback (preview.html private branch)
- MS viewer can't reach private resources; the logged-in user's own browser can.
- Browser extensions CANNOT be reliably detected from a web page (third-party),
  so NO auto-render / no install detection — best-effort only.
- JS UA-detects Chromium (prefer `navigator.userAgentData.brands` containing
  "Chromium"; fallback UA-string check for Chrome/Chromium/Edg/OPR, excluding
  Firefox). Chromium → "Open document" link (target=_blank top-level nav, which an
  installed extension can render) + extension install tips. Non-Chromium →
  explanatory message. Default-visible block is the non-Chromium one (degrades
  without JS).

## Style
- 2/3-compatible; import cross-version helpers from `six`.
- `tk` = `ckan.plugins.toolkit`, `p` = `ckan.plugins`.
- `info()` sets `always_available: False` (no auto-create), `iframed: False`
  (template manages its own iframe).
- Tests use `monkeypatch` + the `ckan_config` fixture to set/delete config keys;
  assert `can_view()` directly with hand-built data_dicts.
