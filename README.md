# Agentic Coding skills

A rubric for agentic coding work, plus three skills that judge and record against
it. The rubric is not a skill: it is a file the skills read.

The rubric names what has to be demonstrably good — context, acceptance criteria,
tests, evidence, implementation — and deliberately does not prescribe how you get
there. SpecKit, Given/When/Then, a plain markdown note: any form counts as long as
it holds up under the evaluation questions.

What changed and when is in [CHANGELOG.md](CHANGELOG.md); the skills and the rubric
ship together under one number.

## The skills

Say it in your own words and the skill triggers by itself, or type its slash command —
`/advise-me`, `/review-my-work`, `/log-feedback` — if you want to be sure it runs.
Each of the three is started by you: none of them decides on its own that feedback or
a review is due.

**`advise-me`** — while you work, including before there is any code. It reads the
transcript and whatever code exists, answers straight away from the session you are
working in, and sends an isolated judge off in the background at the same time; that
second opinion lands a little later and gets the last word. No file.

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

Beside them sits `skills/references/`, which is not a skill and has no slash command:
`rubric.md` holds the criteria and the rules for any judgement made against them, and
`learning-materials.md` the reading behind each one. The skills read those files
directly, so the rubric exists once and nothing has to be invoked to reach it. Open
them yourself to look up what a criterion asks.

## Install

### Step 1 — get the repository

```sh
git clone https://github.com/your-online/agentic-coding-skills.git agentic-coding-skills
cd agentic-coding-skills
```

### Step 2 — install the skills

```sh
./install.sh
```

The script installs into every platform it finds, `~/.claude` and `~/.codex`, and the
same command upgrades. It fails if it finds neither.

These steps are what `evals/test_install_instructions.py` runs against a throwaway
home directory, so the instruction above is the tested one.

## Structure

```
skills/references/rubric.md                      the criteria, and the rules for judging by them
skills/references/learning-materials.md          how to get better per criterion
skills/advise-me/SKILL.md                        feedback on your approach, in chat
skills/review-my-work/SKILL.md                   the full review, one Markdown report
skills/log-feedback/SKILL.md                     your feedback about the process, one bullet
install.sh                                       the installer: both platforms, everything in skills/
evals/                                           regression suite: uvx pytest evals/
CHANGELOG.md                                     what changed, per release
CRITERIA.md                                      what these skills themselves have to satisfy
AGENTS.md                                        pointer file for agents working here
```

The rubric exists once. `advise-me` and `review-my-work` used to carry a copy each,
kept identical by a test; then it became a skill of its own, which meant invoking a
skill to be told where a file was and a reference sitting in your skill list beside
three routes you can actually start. It is a plain directory now, installed with the
skills and read by path, so there is nothing to keep in sync and nothing to invoke.
