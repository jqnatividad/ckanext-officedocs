# Task Completion

After a code change:

1. Run the test suite in an activated CKAN virtualenv:
   `pytest --ckan-ini=<test.ini> ckanext/officedocs/tests`
   (see `mem:suggested_commands` for the test.ini caveat).
2. Lint matches CI: `flake8 . --select=E9,F63,F7,F82` (CI's `test.yml` lint job
   fails the build on these).
3. If any config default changed, apply the default-sync rule in
   `mem:conventions` (constant + config_declaration.yaml + README).
4. If touching packaged data (templates, yaml), confirm it ships in the wheel:
   `python -m build && unzip -l dist/*.whl | grep <file>` (MANIFEST.in governs
   inclusion; `*.yaml` must stay listed).
5. `python -m build && python -m twine check dist/*` should PASS with no warnings.
6. Template/JS changes can't be unit-tested here — verify manually in-browser
   (public iframe path; private fallback in Chromium vs non-Chromium).

## Release (see git history for the established flow)
Bump `setup.py` version, commit, push master, annotated `vX.Y.Z` tag, GitHub
release with contributor credits (mirror prior releases' "What's Changed" /
"New Contributors" format). Pushing a `v*` tag triggers `publish.yml` →
PyPI Trusted Publishing (no token needed once the PyPI trusted publisher is set
up for the repo).
