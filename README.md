# Agentic Coding skills

A rubric for agentic coding work, plus three skills that use it.

The rubric names what has to be demonstrably good — context, acceptance criteria,
tests, evidence, implementation — and deliberately does not prescribe how you get
there. SpecKit, Given/When/Then, a plain markdown note: any form counts as long as
it holds up under the evaluation questions.

Skill version 2.1 · rubric version 1.0.

## The three skills

Each one is started by you, explicitly. None of them triggers itself.

**`advise-me`** — while you work, including before there is any code. One isolated
subagent reads the rubric and the transcript and answers in chat: what to do
differently from here on. No file, no verdict.

```
Give me feedback on my approach so far against the agentic coding rubric.
```

**`review-my-work`** — after the work, or when you want a verdict on what was built.
Reads the session transcript and the diff, runs one isolated reviewer plus one
falsifier round, and writes a single Markdown report.

```
Review this session against the agentic coding rubric.
Write the report to docs/reviews/payment-retry.md
```

**`log-feedback`** — when you have something to say about this way of working or
about these skills. Appends one dated bullet to `docs/feedback.md` in the repository
you are working in. It records your words; it never gives you feedback.

```
Log this as feedback: the falsifier round is too heavy for a one-line change.
```

## Install

### Step 1 — get the repository

```sh
git clone <repository-url> agentic-coding-skills
cd agentic-coding-skills
```

### Step 2 — install the three skills

```sh
./install.sh
```

The script detects which platforms are on this machine and installs into each one it
finds, `~/.claude` as well as `~/.codex`. The same command installs and upgrades:
it removes an existing installation before copying, so the new version replaces the
old one instead of ending up *inside* it. It prints the path of every skill it
installed, and stops with an error if neither platform is there. All three skills go
in together, or the descriptions that point at each other point at nothing.

`evals/test_install_instructions.py` extracts this command from this README and runs
it against a throwaway home directory — fresh, over an existing installation, from
another working directory, and on a machine with only one of the two platforms — so
the instruction above is the tested one.

## Structure

```
skills/advise-me/SKILL.md             feedback on your approach, in chat
skills/review-my-work/SKILL.md        the full review, one Markdown report
skills/log-feedback/SKILL.md          your feedback about the process, one bullet
skills/*/references/                  copies of the two files below
references/rubric.md                  the criteria — the source
references/learning-materials.md      how to get better per criterion — the source
install.sh                            the installer: both platforms, all three skills
evals/                                regression suite: uvx pytest evals/
CRITERIA.md                           what these skills themselves have to satisfy
AGENTS.md                             pointer file for agents working here
```

`references/` is the source; the copies under `skills/*/references/` exist because a
skill has to be installable on its own. `evals/test_reference_sync.py` fails as soon
as a copy differs from the source by one byte.
