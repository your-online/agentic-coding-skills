# Agentic Coding skill

A rubric for agentic coding work, plus a skill that reviews your work against it.

The rubric names what has to be demonstrably good — context, acceptance criteria,
tests, evidence, implementation — and deliberately does not prescribe how you get
there. SpecKit, Given/When/Then, a plain markdown note: any form counts as long as
it holds up under the evaluation questions.

Skill version 1.0 · rubric version 1.0.

## Install

Claude Code:

```sh
cp -R skills/agentic-coding ~/.claude/skills/agentic-coding
```

Codex:

```sh
cp -R skills/agentic-coding ~/.codex/skills/agentic-coding
```

## The two routes

Both routes are started by you, explicitly. The skill never triggers itself.

**Full review** — after the work, or when you want a verdict on what was built.
Reads the session transcript and the diff, runs one isolated reviewer plus one
falsifier round, and writes a single Markdown report.

```
Review this session against the agentic coding rubric.
Write the report to docs/reviews/payment-retry.md
```

**Feedback on your approach** — while you work, including before there is any
code. One isolated subagent reads the rubric and the transcript and answers in
chat: what to do differently from here on. No file, no verdict.

```
Give me feedback on my approach so far against the agentic coding rubric.
```

## Structure

```
skills/agentic-coding/SKILL.md                     the workflow, both routes
skills/agentic-coding/references/rubric.md         the criteria
skills/agentic-coding/references/learning-materials.md   how to get better per criterion
evals/                                             regression suite: uvx pytest evals/
CRITERIA.md                                        what this skill itself has to satisfy
AGENTS.md                                          pointer file for agents working here
```
