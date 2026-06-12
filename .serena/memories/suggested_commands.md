# Suggested Commands

Run inside an activated CKAN virtualenv (the extension can't run standalone;
plain `import ckan` fails otherwise).

## Dev install (from repo root)
- `python setup.py develop`
- `pip install -r dev-requirements.txt`

## Tests (pytest + CKAN test harness)
- All: `pytest --ckan-ini=test.ini ckanext/officedocs/tests`
- Single: `pytest --ckan-ini=test.ini ckanext/officedocs/tests/test_view.py::<test_name>`
- No `test.ini` is checked in — supply CKAN's test config (e.g. `test-core.ini`
  from the CKAN source tree, or a project `test.ini`).

## Notes
- Host OS is Darwin (macOS); standard BSD coreutils. No project-specific shell
  quirks beyond that.
