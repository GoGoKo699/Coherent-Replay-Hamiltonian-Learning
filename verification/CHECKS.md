# Reproduce and check the scientific record

The [experiment guide](README.md) explains the physical model, sampling, exact resource counts and limitations. The wrapper below runs that same experiment. It does not change the estimator, schedules, seeds, shot counts or saved scientific results.

## One-command check

Use Python 3.12 or later. From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The wrapper checks the canonical file layout, local Markdown links and anchors, code-fence closure, inline-math delimiter pairing, and the ordered M01–M30 map with its 11/19 phase allocation, required fields, earlier dependencies and selected Nielsen–Chuang anchor. It then runs [verify_protocol.py](verify_protocol.py) twice in separate processes with its default configuration.

## Numerical and stochastic checks are different

The default check requires the following:

1. Deterministic algebra checks, the noiseless reconstruction, endpoint example, exact-expectation diagnostics, configurations, seed lists and physical resource counts agree with [the committed reference](expected/protocol.json).
2. Every result retains the reference's keys, array dimensions and scalar types, with no nonfinite numerical values. Sampled errors, success flags, ratios and summary statistics are internally consistent.
3. All scientific fields, including sampled trajectories, agree between the two fresh runs on the same machine.

Integer resource counts, seeds, strings and deterministic Boolean outcomes are compared exactly. Floating-point comparisons retain absolute tolerance `2e-9` and relative tolerance `2e-6` through `math.isclose`. These are regression tolerances, not physical error budgets. The top-level environment record and wall-clock runtime are reported but are not numerical-match requirements.

The explicit sampled-field whitelist in [run_all.py](run_all.py) contains fitted coefficients, sampled waveform errors and their derived statistics. Those fields may differ from the historical sample across machines. They are still checked for structure, finiteness, internal consistency and repeatability in the current environment. The wrapper also attempts the full historical comparison and prints the first difference when it does not match. It never describes a differing trajectory as reproduction of the stored sample. The observed success count and error range are reported, not used as a new confidence guarantee or a requirement that every stochastic trial succeed.

The complete historical comparison remains available as a stricter command:

```bash
python3 verification/run_all.py --strict-reference
```

This exits with nonzero status if any scientific field differs from the reference beyond the stated tolerances, including stochastic outcomes. A strict mismatch requires diagnosis; it is not automatically evidence of an incorrect distribution or an invalid theorem.

A seed and package pins alone do not promise cross-machine equality of sampled trajectories. NumPy's [random-stream compatibility policy](https://numpy.org/doc/2.3/reference/random/compatibility.html) also conditions reproducibility on the build, environment, machine and exact method arguments. Here multinomial probabilities come from floating-point propagation and matrix operations, and later models depend on earlier samples. Small numerical differences can therefore change later random draws. This is a portability caveat, not permission to omit failures or replace the reference with a favorable run.

The two new outputs and captured simulator logs are saved under the ignored `verification/generated/` directory as `protocol.*` and `protocol.repeat.*`. A fresh run removes stale output first and never overwrites the committed reference. Every structural, deterministic, consistency or same-machine repeatability failure exits with nonzero status. The default cross-machine historical stochastic difference is instead explicitly reported.

## Structural checks and checker tests

For a structural check without numerical dependencies:

```bash
python3 verification/run_all.py --structure-only
```

This explicitly skips numerical reproduction. Tests of the checker itself run with:

```bash
python3 -m unittest discover -s verification -p 'test_*.py' -v
```

The [continuous-integration workflow](../.github/workflows/verify.yml) uses Python 3.12 and the pinned numerical dependencies to run the default checks on pull requests and updates to `main`. Its repository permission is read-only; it does not modify sources or create releases.

## What a pass means

A default pass confirms the checked navigation and learning-map structure, numerical consistency of deterministic quantities, correct resource records, internally consistent sampled reporting, and repetition of the calculation in the current environment. It does not certify a particular stochastic success frequency, independent researcher replication, the analytical theorem, or a hardware advantage. The original twelve-seed reference, including its smaller-shot failures, remains an unchanged record of that run.

The link checker covers the repository's existing inline and reference-link syntax and heading conventions; it is not a complete Markdown parser and does not contact external sites. Source attribution, theorem assumptions, conceptual teaching quality and actual hosted mathematical rendering require separate review. Source syntax checks alone cannot certify GitHub's displayed appearance.
