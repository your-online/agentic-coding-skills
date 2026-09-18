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
#: The skills the developer actually starts. The first three in the order they
#: are used: advise while working, review the work, log what the developer
#: thought of it. The next three make deliveries demonstrable: build the
#: run document, collect its evidence, and falsify claims against it.
#: `next-steps` judges nothing and proves nothing — it reports the state of the
#: work that is still open, which is the question asked between the two.
#: `clickable-questions` is the odd one out: it produces no artefact and judges
#: nothing. It changes how any of the others put a question to the developer.
RUNNABLE_SKILLS = ("advise-me", "review-my-work", "log-feedback",
                   "create-verification", "collect-evidence", "falsify",
                   "next-steps", "clickable-questions")
#: Everything the installer copies, the reference first.
INSTALLED_DIRS = (REFERENCE_DIR,) + RUNNABLE_SKILLS
#: The two that judge work against the rubric. log-feedback has no use for it.
REVIEWING_SKILLS = ("advise-me", "review-my-work")
#: The ones that must never start on their own initiative: a review that fires
#: itself judges work nobody asked it to judge, and clickable-questions firing
#: itself turns every passing uncertainty into a dialog. The verification trio is the
#: opposite case — its whole point is triggering whenever a delivery needs to be
#: made demonstrable, so it is deliberately not in this set.
INVOKE_ONLY_SKILLS = ("advise-me", "review-my-work", "log-feedback",
                      "clickable-questions")
#: create-verification ships its template and its tooling. The evidence rules it
#: used to carry now sit in the shared reference directory: falsify, collect-evidence
#: and this skill all judge against them, and a copy per skill is how the same
#: paragraph starts drifting in three places.
CREATE_VERIFICATION_FILES = (
    "SKILL.md",
    "assets/VERIFICATION-template.html",
    "bin/bewijs.sh",
    "bin/injecteer.py",
    "bin/lees-oordeel.py",
)

#: falsify ships the falsifier's own instructions beside its SKILL.md. The
#: dispatcher points a freshly spawned subagent at this file by path rather than
#: having it invoke the skill: a skill that opened by working out which of two
#: roles it was in would spawn another dispatcher whenever that marker was lost.
FALSIFY_FILES = (
    "SKILL.md",
    "references/falsifier.md",
)

#: What the reference directory carries at its top level.
REFERENCE_FILES = ("rubric.md", "learning-materials.md", "evidence-rules.md")

# review-my-work has three route-specific resources. The rubric remains shared;
# these files only turn its judgement into the optional score this route adds.
REVIEW_MY_WORK_FILES = (
    "SKILL.md",
    "chat-summary.md",
    "score-contract.json",
    "calculate_score.py",
)

#: Worked examples of the artefacts a person has to read, shipped so that
#: "as short as this" is something a reader can see rather than argue about.
#: They are examples, not a house format: the intent is to have something
#: concrete to react to when the format is settled with the people who own it.
EXAMPLE_DIR = "example-formats"
EXAMPLE_FILES = (
    "criteria-example-1.md",
    "criteria-example-2.md",
    "criteria-example-3.md",
    "decisions.md",
    "open-questions.md",
    "pull-request.md",
)
EXAMPLES = SKILLS_DIR / REFERENCE_DIR / EXAMPLE_DIR

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
