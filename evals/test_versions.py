#!/usr/bin/env python3
"""One version, stated in every file that claims it.

Feedback is only comparable if you can tell which rubric produced it. There is
no version file and no manifest here on purpose — three files each name the
version in prose, and this test is what keeps those three from drifting apart.
It also insists the version has a changelog line, because a bumped number with
nothing said about it is the in-place edit the maintenance rule forbids.
"""

import re
import unittest

from rubric_source import LEARNING, README, RUBRIC, SKILL, criteria, rubric_text

VERSION = re.compile(r"\d+\.\d+")


class VersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rubric = rubric_text()
        cls.skill = " ".join(SKILL.read_text(encoding="utf-8").split())
        cls.readme = " ".join(README.read_text(encoding="utf-8").split())

    def rubric_version(self) -> str:
        heading = self.rubric.splitlines()[0]
        self.assertIn("Agentic coding rubric — version", heading)
        return VERSION.search(heading).group(0)

    def test_the_skill_and_readme_name_the_rubric_version_the_rubric_carries(self):
        version = self.rubric_version()
        self.assertIn(f"using rubric version {version}", self.skill)
        self.assertIn(f"rubric version {version}", self.readme)

    def test_the_skill_version_matches_the_readme(self):
        skill_version = re.search(r"Skill version (\d+\.\d+)", self.skill).group(1)
        self.assertIn(f"Skill version {skill_version}", self.readme)

    def test_the_current_rubric_version_has_a_changelog_line(self):
        changelog = self.rubric.split("## Changelog", 1)[1]
        self.assertIn(f"**{self.rubric_version()}**", changelog)

    def test_the_learning_materials_cover_every_criterion(self):
        text = LEARNING.read_text(encoding="utf-8")
        headings = " ".join(re.findall(r"^## .+$", text, re.MULTILINE))
        for cid, _, _ in criteria():
            with self.subTest(criterion=cid):
                self.assertRegex(headings, rf"\b{cid}\b")

    def test_nothing_here_points_outside_the_publishable_tree(self):
        """Publication is a copy of this directory; a path out of it breaks that."""
        for path in (RUBRIC, SKILL, README, LEARNING):
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                for stale in ("evaluate-acbp", "../../", "slim/"):
                    self.assertNotIn(stale, text)


if __name__ == "__main__":
    unittest.main()
