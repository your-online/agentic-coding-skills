# AGENTS.md

Everything in this directory is the slim agentic-coding product: three skills and
the rubric they share. It is self-contained: publication is a copy of the contents
of this directory into an empty repo, nothing else. Nothing outside `slim/` belongs
to this product, and no file here may reference a path outside it.

## What is where

- `skills/advise-me/SKILL.md` — feedback on the approach, in chat, while the work
  is going on. No file, no falsifier, no verdict.
- `skills/review-my-work/SKILL.md` — the full review: transcript and diff, one
  isolated reviewer, one falsifier round, one revision, one Markdown report.
- `skills/log-feedback/SKILL.md` — what the developer thinks of the process, as one
  dated bullet in `docs/feedback.md` of the repository they work in. It judges
  nothing.
- `skills/*/references/` — copies of the two files below. A skill is installed on
  its own, so it has to carry them.
- `references/rubric.md` — the source of the criteria; each one is a requirement,
  guidance and evaluation questions. Carries the rubric version and its changelog.
- `references/learning-materials.md` — the source of the sources per criterion
  group, for developers who want to get better at one.
- `install.sh` — the installer the README calls: it detects which platforms are
  present (`~/.claude`, `~/.codex`) and installs all three skills into each. No
  flags, no options; it is the whole of step 2.
- `evals/` — the regression suite. Run it from this directory: `uvx pytest evals/`.
  It is not installed, so no SKILL.md may tell anyone to run it.
- `CRITERIA.md` — what these skills themselves have to satisfy, with the test that
  guards each point.
- `README.md` — the public front page: the three skills, install, structure. Its
  install section is two steps and two commands; the platform detection lives in
  `install.sh`, not in the instruction.

## Rules

1. Every change to a skill or to the rubric is a versioned change with a changelog
   line in the file that changed. Never edit meaning in place. The three skills ship
   together and carry one skill version.
2. `references/` is the source. Change a reference there, then copy it over both
   skill copies; `evals/test_reference_sync.py` fails on one byte of difference.
3. Wherever the skills are listed together, `advise-me` comes before
   `review-my-work`: that is the order in which they are used.
4. The suite is green before installation. Never weaken a test to make it pass.
5. Never install into the real `~/.claude` or `~/.codex` from a test. The install
   test runs against a throwaway home directory and must stay that way.
