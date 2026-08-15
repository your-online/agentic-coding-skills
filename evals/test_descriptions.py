#!/usr/bin/env python3
"""Three descriptions that must not compete for the same request.

A skill description is a trigger, not a summary. Version 1.0 was one skill whose
description carried both routes and read almost word for word like another
review skill already installed in the field — "review agentic coding work",
"feedback on your approach" — so the platform had two candidates for one
sentence and the developer had no way to tell which one answered. Splitting into
three makes that worse unless each description matches exactly one request, so:
every skill names its own trigger phrases, the two reviewing skills say out loud
what the other one is for, and no distinguishing marker appears in more than one
description.
"""

import unittest

from rubric_source import RUNNABLE_SKILLS, frontmatter_description

#: Words that decide which skill a request belongs to. Each may appear in one
#: description only — as its own marker, not as a mention of a sibling.
MARKERS = {
    "advise-me": ("in chat", "before any code exists", "how am I doing"),
    "review-my-work": ("Markdown report", "review this session", "the session that just ran"),
    "log-feedback": ("docs/feedback.md", "dated bullet", "log this"),
}

#: Vocabulary of the spreadsheet-producing review skill this one shares a field
#: with. Naming it here would put both in the running for the same request.
FOREIGN = ("Excel", "workbook", "three-sheet", "acceptance-criteria quality",
           "adversarial falsification", "before handoff")


class DescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.descriptions = {name: frontmatter_description(name) for name in RUNNABLE_SKILLS}

    def test_every_skill_carries_its_own_markers(self):
        for name, markers in MARKERS.items():
            for marker in markers:
                with self.subTest(skill=name, marker=marker):
                    self.assertIn(marker, self.descriptions[name])

    def test_no_marker_appears_in_a_sibling_description(self):
        for owner, markers in MARKERS.items():
            for other in RUNNABLE_SKILLS:
                if other == owner:
                    continue
                for marker in markers:
                    with self.subTest(marker=marker, found_in=other):
                        self.assertNotIn(marker, self.descriptions[other])

    def test_the_two_reviewing_skills_send_the_other_request_to_each_other(self):
        self.assertIn("advise-me skill is for", self.descriptions["review-my-work"])
        self.assertIn("review-my-work skill is for", self.descriptions["advise-me"])

    def test_the_logging_skill_cannot_be_read_as_a_review(self):
        text = self.descriptions["log-feedback"]
        self.assertIn("never produces feedback for the developer", text)
        self.assertIn("never judges their work", text)

    def test_no_description_borrows_the_neighbouring_review_skills_vocabulary(self):
        for name, text in self.descriptions.items():
            for word in FOREIGN:
                with self.subTest(skill=name, word=word):
                    self.assertNotIn(word.lower(), text.lower())

    def test_every_description_says_when_to_use_it_with_real_phrasing(self):
        for name, text in self.descriptions.items():
            with self.subTest(skill=name):
                self.assertIn("Use only when", text)
                self.assertIn('"', text, "no example request the developer would type")


if __name__ == "__main__":
    unittest.main()
