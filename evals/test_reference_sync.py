#!/usr/bin/env python3
"""One rubric, copied twice, and never allowed to drift.

`advise-me` and `review-my-work` both need the rubric, and a skill has to be
installable on its own — so a symlink or an include is out, and the copies are
real files. That is a duplication with a known failure mode: someone fixes a
criterion in the skill they happen to have open, the other skill keeps the old
wording, and two developers get feedback from two rubrics that both claim to be
version 1.0. There is no build step to prevent that; this test is the
prevention. `references/` is the source, the skills carry copies, and a
one-byte difference is a red run.

log-feedback records what the developer says about the process. It judges
nothing, so it has no business carrying the rubric, and a copy appearing there
is drift of a different kind.
"""

import unittest

from rubric_source import (
    REFERENCE_FILES,
    REFERENCES,
    RUBRIC_SKILLS,
    SKILLS_DIR,
    SKILL_NAMES,
)


class ReferenceSyncTests(unittest.TestCase):
    def test_the_copies_are_byte_identical_to_the_source(self):
        for skill in RUBRIC_SKILLS:
            for name in REFERENCE_FILES:
                with self.subTest(skill=skill, file=name):
                    source = REFERENCES / name
                    copy = SKILLS_DIR / skill / "references" / name
                    self.assertTrue(copy.is_file(), f"{copy} is missing")
                    self.assertEqual(
                        copy.read_bytes(),
                        source.read_bytes(),
                        f"{copy} has drifted from {source}; copy the source over it",
                    )

    def test_the_source_holds_exactly_the_two_reference_files(self):
        self.assertEqual(
            sorted(p.name for p in REFERENCES.iterdir()), sorted(REFERENCE_FILES)
        )

    def test_the_skills_carry_no_reference_the_source_does_not_have(self):
        for skill in RUBRIC_SKILLS:
            with self.subTest(skill=skill):
                present = sorted(p.name for p in (SKILLS_DIR / skill / "references").iterdir())
                self.assertEqual(present, sorted(REFERENCE_FILES))

    def test_the_feedback_log_carries_no_rubric(self):
        self.assertFalse((SKILLS_DIR / "log-feedback" / "references").exists())

    def test_the_repository_holds_exactly_the_three_skills(self):
        self.assertEqual(sorted(p.name for p in SKILLS_DIR.iterdir()), sorted(SKILL_NAMES))


if __name__ == "__main__":
    unittest.main()
