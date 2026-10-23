"""Regression tests for the checker, independent of the scientific simulator."""
from copy import deepcopy
import tempfile
from pathlib import Path
import unittest

from run_all import (anchors, check_links, compare, prose, check_shape,
                     check_sampled_consistency, deterministic_projection)


class CheckerTests(unittest.TestCase):
    def test_ignored_metadata(self):
        compare({"environment": {"python": "old"}, "runtime_seconds": 1.0, "x": [1, True, 0.3]},
                {"environment": {"python": "new"}, "runtime_seconds": 2.0, "x": [1, True, 0.3]})

    def test_float_tolerance(self):
        compare({"x": 0.0005}, {"x": 0.0005000001})
        with self.assertRaises(ValueError):
            compare({"x": 0.0005}, {"x": 0.0006})

    def test_integer_and_boolean_are_exact(self):
        for actual in (2, 1.0, True):
            with self.subTest(actual=actual), self.assertRaises(ValueError):
                compare({"x": 1}, {"x": actual})

    def test_missing_key_or_seed(self):
        with self.assertRaises(ValueError):
            compare({"seeds": [1, 2]}, {"seeds": [1]})
        with self.assertRaises(ValueError):
            compare({"seeds": [1, 2]}, {})

    def test_nonfinite_rejected(self):
        for actual in (float("nan"), float("inf")):
            with self.subTest(actual=actual), self.assertRaises(ValueError):
                compare({"x": 1.0}, {"x": actual})

    def test_headings_and_explicit_anchors(self):
        found = anchors('# A title\n## More: things\n<a id="m01"></a>\n## More: things\n')
        self.assertTrue({"a-title", "more-things", "more-things-1", "m01"} <= found)

    def test_code_fences(self):
        self.assertNotIn("hidden", prose('A\n```python\nhidden\n```\nB'))
        with self.assertRaises(ValueError):
            prose('A\n```math\nx')

    def test_local_navigation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text('[A](topic.md#target)\n[B][r]\n[r]: topic.md\n')
            (root / "topic.md").write_text('# Target\n')
            self.assertEqual(check_links(root), (2, 2))
            (root / "topic.md").write_text('# Changed\n')
            with self.assertRaises(ValueError):
                check_links(root)

    def test_missing_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text('[A][missing]\n')
            with self.assertRaises(ValueError):
                check_links(root)


def sampled_fixture():
    row = dict(uniform_waveform_error=0.2, per_term_error={"X": 0.2},
               max_exact_transfer_standard_error=0.01, maintained_input_bound=1.0,
               output_bound=0.5, error_over_input_bound=0.2,
               error_over_previous_actual_error=0.5, within_next_bound=True,
               unknown_prefix_queries=100)
    trial = dict(seed=1, initial_uniform_error=0.4, history=[row],
                 final_uniform_error=0.2, all_stages_within_maintained_bounds=True,
                 learned_endpoint_operator_error=0.1, learned_chebyshev_coefficients=[[0.2]],
                 waveform_samples={"learned": [[0.2]], "truth": [[0.0]]},
                 total_unknown_prefix_queries=100)
    summary = dict(count=1, seeds=[1], all_stage_bound_successes=1,
                   final_error_min=0.2, final_error_median=0.2, final_error_max=0.2,
                   final_errors=[0.2], stage_errors_by_trial=[[0.2]])
    return dict(finite_shot_example=trial, finite_shot_repetition_summary=summary,
                shot_budget_sweep=[dict(shots_per_prefix_per_stage=10,
                    all_stage_bounds_held=True, final_error=0.2,
                    error_over_final_target_bound=0.4)], algebra_checks={"error": 1e-12})


class PortableResultTests(unittest.TestCase):
    def test_sampled_record_consistency(self):
        check_sampled_consistency(sampled_fixture())

    def test_projection_changes_only_sampled_values(self):
        expected = sampled_fixture()
        actual = deepcopy(expected)
        actual["finite_shot_example"]["learned_endpoint_operator_error"] = 0.3
        check_shape(expected, actual)
        compare(deterministic_projection(expected), deterministic_projection(actual))
        with self.assertRaises(ValueError):
            compare(expected, actual)

    def test_deterministic_and_resource_changes_rejected(self):
        expected = sampled_fixture()
        for container, key in (("algebra_checks", "error"),
                               ("finite_shot_example", "total_unknown_prefix_queries")):
            actual = deepcopy(expected)
            actual[container][key] += 1
            with self.subTest(key=key), self.assertRaises(ValueError):
                compare(deterministic_projection(expected), deterministic_projection(actual))

    def test_malformed_sampled_values_rejected(self):
        expected = sampled_fixture()
        for value in (float("nan"), "not a number"):
            actual = deepcopy(expected)
            actual["finite_shot_example"]["final_uniform_error"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                check_shape(expected, actual)

    def test_contradictory_summary_rejected(self):
        actual = sampled_fixture()
        actual["finite_shot_repetition_summary"]["all_stage_bound_successes"] = 0
        with self.assertRaises(ValueError):
            check_sampled_consistency(actual)


if __name__ == "__main__":
    unittest.main()
