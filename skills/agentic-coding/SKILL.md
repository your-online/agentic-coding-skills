---
name: agentic-coding
description: Review agentic coding work against the agentic coding rubric, or get feedback on the approach you are taking right now. Use when a developer explicitly asks for a review of what was built in this session, or for advice on how their current way of working measures up. Two routes, both developer-invoked: a full review that writes one Markdown report, and a short forward-looking feedback round in chat.
---

# Agentic coding review

Skill version 1.0, using rubric version 1.0 in
[references/rubric.md](references/rubric.md).

Two routes. Both run only when the developer asks for them by name. Never start
either one on your own initiative, and never infer from the state of the work that a
review is due.

| | Route 1 — full review | Route 2 — feedback on your approach |
|---|---|---|
| When | after the work, or on a claim of done | at any moment, including before there is code |
| Sources | transcript and the diff | transcript, and the diff if there is one |
| Reviewers | one isolated reviewer, then one falsifier round | one isolated subagent |
| Result | one Markdown report file | an answer in chat, no file |

## Rules that hold for both routes

**Never judge your own work.** The main agent does not review the session it
worked in. Every judgement comes from a subagent with fresh context that receives
the raw sources and the rubric, and no expected outcome, no earlier conclusion and
no summary you wrote yourself. If an isolated subagent cannot be spawned, say so and
run nothing — a review the main agent performed on itself supports no claim.

**Model requirement.** Every reviewing role — the reviewer, the falsifier, the
feedback subagent — runs on Opus 5 (`claude-opus-5`). When Opus 5 is unavailable
they run on Opus 4.8 (`claude-opus-4-8`). There is no third option. When neither is
available, or usage limits block them, fail hard: run nothing and tell the developer
in chat that the review cannot run with the available models or under the current
limits. Never quietly continue on a lighter model — a downgraded judge produces
thinner challenges and softer findings, and nothing in the report would say so.

**Read the rubric whole.** Both routes hand the subagent the complete
[references/rubric.md](references/rubric.md). Do not summarise it first; a summary
of the rubric is a second rubric.

## Route 1 — Full review

Sources: the transcript of this session, and the newly produced output — code and
text — as a diff.

### Determine the diff basis

1. Is there uncommitted work? Then diff against `HEAD`.
2. Is everything committed? Then diff against the commit this session or task
   started from — `HEAD~n` when nothing better identifies it.

State the basis in the report, always, in the form `Diff basis: <ref> (<why>)`. The
developer is the one who knows where the task really started; naming the basis is
what lets them correct it.

### Run it

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

### The report

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

## Route 2 — Feedback on your approach

Light and synchronous, in chat only. Write no file.

Sources: the whole transcript — the pattern in how this is being approached so far —
plus the diff if there is one. The diff is optional; this route is also used before
any code exists.

Spawn one isolated subagent that reads the rubric and the sources and advises. No
falsifier, no revision round.

The output is forward-looking: what would you do differently or better from here on
to satisfy the rubric. Not a verdict on what has happened. Name the two or three
things that would help most, say why, and keep it short enough to read in the middle
of the work.

## Maintaining this skill

The practices this rubric measures apply to this skill too.

1. Every change to the skill or the rubric is a versioned change with a changelog
   line in the file that changed. Never edit meaning in place.
2. Run the suite (`uvx pytest evals/`) before installing. Never install with a red
   suite, and never weaken a test to make it pass.
