#!/usr/bin/env python3
"""Shared paths and rubric parsing, so every test agrees on what is where and on
what a criterion is."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

SKILLS_DIR = ROOT / "skills"

#: The directory that is only material to read. It holds the rubric, so there is
#: one copy of it and the skills that judge against it read this file. It was a
#: skill once, with a SKILL.md whose whole job was to name a path; invoking a
#: skill to be told where a file lives is a round trip that returns nothing, and
#: it put a reference in the developer's skill list beside three routes they can
#: actually start. It installs alongside the skills and carries no SKILL.md, so
#: no platform offers it as something to run.
REFERENCE_DIR = "references"
#: The three the developer actually starts, in the order they are used: advise
#: while working, review the work, log what the developer thought of it.
RUNNABLE_SKILLS = ("advise-me", "review-my-work", "log-feedback")
#: Everything the installer copies, the reference first.
INSTALLED_DIRS = (REFERENCE_DIR,) + RUNNABLE_SKILLS
#: The two that judge work against the rubric. log-feedback has no use for it.
REVIEWING_SKILLS = ("advise-me", "review-my-work")

#: What the reference directory carries.
REFERENCE_FILES = ("rubric.md", "learning-materials.md")

RUBRIC = SKILLS_DIR / REFERENCE_DIR / "rubric.md"
LEARNING = SKILLS_DIR / REFERENCE_DIR / "learning-materials.md"


def skill_file(name: str) -> Path:
    return SKILLS_DIR / name / "SKILL.md"


def skill_text(name: str) -> str:
    return skill_file(name).read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Line wrapping is not part of the contract; the wording is."""
    return " ".join(text.split())


class FrontmatterError(ValueError):
    """The frontmatter block is not valid YAML."""


try:  # pragma: no cover - depends on the interpreter the suite runs on
    import yaml
except ImportError:  # `uvx pytest` gives an isolated env without pyyaml
    yaml = None


def frontmatter_block(text: str) -> str:
    """The text between the opening and closing `---` of a Markdown file."""
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        raise FrontmatterError("no frontmatter block delimited by ---")
    return parts[1]


def _load_without_pyyaml(block: str) -> dict:
    """A deliberately narrow stand-in for `yaml.safe_load` on flat `key: value`
    frontmatter. It exists so this check still runs where pyyaml is missing, and
    it rejects exactly what a real parser rejects here: a plain (unquoted) value
    that carries a `: ` of its own, which YAML reads as a nested mapping."""
    data = {}
    for number, line in enumerate(block.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            raise FrontmatterError(f"line {number}: unexpected indentation")
        key, separator, value = line.partition(":")
        if not separator:
            raise FrontmatterError(f"line {number}: no `key: value` pair")
        value = value.strip()
        quote = value[:1]
        if len(value) >= 2 and quote in "'\"" and value.endswith(quote):
            inner = value[1:-1]
            if quote == "'":
                if inner.replace("''", "").count("'"):
                    raise FrontmatterError(f"line {number}: unescaped ' inside a quoted value")
                value = inner.replace("''", "'")
            else:
                if inner.replace('\\"', "").count('"'):
                    raise FrontmatterError(f"line {number}: unescaped \" inside a quoted value")
                value = inner.replace('\\"', '"')
        elif ": " in value or value.endswith(":"):
            raise FrontmatterError(
                f"line {number}: mapping values are not allowed in this context; "
                "quote the value or use a block scalar"
            )
        elif quote in "[{&*!|>%@`":
            raise FrontmatterError(f"line {number}: plain value starts with the indicator {quote}")
        data[key.strip()] = value
    return data


def load_frontmatter(text: str) -> dict:
    """Parse the frontmatter of a Markdown file, or raise FrontmatterError."""
    block = frontmatter_block(text)
    if yaml is None:
        return _load_without_pyyaml(block)
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError as error:
        raise FrontmatterError(str(error)) from error
    if not isinstance(loaded, dict):
        raise FrontmatterError(f"frontmatter is {type(loaded).__name__}, not a mapping")
    return loaded


def skill_frontmatter(name: str) -> dict:
    return load_frontmatter(skill_text(name))


def frontmatter_description(name: str) -> str:
    description = skill_frontmatter(name).get("description")
    assert description, f"{name} has no description in its frontmatter"
    return flat(description)


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
