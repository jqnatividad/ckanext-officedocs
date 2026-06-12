# Core

CKAN extension `ckanext-officedocs`: registers one `IResourceView` plugin
(`officedocs_view`) that previews MS Office / OpenOffice docs by embedding
Microsoft's hosted Office Web Viewer in an iframe. No runtime deps of its own.

## Source map
- `ckanext/officedocs/plugin.py` — the entire plugin (`OfficeDocsPlugin` +
  module-level config helpers). Everything of interest lives here.
- `ckanext/officedocs/templates/officedocs/preview.html` — iframe + fullscreen JS
  (public branch) and private-package fallback panel (private branch).
- `ckanext/officedocs/templates/officedocs/form.html` — intentionally empty (no
  view config options).
- `ckanext/officedocs/tests/test_view.py` — pytest, CKAN factories + `ckan_config`.
- `ckanext/officedocs/{fanstatic,public}/` — empty placeholders (only .gitignore);
  all JS is inlined in templates despite `tk.add_resource("fanstatic", ...)`.
- `setup.py` — declares entry point `officedocs_view=...plugin:OfficeDocsPlugin`
  under `[ckan.plugins]`; bump `version` for releases.

## Invariants
- `can_view()` is the gate: format must be in supported list (always), AND
  package must be public — UNLESS the private-fallback flag is enabled (then
  private+supported is allowed too). It wraps logic in broad `try/except ->
  False`: view detection must never raise into CKAN page rendering.
- Private packages can't use MS's viewer (it fetches a public URL it can't
  reach). Private branch instead shows a client-side fallback; see `mem:conventions`.
- `setup_template_variables()` passes `resource_url` (quote_plus-encoded, for the
  MS viewer query param) AND `resource_download_url` (raw, for the fallback link).
  Preserve the quote_plus on `resource_url`.

## Further reading
- Stack & versions: `mem:tech_stack`
- Commands to run (dev/test): `mem:suggested_commands`
- Code conventions, config flags, format-sync rule: `mem:conventions`
- What to run when a task is done: `mem:task_completion`

Note: a project `CLAUDE.md` (repo root) documents the same architecture in prose.
