#!/usr/bin/env python3
"""Two routes that must stay two routes.

The cheap failure here is convergence: route 2 grows a report file, or route 1
loses its falsifier because one pass looked good enough. They answer different
questions — one judges what was built, the other advises on what to do next —
and the differences that carry that split are the file, the falsifier, and
whether a diff is required at all. The diff basis is checked separately: a
review of the wrong range is worse than no review, and only the developer can
spot that, which they can only do if the report says which range it used.
"""

import unittest

from rubric_source import SKILL


def flat(text: str) -> str:
    """Line wrapping is not part of the contract; the wording is."""
    return " ".join(text.split())


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = SKILL.read_text(encoding="utf-8")
        cls.text = flat(text)
        cls.route1 = flat(text.split("## Route 1 — Full review", 1)[1].split("## Route 2", 1)[0])
        cls.route2 = flat(
            text.split("## Route 2 — Feedback on your approach", 1)[1]
            .split("## Maintaining this skill", 1)[0]
        )

    def test_neither_route_ever_triggers_itself(self):
        self.assertIn("Both run only when the developer asks for them by name", self.text)
        self.assertIn("Never start either one on your own initiative", self.text)
        self.assertIn("never infer from the state of the work that a review is due", self.text)

    def test_only_the_full_review_writes_a_file(self):
        self.assertIn("One Markdown file", self.route1)
        self.assertIn("docs/reviews/agentic-coding-review-", self.route1)
        self.assertIn("Never overwrite an existing report", self.route1)
        self.assertIn("The developer chooses where it goes", self.route1)
        self.assertIn("Write no file", self.route2)
        self.assertIn("in chat only", self.route2)
        self.assertNotIn("Markdown file", self.route2)

    def test_only_the_full_review_runs_a_falsifier_and_exactly_one_revision(self):
        self.assertIn("Spawn one falsifier", self.route1)
        self.assertIn("exactly one revision", self.route1)
        self.assertIn("No falsifier, no revision round", self.route2)

    def test_the_diff_is_required_in_route_one_and_optional_in_route_two(self):
        self.assertIn("as a diff", self.route1)
        self.assertIn("The diff is optional", self.route2)
        self.assertIn("this route is also used before any code exists", self.route2)

    def test_route_two_looks_forward_instead_of_judging(self):
        self.assertIn("forward-looking", self.route2)
        self.assertIn("Not a verdict on what has happened", self.route2)

    def test_the_diff_basis_is_derived_and_always_reported(self):
        self.assertIn("Is there uncommitted work? Then diff against `HEAD`", self.route1)
        self.assertIn("the commit this session or task started from", self.route1)
        self.assertIn("`HEAD~n`", self.route1)
        self.assertIn("State the basis in the report, always", self.route1)
        self.assertIn("Diff basis: <ref> (<why>)", self.route1)

    def test_the_report_stays_free_form_and_unlabelled(self):
        self.assertIn("The form is free", self.route1)
        self.assertIn("Do not attach a label to each criterion", self.route1)
        self.assertIn("do not put a percentage anywhere", self.route1)
        self.assertIn("what is good, what is weak, what is missing", self.route1)

    def test_the_stripped_machinery_stays_stripped(self):
        self.assertIn(
            "There is no orchestrator layer, no scorer, no validator and no snapshot ceremony.",
            self.route1,
        )


if __name__ == "__main__":
    unittest.main()
