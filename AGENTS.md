# AGENTS.md

This repository is the agentic-coding skill: a rubric plus the skill that reviews
work against it. It is self-contained; no file here references a path outside it.

## What is where

- `skills/agentic-coding/SKILL.md` — the workflow: the two routes, the model
  requirement, the isolation rule, the maintenance rule.
- `skills/agentic-coding/references/rubric.md` — the criteria; each one is a
  requirement, guidance and evaluation questions. Carries the rubric version and
  its changelog.
- `skills/agentic-coding/references/learning-materials.md` — sources per criterion
  group, for developers who want to get better at one.
- `evals/` — the regression suite. Run it from this directory: `uvx pytest evals/`.
- `CRITERIA.md` — what this skill itself has to satisfy, with the test that guards
  each point.
- `README.md` — the public front page: install, both routes, structure.

## Rules

1. Every change to the skill or the rubric is a versioned change with a changelog
   line in the file that changed. Never edit meaning in place.
2. The suite is green before installation. Never weaken a test to make it pass.
