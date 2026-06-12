# Task Completion

No lint/format/type-check tooling is configured in-repo. After a code change:

1. Run the test suite in an activated CKAN virtualenv:
   `pytest --ckan-ini=<test.ini> ckanext/officedocs/tests`
   (see `mem:suggested_commands` for the test.ini caveat).
2. If default supported formats changed, verify the format-list sync rule in
   `mem:conventions` (plugin.py + two README lists).
3. Template/JS changes can't be unit-tested here — verify manually in-browser
   (public iframe path; private fallback in Chromium vs non-Chromium).
