#!/usr/bin/env python3
"""Shared parsing of the rubric, so the shape tests and the language test agree
on what a criterion is."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agentic-coding"
SKILL = SKILL_DIR / "SKILL.md"
RUBRIC = SKILL_DIR / "references" / "rubric.md"
LEARNING = SKILL_DIR / "references" / "learning-materials.md"
README = ROOT / "README.md"

CRITERION_HEADING = re.compile(r"^## (C\d+) — (.+)$", re.MULTILINE)

PARTS = ("**Requirement.**", "**Guidance.**", "**Evaluation questions.**")


def rubric_text() -> str:
    return RUBRIC.read_text(encoding="utf-8")


def criteria() -> "list[tuple[str, str, str]]":
    """Return (id, title, body) for every criterion section, in file order."""
    text = rubric_text()
    matches = list(CRITERION_HEADING.finditer(text))
    out = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((match.group(1), match.group(2), text[match.end():end]))
    return out


def evaluation_questions(body: str) -> "list[str]":
    block = body.split(PARTS[2], 1)[1]
    return re.findall(r"^\d+\. ", block, re.MULTILINE)
