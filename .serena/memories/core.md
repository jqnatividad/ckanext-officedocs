# Core

CKAN extension `ckanext-officedocs`: registers one `IResourceView` plugin
(`officedocs_view`) that previews MS Office / OpenOffice docs by embedding
Microsoft's hosted Office Web Viewer in an iframe. No runtime deps of its own.

## Source map
- `ckanext/officedocs/plugin.py` — the entire plugin (`OfficeDocsPlugin` +
  module-level config helpers). Everything of interest lives here.
- `ckanext/officedocs/config_declaration.yaml` — CKAN config declaration for the
  three options (loaded via `@tk.blanket.config_declarations` on the plugin).
- `ckanext/officedocs/templates/officedocs/preview.html` — iframe + fullscreen JS
  (public branch) and private-package fallback panel (private branch); strings
  are i18n-wrapped.
- `ckanext/officedocs/templates/officedocs/form.html` — intentionally empty (no
  view config options).
- `ckanext/officedocs/tests/test_view.py` — pytest, CKAN factories + `ckan_config`.
- `ckanext/officedocs/{fanstatic,public}/` — empty placeholders (only .gitignore);
  all JS is inlined in templates despite `tk.add_resource("fanstatic", ...)`.
- `setup.py` — entry point `officedocs_view=...plugin:OfficeDocsPlugin` under
  `[ckan.plugins]`; bump `version` for releases.
- `test.ini` — CKAN test config (`use = config:../ckan/test-core.ini`); CI
  rewrites that path to the container's core test ini.
- `.github/workflows/` — `test.yml` (lint + CKAN matrix) and `publish.yml`
  (PyPI Trusted Publishing on `v*` tag). See `mem:tech_stack`.

## Invariants
- `can_view()` is the gate: format must be in supported list (always), AND
  package must be public — UNLESS the private-fallback flag is enabled (then
  private+supported is allowed too). It wraps logic in broad `try/except ->
  False`: view detection must never raise into CKAN page rendering.
- Private packages can't use MS's viewer (it fetches a public URL it can't
  reach). Private branch instead shows a client-side fallback; see `mem:conventions`.
- `setup_template_variables()` passes `resource_url` (quote_plus-encoded, for the
  MS viewer query param), `resource_download_url` (raw, for the fallback link),
  and `iframe_height`. Preserve the quote_plus on `resource_url`. Uses defensive
  `.get()` on data_dict.

## Further reading
- Stack & versions, CI/release: `mem:tech_stack`
- Commands to run (dev/test): `mem:suggested_commands`
- Code conventions, config flags, default-sync rule: `mem:conventions`
- What to run when a task is done: `mem:task_completion`

Note: a project `CLAUDE.md` (repo root) documents the same architecture in prose.
