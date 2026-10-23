# Reproduce and check the scientific record

The [experiment guide](README.md) explains the physical model, sampling, exact resource counts and limitations. The wrapper below runs that same experiment and checks the new output against its committed reference. It does not change the estimator, schedules, seeds, shot counts or scientific claims.

## One-command check

Use Python 3.12 or later. From the repository root, install the [pinned numerical dependencies](requirements.txt), then run:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The wrapper checks the canonical file layout, local Markdown links and anchors, code-fence closure, inline-math delimiter pairing, and the ordered M01–M30 map with its 11/19 phase allocation, required fields, earlier dependencies and selected Nielsen–Chuang anchor. It then runs [verify_protocol.py](verify_protocol.py) with the default configuration and compares every scientific result field with [expected/protocol.json](expected/protocol.json).

Integer counts, Boolean outcomes, seeds, strings and record structure must agree exactly. Floating-point results use absolute tolerance `2e-9` and relative tolerance `2e-6` through `math.isclose`. These are numerical regression tolerances, not additional physical error budgets. Only the top-level environment record and wall-clock runtime are excluded from comparison; both recorded and current environments are printed. A new run never overwrites the reference. Generated JSON and captured simulator output go under the ignored `verification/generated/` directory. A mismatch or failed simulation exits with nonzero status.

For a structural check without installing numerical dependencies:

```bash
python3 verification/run_all.py --structure-only
```

This option explicitly skips numerical reproduction. Tests of the checker itself run with:

```bash
python3 -m unittest discover -s verification -p 'test_*.py' -v
```

The [continuous-integration workflow](../.github/workflows/verify.yml) uses Python 3.12 and the pinned numerical dependencies to run these checks on pull requests and updates to `main`. Its repository permission is read-only, and it does not publish results, modify source files or create releases.

## What a pass means

A pass confirms consistency with the stored finite experiment and the checked navigation and learning-map structure. It includes all twelve predetermined seeds, the recorded smaller-shot failures and the explicit physical resource counts. It is not independent replication by another researcher, a proof of the analytical theorem, a guarantee for arbitrary random seeds or evidence of a hardware advantage.

The link checker covers the repository's existing inline and reference-link syntax and heading conventions; it is not a complete Markdown parser. It does not contact external sites. Source attribution, theorem assumptions, conceptual teaching quality and actual hosted mathematical rendering require separate review. Source syntax checks alone cannot certify the appearance of GitHub's renderer.
