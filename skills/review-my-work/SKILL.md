---
name: review-my-work
description: 'Review the agentic coding work of the session that just ran against the agentic coding rubric and write one Markdown report to a path the developer picks. Use only when the developer explicitly asks for a review of what was built here — "review this session", "review my work against the rubric", "write the review to docs/reviews/x.md". Not for advice while the work is still going on and not for a verdict-free look ahead: that is what the advise-me skill is for. Produces one Markdown file and nothing else, and reviews only what the developer asked it to review.'
---

# Review my work

For the criteria, and for the rules that hold for every judgement made against them —
an isolated judge, the strongest model of the platform, the rubric read whole — use
the `/agentic-coding-rubric` skill. It is the shared source of those rules and of the
learning materials behind them, and it is a reference to consult, not a session to
run. Read it before you start.

This is the full review: the transcript and the diff, one isolated reviewer, one
falsifier round, one revision, one Markdown report.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that a review is due.

The other half of this pair is `advise-me`: short forward-looking feedback in chat
while the work is still going on, with no file and no verdict. When the developer
wants to know what to do better from here, that is the skill; this one is for a
verdict on what was built.

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
