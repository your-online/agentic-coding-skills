---
name: advise-me
description: Advise a developer, in chat, on how they are working right now against the agentic coding rubric — what to do differently from here on. Use only when the developer asks about their own approach while the work is still going on, including before any code exists — "how am I doing so far", "feedback on my approach", "am I going about this the right way". Writes no file and gives no verdict on finished work; a review of what was built, with a written report, is what the review-my-work skill is for.
---

# Advise me

Skill version 2.0, using rubric version 1.0 in
[references/rubric.md](references/rubric.md).

This is the light route: forward-looking feedback in chat, no file, no falsifier,
no verdict. It works at any moment, including before there is a single line of
code.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that feedback is due.

The other half of this pair is `review-my-work`: the full review of what was built,
which reads the diff, runs a falsifier and writes one Markdown report. When the
developer wants a verdict on finished work, that is the skill; this one only looks
ahead.

## Rules

**Never judge your own work.** The main agent does not advise on the session it
worked in. The judgement comes from a subagent with fresh context that receives
the raw sources and the rubric, and no expected outcome, no earlier conclusion and
no summary you wrote yourself. If an isolated subagent cannot be spawned, say so and
run nothing — advice the main agent produced about itself supports no claim.

**Model requirement.** Every reviewing role — the reviewer, the falsifier, the
feedback subagent — runs on the strongest reasoning model the platform you are on
offers. In Claude Code that is Opus 5 (`claude-opus-5`), or Opus 4.8
(`claude-opus-4-8`) when Opus 5 is out of reach; on another platform it is that
platform's own strongest reasoning model. Never quietly fall back to a lighter or
faster model — a downgraded judge produces thinner challenges and softer findings,
and nothing in the answer would say so. When the strongest model cannot be used,
because it is unavailable or usage limits block it, say so explicitly instead of
continuing in silence: tell the developer which model the advice actually ran on, so
they can weigh it, or stop and tell them it cannot run under the current limits.

**Read the rubric whole.** Hand the subagent the complete
[references/rubric.md](references/rubric.md). Do not summarise it first; a summary
of the rubric is a second rubric.

## Sources

The whole transcript — the pattern in how this is being approached so far — plus the
diff if there is one. The diff is optional; this route is also used before any code
exists.

## Run it

Spawn one isolated subagent that reads the rubric and the sources and advises. No
falsifier, no revision round. Write no file; the answer is in chat only.

The output is forward-looking: what would you do differently or better from here on
to satisfy the rubric. Not a verdict on what has happened. Name the two or three
things that would help most, say why, and keep it short enough to read in the middle
of the work.

## Maintaining this skill

The practices this rubric measures apply to this skill too.

1. Every change to the skill or the rubric is a versioned change with a changelog
   line in the file that changed. Never edit meaning in place.
2. `references/rubric.md` and `references/learning-materials.md` are copies. The
   source lives in the repository this skill was installed from, together with the
   regression suite that keeps the copies identical and that has to be green before
   anything is installed. Never weaken a test to make it pass.

## Changelog

- **2.0** — Split off from the two-route `agentic-coding` skill: this skill is only
  the feedback round, `review-my-work` is the full review, `log-feedback` is new.
  The model requirement is now platform-agnostic instead of two named Claude models.
- **1.0** — First version, as route 2 of the `agentic-coding` skill.
