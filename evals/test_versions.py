#!/usr/bin/env python3
"""One version, stated in every file that claims it.

Feedback is only comparable if you can tell which rubric produced it. There is
no version file and no manifest here on purpose — the skills and the README each
name the version in prose, and this test is what keeps them from drifting apart.
It also insists a version has a changelog line, because a bumped number with
nothing said about it is the in-place edit the maintenance rule forbids. The
three skills ship together and carry one skill version; splitting them was the
breaking change that made it 2.0.
"""

import re
import unittest

from rubric_source import (
    LEARNING,
    README,
    RUBRIC,
    RUBRIC_SKILLS,
    SKILL_NAMES,
    criteria,
    flat,
    rubric_text,
    skill_file,
    skill_text,
)

VERSION = re.compile(r"\d+\.\d+")


class VersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rubric = rubric_text()
        cls.skills = {name: flat(skill_text(name)) for name in SKILL_NAMES}
        cls.readme = flat(README.read_text(encoding="utf-8"))

    def rubric_version(self) -> str:
        heading = self.rubric.splitlines()[0]
        self.assertIn("Agentic coding rubric — version", heading)
        return VERSION.search(heading).group(0)

    def test_the_rubric_skills_and_the_readme_name_the_rubric_version_it_carries(self):
        version = self.rubric_version()
        for name in RUBRIC_SKILLS:
            with self.subTest(skill=name):
                self.assertIn(f"using rubric version {version}", self.skills[name])
        self.assertIn(f"rubric version {version}", self.readme)

    def test_all_three_skills_carry_the_same_skill_version_as_the_readme(self):
        versions = {}
        for name, text in self.skills.items():
            match = re.search(r"Skill version (\d+\.\d+)", text)
            self.assertIsNotNone(match, f"{name} states no skill version")
            versions[name] = match.group(1)
        self.assertEqual(len(set(versions.values())), 1, versions)
        self.assertIn(f"Skill version {set(versions.values()).pop()}", self.readme)

    def test_every_skill_has_a_changelog_line_for_its_own_version(self):
        for name, text in self.skills.items():
            with self.subTest(skill=name):
                version = re.search(r"Skill version (\d+\.\d+)", text).group(1)
                changelog = text.split("## Changelog", 1)
                self.assertEqual(len(changelog), 2, f"{name} has no changelog")
                self.assertIn(f"**{version}**", changelog[1])

    def test_the_current_rubric_version_has_a_changelog_line(self):
        changelog = self.rubric.split("## Changelog", 1)[1]
        self.assertIn(f"**{self.rubric_version()}**", changelog)

    def test_the_learning_materials_cover_every_criterion(self):
        text = LEARNING.read_text(encoding="utf-8")
        headings = " ".join(re.findall(r"^## .+$", text, re.MULTILINE))
        for cid, _, _ in criteria():
            with self.subTest(criterion=cid):
                self.assertRegex(headings, rf"\b{cid}\b")

    def test_nothing_installed_points_outside_the_skill_that_ships_it(self):
        """A skill is installed on its own: everything it names has to travel
        with it, and nothing may name the repository layout around it."""
        installed = [skill_file(name) for name in SKILL_NAMES]
        installed += [
            skill_file(name).parent / "references" / ref.name
            for name in RUBRIC_SKILLS
            for ref in (RUBRIC, LEARNING)
        ]
        for path in installed:
            with self.subTest(file=str(path.relative_to(skill_file("advise-me").parents[2]))):
                text = path.read_text(encoding="utf-8")
                for stale in ("evaluate-acbp", "../../", "slim/", "evals/", "uvx pytest"):
                    self.assertNotIn(stale, text)


if __name__ == "__main__":
    unittest.main()
