#!/usr/bin/env python3
"""Shared paths and rubric parsing, so every test agrees on what is where and on
what a criterion is."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

REFERENCES = ROOT / "references"
RUBRIC = REFERENCES / "rubric.md"
LEARNING = REFERENCES / "learning-materials.md"

SKILLS_DIR = ROOT / "skills"
#: The three skills, in the order they are used: advise while working, review the
#: work, log what the developer thought of it.
SKILL_NAMES = ("advise-me", "review-my-work", "log-feedback")
#: The two that carry the rubric. log-feedback has no use for it.
RUBRIC_SKILLS = ("advise-me", "review-my-work")

REFERENCE_FILES = ("rubric.md", "learning-materials.md")


def skill_file(name: str) -> Path:
    return SKILLS_DIR / name / "SKILL.md"


def skill_text(name: str) -> str:
    return skill_file(name).read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Line wrapping is not part of the contract; the wording is."""
    return " ".join(text.split())


def frontmatter_description(name: str) -> str:
    text = skill_text(name)
    block = text.split("---", 2)[1]
    match = re.search(r"^description:\s*(.+?)(?=^\w+:|\Z)", block, re.MULTILINE | re.DOTALL)
    assert match, f"{name} has no description in its frontmatter"
    return flat(match.group(1))


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
