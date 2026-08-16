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

from rubric_source import README, ROOT, RUNNABLE_SKILLS, RUBRIC, LEARNING, skill_file

CHANGELOG = ROOT / "CHANGELOG.md"
CRITERIA = ROOT / "CRITERIA.md"

#: Every `::name` in CRITERIA.md is a promise that a test by that name guards
#: the point above it.
GUARD = re.compile(r"::([A-Za-z_][A-Za-z0-9_]*)")


class CriteriaGuardTests(unittest.TestCase):
    """CRITERIA.md is this package's own map from a claim to the test that
    holds it down, which makes a name in it that no longer resolves the exact
    false green the rubric's C7 warns about: the page still reads as covered.
    It happened twice in one sitting — a test renamed when the question ceiling
    moved, another deleted when the diff-basis rule moved into the rubric — and
    the suite stayed green through both, because nothing was reading this file.
    Now something is."""

    def test_every_test_named_in_the_criteria_exists(self):
        defined = set()
        for path in (ROOT / "evals").glob("test_*.py"):
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                for keyword in ("def ", "class "):
                    if stripped.startswith(keyword):
                        defined.add(stripped[len(keyword):].split("(")[0].split(":")[0])
        for name in GUARD.findall(CRITERIA.read_text(encoding="utf-8")):
            with self.subTest(guard=name):
                self.assertIn(name, defined, f"CRITERIA.md names {name}, which no test defines")


RELEASE = re.compile(r"^## (\d+)\.(\d+)$", re.MULTILINE)

#: The history of the reviewer these skills came out of, kept at the foot of the
#: file. Each line is one version step of one of its two tracks.
HISTORY = "## Before these skills"
TRACK = re.compile(r"^### (.+)$", re.MULTILINE)
STEP = re.compile(r"^- \*\*v(\S+) → v(\S+)\*\*", re.MULTILINE)

#: Files that ship to a machine. None of them may keep its own bookkeeping.
SHIPPED = [skill_file(name) for name in RUNNABLE_SKILLS] + [RUBRIC, LEARNING]


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
        named = [
            name
            for name in ("references", "advise-me", "review-my-work")
            if f"**{name}**" in newest
        ]
        self.assertTrue(named, "the newest release names no skill")

    def test_the_history_comes_after_the_releases_and_leaves_no_gap(self):
        """A dropped step is the one way a compressed history misleads."""
        head, _, history = self.text.partition(HISTORY)
        self.assertTrue(history, f"{HISTORY} is gone")
        self.assertFalse(RELEASE.search(history), "a release is listed under the history")
        self.assertTrue(RELEASE.search(head), "the history swallowed the releases")
        tracks = TRACK.split(history)[1:]
        self.assertTrue(tracks, "the history names no track")
        for name, body in zip(tracks[::2], tracks[1::2]):
            with self.subTest(track=name):
                steps = STEP.findall(body)
                self.assertGreater(len(steps), 1, f"{name} lists no chain")
                for (_, older), (newer, _) in zip(steps[1:], steps):
                    self.assertEqual(older, newer, f"{name} skips from {older} to {newer}")

    def test_nothing_that_ships_carries_a_version_or_a_changelog_of_its_own(self):
        for path in SHIPPED + [README]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                for stale in ("Skill version", "rubric version", "## Changelog"):
                    self.assertNotIn(stale, text, f"{path} keeps its own bookkeeping again")


if __name__ == "__main__":
    unittest.main()
