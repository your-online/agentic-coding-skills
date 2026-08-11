#!/usr/bin/env python3
"""Who judges, and on what.

Both rules protect the same thing: a review that is worth less than it looks.
An agent grading the session it worked in has every prior conclusion in context
and will confirm itself; a reviewer quietly demoted to a lighter model returns
thinner challenges and softer findings, and the report reads exactly the same
either way. Neither failure announces itself, so both are written down as hard
stops — run nothing and say so — rather than as preferences.
"""

import unittest

from rubric_source import SKILL


class IsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = " ".join(SKILL.read_text(encoding="utf-8").split())

    def test_the_main_agent_never_reviews_its_own_session(self):
        self.assertIn("Never judge your own work", self.text)
        self.assertIn("does not review the session it worked in", self.text)
        self.assertIn("subagent with fresh context", self.text)

    def test_the_reviewer_gets_raw_sources_and_no_expected_outcome(self):
        self.assertIn("no expected outcome", self.text)
        self.assertIn("no earlier conclusion", self.text)
        self.assertIn("no summary you wrote yourself", self.text)
        self.assertIn("hand the subagent the complete", self.text)

    def test_missing_isolation_stops_the_review_instead_of_downgrading_it(self):
        self.assertIn("If an isolated subagent cannot be spawned, say so and run nothing",
                      self.text)

    def test_every_reviewing_role_is_pinned_to_one_of_two_named_models(self):
        for role in ("the reviewer, the falsifier, the feedback subagent",):
            self.assertIn(role, self.text)
        self.assertIn("Opus 5 (`claude-opus-5`)", self.text)
        self.assertIn("Opus 4.8 (`claude-opus-4-8`)", self.text)
        self.assertIn("There is no third option", self.text)

    def test_an_unavailable_or_limited_model_is_a_hard_visible_failure(self):
        self.assertIn("usage limits block them", self.text)
        self.assertIn("fail hard", self.text)
        self.assertIn("run nothing and tell the developer", self.text)
        self.assertIn(
            "the review cannot run with the available models or under the current limits",
            self.text,
        )
        self.assertIn("Never quietly continue on a lighter model", self.text)


if __name__ == "__main__":
    unittest.main()
