#!/usr/bin/env python3
"""The small scoring layer used only by review-my-work."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from rubric_source import SKILLS_DIR


REVIEW = SKILLS_DIR / "review-my-work"
CONTRACT = REVIEW / "scoring" / "score-contract.json"
CALCULATOR = REVIEW / "scripts" / "calculate_score.py"
CHAT = REVIEW / "references" / "chat-summary.md"


def assessment(*, c4="pass", unknown=(), not_applicable=(), score=5):
    rows = []
    for number in range(1, 10):
        cid = f"C{number}"
        if cid in unknown:
            rows.append({"id": cid, "applicability": "unknown", "evidence": "Source unavailable"})
        elif cid in not_applicable:
            rows.append({"id": cid, "applicability": "not_applicable", "evidence": "Agreed scope excludes it"})
        elif cid == "C4":
            rows.append({"id": cid, "applicability": "applicable", "status": c4, "evidence": "report.md#c4"})
        else:
            rows.append({"id": cid, "applicability": "applicable", "score": score, "evidence": f"report.md#{cid.lower()}"})
    return {"criteria": rows}


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_one_contract_holds_the_scale_and_each_criterion_once(self):
        scale = self.contract["scale"]
        self.assertEqual((scale["minimum"], scale["maximum"], scale["step"]), (0, 5, 0.5))
        self.assertEqual(set(scale["anchors"]), {str(i) for i in range(6)})
        ids = [row["id"] for row in self.contract["criteria"]]
        self.assertEqual(ids, [f"C{i}" for i in range(1, 10)])
        self.assertEqual(len(ids), len(set(ids)))

    def test_c4_is_a_merge_gate_and_the_other_weights_sum_to_100(self):
        rows = {row["id"]: row for row in self.contract["criteria"]}
        self.assertEqual(rows["C4"], {"id": "C4", "merge_gate": True})
        self.assertEqual(rows["C3"]["weight"], 20)
        self.assertEqual(rows["C5"]["weight"], 18)
        self.assertEqual(sum(row.get("weight", 0) for row in rows.values()), 100)


class CalculatorTests(unittest.TestCase):
    def run_calculator(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assessment.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            run = subprocess.run(
                ["python3", str(CALCULATOR), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
        return run, json.loads(run.stdout) if run.stdout else None

    def test_a_complete_top_score_is_clear_and_fully_assessable(self):
        run, result = self.run_calculator(assessment())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["score"], 10.0)
        self.assertEqual(result["assessability_percent"], 100)
        self.assertEqual(result["merge_status"], "clear")

    def test_c4_failure_blocks_merge_without_changing_the_numeric_score(self):
        run, result = self.run_calculator(assessment(c4="fail"))
        self.assertEqual(run.returncode, 1)
        self.assertEqual(result["score"], 10.0)
        self.assertEqual(result["merge_status"], "blocked")

    def test_the_calculator_uses_the_criterion_weights(self):
        payload = assessment(score=0)
        next(row for row in payload["criteria"] if row["id"] == "C3")["score"] = 5
        run, result = self.run_calculator(payload)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["score"], 2.0)

    def test_unknown_lowers_assessability_and_not_applicable_reweights(self):
        run, result = self.run_calculator(assessment(unknown={"C9"}, not_applicable={"C8"}, score=4))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(result["score"], 8.0)
        self.assertEqual(result["assessability_percent"], 89)
        self.assertEqual(result["applicable_weight"], 86)

    def test_off_step_scores_and_duplicate_criteria_are_rejected(self):
        payload = assessment()
        payload["criteria"][0]["score"] = 4.2
        run, _ = self.run_calculator(payload)
        self.assertEqual(run.returncode, 2)
        self.assertIn("0.5", run.stderr)

        payload = assessment()
        payload["criteria"][-1]["id"] = "C8"
        run, _ = self.run_calculator(payload)
        self.assertEqual(run.returncode, 2)
        self.assertIn("exactly once", run.stderr)

        payload = assessment()
        payload["criteria"][0] = "C1"
        run, _ = self.run_calculator(payload)
        self.assertEqual(run.returncode, 2)
        self.assertIn("criterion id", run.stderr)


class ChatGuidanceTests(unittest.TestCase):
    def test_the_chat_guidance_is_natural_concise_and_invites_follow_up(self):
        text = CHAT.read_text(encoding="utf-8")
        self.assertIn("one to four short lines", text)
        self.assertIn("Do not copy a fixed format", text)
        self.assertIn("assessability", text)
        self.assertIn("shall I explain them briefly", text)
        self.assertGreaterEqual(text.count("**Example"), 2)

    def test_links_are_optional_and_must_be_verified(self):
        text = CHAT.read_text(encoding="utf-8")
        self.assertIn("verified stable target", text)
        self.assertIn("omit the link", text)


if __name__ == "__main__":
    unittest.main()
