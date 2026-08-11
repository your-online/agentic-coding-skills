#!/usr/bin/env python3
"""The rubric speaks human, not machine.

Verdict labels, criticality keywords, gates and percentages are how the previous
rubric turned into a scoring instrument: once a criterion can be PASS or FAIL,
the feedback collapses into a label and the reader stops reading the sentence.
This rubric deliberately has none of that vocabulary, and the ban is worth a
test because it erodes one word at a time. The detector is checked against
planted violations first, so a green run here means the detector still bites.
"""

import re
import unittest

from rubric_source import RUBRIC, rubric_text

MACHINE_WORDS = (
    "PASS", "PARTIAL", "FAIL", "UNKNOWN", "PENDING",
    "MUST", "SHOULD", "CONDITIONAL",
)
PLAIN_WORDS = ("criticality", "gate", "gates", "score", "scores", "scored", "scoring")

PATTERNS = (
    [re.compile(rf"\b{word}\b") for word in MACHINE_WORDS]
    + [re.compile(rf"\b{word}\b", re.IGNORECASE) for word in PLAIN_WORDS]
    + [re.compile(r"\bN/A\b"), re.compile(r"\d\s*%")]
)


def violations(text: str) -> "list[str]":
    found = []
    for line in text.splitlines():
        for pattern in PATTERNS:
            match = pattern.search(line)
            if match:
                found.append(f"{match.group(0)!r} in: {line.strip()[:90]}")
    return found


class RubricLanguageTests(unittest.TestCase):
    def test_the_detector_catches_planted_violations(self):
        planted = [
            "- **PASS:** every material criterion has evidence.",
            "Criticality: MUST. Gate: G-PROOF.",
            "A SHOULD stays diagnostic and may be PARTIAL.",
            "Not applicable, so N/A.",
            "Evidence quality is 87% of the maximum.",
            "The scorer awards a score of 2 per criterion.",
            "This one is UNKNOWN and that one is FAIL.",
        ]
        for line in planted:
            with self.subTest(line=line):
                self.assertTrue(violations(line), f"detector missed: {line}")

    def test_the_detector_does_not_fire_on_ordinary_prose(self):
        for line in (
            "The work is grounded in the situation it actually lands in.",
            "A check that cannot go red proves nothing, so failure has to be shown.",
            "Which parts of the existing system did the work inspect?",
        ):
            with self.subTest(line=line):
                self.assertEqual(violations(line), [])

    def test_the_rubric_is_free_of_machine_vocabulary(self):
        found = violations(rubric_text())
        self.assertEqual(found, [], f"{RUBRIC} uses machine vocabulary: {found}")


if __name__ == "__main__":
    unittest.main()
