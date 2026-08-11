#!/usr/bin/env python3
"""A criterion is three parts, in one order, or it is not a criterion.

The shape is the whole promise of this rubric: say what has to be true, offer
ways to get there without demanding any of them, and hand the reviewer the
questions that decide it. Drop the guidance and the requirement hardens into a
procedure; drop the questions and every reviewer invents their own bar. So the
three parts, their order, and a usable number of questions are checked, and the
criterion count is held near ten — a rubric that grows back to twenty-two is a
different product.
"""

import unittest

from rubric_source import PARTS, criteria, evaluation_questions, rubric_text


class RubricShapeTests(unittest.TestCase):
    def setUp(self):
        self.criteria = criteria()

    def test_the_rubric_stays_compact(self):
        self.assertTrue(8 <= len(self.criteria) <= 10, len(self.criteria))
        ids = [cid for cid, _, _ in self.criteria]
        self.assertEqual(ids, sorted(ids, key=lambda c: int(c[1:])))
        self.assertEqual(len(set(ids)), len(ids))

    def test_every_criterion_has_the_three_parts_exactly_once_and_in_order(self):
        for cid, title, body in self.criteria:
            with self.subTest(criterion=cid):
                self.assertTrue(title.strip())
                positions = []
                for part in PARTS:
                    self.assertEqual(body.count(part), 1, f"{cid} misses or repeats {part}")
                    positions.append(body.index(part))
                self.assertEqual(positions, sorted(positions), f"{cid} has the parts out of order")

    def test_every_part_actually_says_something(self):
        for cid, _, body in self.criteria:
            with self.subTest(criterion=cid):
                requirement = body.split(PARTS[0], 1)[1].split(PARTS[1], 1)[0]
                guidance = body.split(PARTS[1], 1)[1].split(PARTS[2], 1)[0]
                self.assertGreater(len(requirement.split()), 25, f"{cid} requirement is a stub")
                self.assertGreater(len(guidance.split()), 40, f"{cid} guidance is a stub")

    def test_each_criterion_asks_two_to_four_evaluation_questions(self):
        for cid, _, body in self.criteria:
            with self.subTest(criterion=cid):
                questions = evaluation_questions(body)
                self.assertTrue(2 <= len(questions) <= 4, f"{cid} has {len(questions)} questions")

    def test_guidance_is_offered_and_never_demanded(self):
        """The line between this rubric and a standard is that guidance suggests."""
        text = rubric_text()
        self.assertIn("Suggestions and patterns, never demands", text)
        self.assertIn("It does not say how you get there", text)
        # The two working methods that inspired C9 and C8 stay examples.
        self.assertIn("offered as an example and not as a step to follow", text)


if __name__ == "__main__":
    unittest.main()
