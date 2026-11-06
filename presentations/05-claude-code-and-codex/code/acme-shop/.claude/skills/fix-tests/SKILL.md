---
name: fix-tests
description: Fix failing tests. Use when a pytest run fails.
---
1. Run `python -m pytest -q` and read the first failure.
2. Fix the cause in the source code. Never edit `tests/`.
3. Re-run the tests. Stop after three tries.
4. Reply in one line: file, cause, test result.
