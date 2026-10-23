"""Regression tests for the checker, independent of the scientific simulator."""
import tempfile
from pathlib import Path
import unittest

from run_all import anchors, check_links, compare, prose


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


if __name__ == "__main__":
    unittest.main()
