#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from strip_repository_stats import FORK_PATH, STAR_PATH, remove_repository_stats


class RemoveRepositoryStatsTests(unittest.TestCase):
    def make_svg(self):
        return f"""<svg xmlns="http://www.w3.org/2000/svg">
<g>
  <text>952 contributions</text>
  <g><path d="{STAR_PATH}"/></g>
  <text><title>135</title>135</text>
  <g><path d="{FORK_PATH}"/></g>
  <text><title>14</title>14</text>
  <text>2026-01-01 / 2026-12-31</text>
</g>
</svg>"""

    def test_removes_star_and_fork_blocks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            svg_path = Path(temp_dir) / "profile.svg"
            svg_path.write_text(self.make_svg(), encoding="utf-8")

            self.assertEqual(remove_repository_stats(svg_path), 2)
            output = svg_path.read_text(encoding="utf-8")

            self.assertNotIn(STAR_PATH, output)
            self.assertNotIn(FORK_PATH, output)
            self.assertNotIn("<title>135</title>", output)
            self.assertNotIn("<title>14</title>", output)
            self.assertIn("952 contributions", output)
            self.assertIn("2026-01-01 / 2026-12-31", output)

    def test_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            svg_path = Path(temp_dir) / "profile.svg"
            svg_path.write_text(self.make_svg(), encoding="utf-8")

            self.assertEqual(remove_repository_stats(svg_path), 2)
            self.assertEqual(remove_repository_stats(svg_path), 0)


if __name__ == "__main__":
    unittest.main()
