#!/usr/bin/env python3
"""Review My Work follows a work item across chat-session boundaries."""

import unittest

from rubric_source import flat, skill_text


class MultiSessionSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = flat(skill_text("review-my-work"))
        cls.advice = flat(skill_text("advise-me"))

    def test_the_current_session_is_a_starting_point_not_the_source_boundary(self):
        self.assertIn("The current session is the starting point, not the source boundary", self.review)
        self.assertIn("Before spawning the reviewer", self.review)
        for platform in ("Codex", "Claude Code", "Cursor"):
            with self.subTest(platform=platform):
                self.assertIn(platform, self.review)

    def test_discovery_checks_metadata_before_reading_other_transcripts(self):
        self.assertIn("Search session metadata or indexes first", self.review)
        self.assertIn("Only read another transcript after it becomes a plausible candidate", self.review)

    def test_matching_needs_one_unique_or_two_independent_signals(self):
        self.assertIn("one unique work-item identifier", self.review)
        self.assertIn("at least two independent weaker signals", self.review)
        self.assertIn("The same repository alone is never enough", self.review)
        for signal in ("repository or worktree", "branch, commit or pull request", "distinctive files or commands"):
            with self.subTest(signal=signal):
                self.assertIn(signal, self.review)

    def test_material_ambiguity_causes_one_question_instead_of_a_guess(self):
        self.assertIn("Ask once", self.review)
        self.assertIn("could materially change the review", self.review)
        self.assertIn("session ID, platform and matching signals", self.review)

    def test_included_sessions_are_raw_and_auditable(self):
        self.assertIn("raw transcript of every included session", self.review)
        self.assertIn("never a summary written from them", self.review)
        self.assertIn("session ID, platform and inclusion reason", self.review)

    def test_unreachable_history_only_reduces_affected_criteria(self):
        self.assertIn("Name an unreachable history source", self.review)
        self.assertIn("mark only the criteria it could affect as `unknown`", self.review)
        self.assertIn("Do not lower assessability mechanically", self.review)

    def test_advise_me_does_not_inherit_the_cross_session_search(self):
        self.assertNotIn("session metadata or indexes", self.advice)
        self.assertNotIn("one unique work-item identifier", self.advice)


if __name__ == "__main__":
    unittest.main()
