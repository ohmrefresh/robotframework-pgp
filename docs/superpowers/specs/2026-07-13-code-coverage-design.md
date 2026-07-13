# Design: Improve code coverage (78% → 100%)

**Date:** 2026-07-13
**Status:** Implemented

## Goal

Raise unit-test coverage of `src/RobotFrameworkPGP` from 78% to 95%+ and enforce a
minimum threshold so it cannot regress.

## Starting point

After the mixin refactor, coverage per module was:

| Module | Coverage | Gap |
|--------|----------|-----|
| `_keys.py` | 55% | error-raise branches, `import_key_from_file`, all of `delete_key` |
| `_info.py` | 65% | `get_gpg_version` fallback branches |
| `_signing.py` | 93% | sign-failure raise |
| `_base.py`, `_crypto.py`, `pgp_library.py` | 100% | — |

The real `delete_key` test had been commented out due to long-standing flakiness
(see `debug_delete.py`).

## Decisions

- **Target:** ~95%+ (achieved 100%).
- **Style:** mix — realistic failures (unknown key ids, garbage key data,
  fingerprint-addressed deletion) run against the real `gpg` binary in
  `tests/test_pgp_library.py`; branches unreachable with a real binary
  (`gen_key` returning falsy, `import_keys` count 0, deletion-failure raises,
  `get_gpg_version` fallbacks) are mocked in the new `tests/test_error_paths.py`
  by patching `RobotFrameworkPGP._base.gnupg.GPG`.
- **delete_key:** re-enabled real tests. Secret keys are addressed by
  fingerprint (GnuPG 2.1+ rejects deletion of secret keys by email).
- **Gate:** `[tool.coverage.report] fail_under = 90` in `pyproject.toml` —
  headroom below the achieved 100% so small future changes don't break CI.

## Bug found and fixed

Re-enabling the real deletion test exposed the actual bug behind the
commented-out test: `gpg --delete-secret-key` does **not** delete the public
key, but `delete_key` assumed it did, leaving the public key behind and passing
silently (the post-check tolerated `status == "ok"`). Fix in `_keys.py`: when a
key has a secret part and `secret=False`, delete the secret key first, then the
public key.

## Known limitation

`tests/conftest.py` skips *all* tests when no `gpg` binary is present,
including the mock-based ones that don't need it. Left unchanged — narrowing
the skip to `requires_gpg`-marked tests would unskip real-gpg tests on
gpg-less machines and needs its own pass.

## Verification (all passing)

- `pytest`: 38 passed, coverage 100%, `fail_under=90` gate active
- `robot tests/acceptance/`: 20/20 passed
- `flake8` / `mypy src` / `black --check`: clean (no new findings)
