#!/usr/bin/env python3
"""One changelog, and nothing that keeps its own.

Every skill used to state a version and carry a changelog, and the rubric did
too, so a release meant editing the same number in five files and a test existed
to catch the one that got missed. The package moves as a whole, so it is counted
as a whole: `CHANGELOG.md` at the root, and the files themselves say nothing
about versions.

That turns the old check inside out. What used to be "these numbers agree" is
now "no file carries a number to disagree with", which is the invariant the new
shape actually rests on — a version line reappearing in a SKILL.md is how the
five-place bookkeeping comes back.
"""

import re
import unittest

from rubric_source import README, ROOT, SKILL_NAMES, RUBRIC, LEARNING, skill_file

CHANGELOG = ROOT / "CHANGELOG.md"

RELEASE = re.compile(r"^## (\d+)\.(\d+)$", re.MULTILINE)

#: Files that ship to a machine. None of them may keep its own bookkeeping.
SHIPPED = [skill_file(name) for name in SKILL_NAMES] + [RUBRIC, LEARNING]


class ChangelogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CHANGELOG.read_text(encoding="utf-8")

    def releases(self) -> "list[tuple[int, int]]":
        return [(int(major), int(minor)) for major, minor in RELEASE.findall(self.text)]

    def test_the_changelog_lists_releases_newest_first(self):
        releases = self.releases()
        self.assertGreater(len(releases), 1, "a changelog with one entry is a version line")
        self.assertEqual(len(set(releases)), len(releases), f"a release is listed twice: {releases}")
        self.assertEqual(releases, sorted(releases, reverse=True), releases)

    def test_every_release_says_what_changed(self):
        sections = RELEASE.split(self.text)[1:]
        # split() gives major, minor, body, major, minor, body, ...
        for major, minor, body in zip(sections[::3], sections[1::3], sections[2::3]):
            with self.subTest(release=f"{major}.{minor}"):
                self.assertTrue(
                    [line for line in body.splitlines() if line.startswith("- ")],
                    f"{major}.{minor} has no entries",
                )

    def test_the_newest_release_names_the_skills_it_changed(self):
        """An entry that does not say which skill moved is a note to nobody."""
        newest = RELEASE.split(self.text)[3]
        for name in ("agentic-coding-rubric", "advise-me", "review-my-work"):
            with self.subTest(skill=name):
                self.assertIn(f"**{name}**", newest)

    def test_nothing_that_ships_carries_a_version_or_a_changelog_of_its_own(self):
        for path in SHIPPED + [README]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                for stale in ("Skill version", "rubric version", "## Changelog"):
                    self.assertNotIn(stale, text, f"{path} keeps its own bookkeeping again")


if __name__ == "__main__":
    unittest.main()
