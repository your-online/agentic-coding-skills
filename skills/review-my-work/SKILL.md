---
name: review-my-work
description: Review the agentic coding work of the session that just ran against the agentic coding rubric and write one Markdown report to a path the developer picks. Use only when the developer explicitly asks for a review of what was built here — "review this session", "review my work against the rubric", "write the review to docs/reviews/x.md". Not for advice while the work is still going on and not for a verdict-free look ahead: that is what the advise-me skill is for. Produces one Markdown file and nothing else, and never triggers itself.
---

# Review my work

Skill version 2.1, using rubric version 1.0 in
[references/rubric.md](references/rubric.md).

This is the full review: the transcript and the diff, one isolated reviewer, one
falsifier round, one revision, one Markdown report.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that a review is due.

The other half of this pair is `advise-me`: short forward-looking feedback in chat
while the work is still going on, with no file and no verdict. When the developer
wants to know what to do better from here, that is the skill; this one is for a
verdict on what was built.

## Rules

**Never judge your own work.** The main agent does not review the session it
worked in. Every judgement comes from a subagent with fresh context that receives
the raw sources and the rubric, and no expected outcome, no earlier conclusion and
no summary you wrote yourself. If an isolated subagent cannot be spawned, say so and
run nothing — a review the main agent performed on itself supports no claim.

**Model requirement.** Every reviewing role — the reviewer, the falsifier, the
feedback subagent — runs on the strongest reasoning model the platform you are on
offers. In Claude Code that is Opus 5 (`claude-opus-5`), or Opus 4.8
(`claude-opus-4-8`) when Opus 5 is out of reach; on another platform it is that
platform's own strongest reasoning model. Never quietly fall back to a lighter or
faster model — a downgraded judge produces thinner challenges and softer findings,
and nothing in the report would say so. When the strongest model cannot be used,
because it is unavailable or usage limits block it, say so explicitly instead of
continuing in silence: tell the developer in chat and in the report which model the
review actually ran on, so they can weigh the findings, or stop and tell them the
review cannot run under the current limits.

**Read the rubric whole.** Hand the subagent the complete
[references/rubric.md](references/rubric.md). Do not summarise it first; a summary
of the rubric is a second rubric.

## Sources

The transcript of this session, and the newly produced output — code and text — as
a diff.

### Determine the diff basis

1. Is there uncommitted work? Then diff against `HEAD`.
2. Is everything committed? Then diff against the commit this session or task
   started from — `HEAD~n` when nothing better identifies it.

State the basis in the report, always, in the form `Diff basis: <ref> (<why>)`. The
developer is the one who knows where the task really started; naming the basis is
what lets them correct it.

## Run it

1. Spawn one reviewer subagent with fresh context. Give it the rubric, the
   transcript and the diff, and the diff basis. Give it no expected outcome.
2. Spawn one falsifier with the same raw sources and the reviewer's findings. Its
   job is to attack those findings: unsupported claims, evidence that does not carry
   the conclusion, a criterion applied where it does not fit, a weakness that was
   missed. It may return nothing. Do not reward volume.
3. Hand the critique back to the reviewer for exactly one revision. Then stop. A
   finding the reviewer cannot defend after that round comes out of the report or
   goes in as an open doubt, in words.

There is no orchestrator layer, no scorer, no validator and no snapshot ceremony.

## The report

One Markdown file. The form is free; the bar is signal. Cover what is good, what is
weak, what is missing, why each of those matters, and how to improve it. Point at
the criterion it relates to and at the concrete place in the transcript, diff or file
where you saw it. Write in ordinary language a developer can act on.

Do not attach a label to each criterion, do not produce a table because it looks
thorough, and do not put a percentage anywhere. A criterion nothing useful can be
said about is left out.

The developer chooses where it goes. When they do not,
`docs/reviews/agentic-coding-review-<yyyy-mm-dd>.md` is the default. Never overwrite
an existing report: suffix the filename until it is free.

## Maintaining this skill

The practices this rubric measures apply to this skill too.

1. Every change to the skill or the rubric is a versioned change with a changelog
   line in the file that changed. Never edit meaning in place.
2. `references/rubric.md` and `references/learning-materials.md` are copies. The
   source lives in the repository this skill was installed from, together with the
   regression suite that keeps the copies identical and that has to be green before
   anything is installed. Never weaken a test to make it pass.

## Changelog

- **2.1** — Installation is one command: `./install.sh` detects the platforms
  present and installs into each, replacing any existing version. No change to
  what this skill does.
- **2.0** — Split off from the two-route `agentic-coding` skill: this skill is only
  the full review, `advise-me` is the feedback round, `log-feedback` is new. The
  model requirement is now platform-agnostic instead of two named Claude models.
- **1.0** — First version, as route 1 of the `agentic-coding` skill.
