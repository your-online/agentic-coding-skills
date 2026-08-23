#!/usr/bin/env python3
"""Validate one review assessment and calculate its deterministic score.

Exit 0: merge clear; 1: merge blocked; 2: invalid input; 3: outcome unknown.
The JSON result is printed for every valid assessment, including blocked ones.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CONTRACT_PATH = SKILL_DIR / "scoring" / "score-contract.json"
APPLICABILITY = {"applicable", "not_applicable", "unknown"}


class AssessmentError(ValueError):
    pass


def read_json(path: str) -> dict:
    try:
        if path == "-":
            value = json.load(sys.stdin)
        else:
            with Path(path).open(encoding="utf-8") as handle:
                value = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise AssessmentError(f"cannot read assessment JSON: {error}") from error
    if not isinstance(value, dict):
        raise AssessmentError("assessment must be a JSON object")
    return value


def load_contract() -> tuple[dict, list[dict]]:
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AssessmentError(f"cannot read score contract: {error}") from error

    scale = contract.get("scale")
    criteria = contract.get("criteria")
    if not isinstance(scale, dict) or not isinstance(criteria, list):
        raise AssessmentError("score contract needs a scale and criteria list")
    ids = [row.get("id") for row in criteria if isinstance(row, dict)]
    expected = [f"C{number}" for number in range(1, 10)]
    if ids != expected or len(ids) != len(set(ids)):
        raise AssessmentError("score contract must contain C1 through C9 exactly once and in order")
    if sum(row.get("weight", 0) for row in criteria) != 100:
        raise AssessmentError("weighted criteria in score contract must add up to 100")
    c4 = criteria[3]
    if c4 != {"id": "C4", "merge_gate": True}:
        raise AssessmentError("C4 must be the unweighted merge gate")
    return scale, criteria


def decimal_score(value: object, criterion: str, scale: dict) -> Decimal:
    if isinstance(value, bool):
        raise AssessmentError(f"{criterion} score must be numeric")
    try:
        score = Decimal(str(value))
        minimum = Decimal(str(scale["minimum"]))
        maximum = Decimal(str(scale["maximum"]))
        step = Decimal(str(scale["step"]))
    except (InvalidOperation, KeyError) as error:
        raise AssessmentError(f"{criterion} score or scale is invalid") from error
    if score < minimum or score > maximum:
        raise AssessmentError(f"{criterion} score must be between {minimum} and {maximum}")
    if (score - minimum) % step:
        raise AssessmentError(f"{criterion} score must use increments of {step}")
    return score


def calculate(payload: dict) -> dict:
    scale, contract_rows = load_contract()
    rows = payload.get("criteria")
    if not isinstance(rows, list):
        raise AssessmentError("assessment needs a criteria list")
    if any(not isinstance(row, dict) or not isinstance(row.get("id"), str) for row in rows):
        raise AssessmentError("every assessment entry needs a criterion id")

    ids = [row["id"] for row in rows]
    expected = [row["id"] for row in contract_rows]
    if len(rows) != len(expected) or sorted(ids) != sorted(expected) or len(ids) != len(set(ids)):
        raise AssessmentError("assessment must contain C1 through C9 exactly once")

    assessment = {row["id"]: row for row in rows}
    weighted_points = Decimal("0")
    applicable_weight = 0
    assessed = 0
    merge_status = "clear"

    for contract_row in contract_rows:
        cid = contract_row["id"]
        row = assessment[cid]
        applicability = row.get("applicability")
        evidence = row.get("evidence")
        if applicability not in APPLICABILITY:
            raise AssessmentError(f"{cid} applicability must be applicable, not_applicable or unknown")
        if not isinstance(evidence, str) or not evidence.strip():
            raise AssessmentError(f"{cid} needs an evidence locator or a reason for the gap")
        if applicability != "unknown":
            assessed += 1

        if cid == "C4":
            if "score" in row:
                raise AssessmentError("C4 is a merge gate and cannot have a numeric score")
            if applicability == "unknown":
                if "status" in row:
                    raise AssessmentError("unknown C4 cannot have a status")
                merge_status = "undetermined"
            elif applicability == "not_applicable":
                if "status" in row:
                    raise AssessmentError("not-applicable C4 cannot have a status")
            elif row.get("status") == "fail":
                merge_status = "blocked"
            elif row.get("status") != "pass":
                raise AssessmentError("applicable C4 status must be pass or fail")
            continue

        if "status" in row:
            raise AssessmentError(f"{cid} is weighted and cannot have a gate status")
        if applicability == "applicable":
            if "score" not in row:
                raise AssessmentError(f"{cid} needs a score when applicable")
            score = decimal_score(row["score"], cid, scale)
            weight = contract_row["weight"]
            weighted_points += score / Decimal(str(scale["maximum"])) * weight
            applicable_weight += weight
        elif "score" in row:
            raise AssessmentError(f"{cid} cannot have a score when {applicability}")

    score = None
    if applicable_weight:
        score = float((weighted_points / applicable_weight * 10).quantize(Decimal("0.1")))
    assessability = round(assessed / len(expected) * 100)
    if score is None and merge_status == "clear":
        merge_status = "undetermined"

    return {
        "score": score,
        "score_out_of": 10,
        "assessability_percent": assessability,
        "merge_status": merge_status,
        "applicable_weight": applicable_weight,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", nargs="?", default="-", help="assessment JSON file, or - for stdin")
    args = parser.parse_args()
    try:
        result = calculate(read_json(args.assessment))
    except AssessmentError as error:
        print(f"invalid assessment: {error}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    if result["merge_status"] == "blocked":
        return 1
    if result["merge_status"] == "undetermined":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
