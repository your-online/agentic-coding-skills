---
name: review-my-work
description: 'Review the agentic coding work of the session that just ran against the agentic coding rubric, write one Markdown report to a path the developer picks, and return a concise weighted score beside it. Use only when the developer explicitly asks for a review of what was built here — "review this session", "review my work against the rubric", "write the review to docs/reviews/x.md". Not for advice while the work is still going on and not for a verdict-free look ahead: that is what the advise-me skill is for. Reviews only what the developer asked it to review.'
---

# Review my work

The criteria, and the rules that hold for every judgement made against them — an
isolated judge, the strongest model of the platform, the rubric read whole — live in
`references/rubric.md`, the `references` directory beside this skill's own directory
in the same skills directory. It is material to read, not a skill: there is nothing
to invoke. Read it before you start, and hand it to the reviewer whole. Beside it
sits `learning-materials.md`, wider reading per criterion for the developer, not
input to the review.

This is the full review: the transcript and the diff, one isolated reviewer, one
falsifier round, one revision, one Markdown report, and one concise chat summary.
Only this route adds a score. The prose judgement remains primary; the score makes
its overall strength easier to scan and compare, not easier to skip.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that a review is due.

The other half of this pair is `advise-me`: a short read against the same rubric in
chat while the work is still going on, answered in the working context with an
isolated second opinion following in the background, and no file. When the developer
wants to know what to do better from here, that is the skill; this one is for a
written verdict on what was built.

## Sources

The transcript of this session, and the newly produced output — code and text — as
a diff, on the basis the rubric's judging rules derive and ask you to name.

## Run it

1. Spawn one reviewer subagent with fresh context. Give it the complete rubric, the
   transcript and the diff, the diff basis, and this skill's
   `scoring/score-contract.json`. Give it no expected outcome. Alongside its prose
   findings it returns exactly one assessment entry for C1–C9, each with an evidence
   locator or a reason the evidence is unavailable. Weighted criteria use 0–5 in
   0.5 steps; C4 uses only `pass` or `fail`. `not_applicable` and `unknown` are
   explicit applicability values, never disguised zeroes.
2. Have that reviewer run `scripts/calculate_score.py` over its assessment and keep
   both the assessment and calculator output with its draft. Resolve both paths
   relative to this SKILL.md. The calculator accepts a JSON file or stdin and owns
   the arithmetic, weights, reweighting, assessability and C4 merge result.
3. Spawn one falsifier with the same raw sources, the reviewer's findings, assessment
   and calculated result. Its job is to attack all four: unsupported claims,
   evidence that does not carry the conclusion, an inflated or deflated criterion
   score, a criterion applied where it does not fit, a weakness that was missed. It
   may return nothing. Do not reward volume.
4. Hand the critique back to the reviewer for exactly one revision. The reviewer
   explicitly checks whether the calculated result represents the evidence. Where
   it does not, it may correct a criterion score with one short reason, then run the
   calculator again. Never edit the final score or a weight directly. Then stop. A
   finding the reviewer cannot defend after that round comes out of the report or
   goes in as an open doubt, in words.

There is still no orchestrator layer, validator or snapshot ceremony: the only new
machinery is one JSON contract and one deterministic calculator.

## The score

The contract deliberately lives in one file. It gives C3 and C5 the most weight,
because useful acceptance criteria and verification that actually exercises them
carry the rest of the review. C4 has no weight: if requested behaviour was not
delivered, and no scope correction was demonstrably agreed while the work was in
progress, the result is merge-blocking rather than something a high average can
compensate for.

`not_applicable` is removed from the weighted denominator. `unknown` is also left
out of the numeric result, but lowers the separately displayed assessability, so a
high score cannot hide thin evidence. The calculator rejects missing or duplicate
criteria, scores off the half-point scale, unweighted C4 scores and unsupported
applicability values. Its non-zero exit for a blocked or undetermined merge is part
of the result; read its JSON output even when the command exits non-zero.

## The report

One Markdown file. The form is free; the bar is signal. Cover what is good, what is
weak, what is missing, why each of those matters, and how to improve it. Point at
the criterion it relates to and at the concrete place in the transcript, diff or file
where you saw it. Write in ordinary language a developer can act on. Each point
carries its remedy, the way the rubric's judging rules ask — concrete enough to
start on.

End the report with a compact scoring basis: the final score, assessability, merge
status, and one short line per criterion containing its score or applicability,
reason and evidence locator. This record is what lets another reviewer rerun or
disagree with the calculation; it never replaces the ordinary-language findings.

The developer chooses where it goes. When they do not,
`docs/reviews/agentic-coding-review-<yyyy-mm-dd>.md` is the default. Never overwrite
an existing report: suffix the filename until it is free.

After the file is written, read `references/chat-summary.md` in this skill directory
and return the concise chat summary it describes. Keep it natural rather than
forcing a template. Links to a rubric criterion or evaluation question are useful
only when their target was verified; omit an uncertain link.
