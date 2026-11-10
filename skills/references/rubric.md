# Agentic coding rubric

This rubric says what has to be demonstrably good about a piece of agentic coding
work. It does not say how you get there. Acceptance criteria may come from SpecKit,
from Given/When/Then, from a ticket, or from three sentences in a markdown file —
what matters is whether they are precise enough to decide behaviour and to hang
tests and evidence on.

Every criterion has the same three parts:

- **Requirement** — what has to be true.
- **Guidance** — ways you could get there. Suggestions and patterns, never demands.
  Skipping all of them and doing something else entirely is fine if the requirement
  holds.
- **Evaluation questions** — what a reviewer asks to find out whether it really is
  good.

A reviewer uses the questions to form a judgement in ordinary language: what is
good, what is weak, what is missing, why it matters, how to improve it. Criteria
overlap at the edges; say a thing once, under the criterion where it bites hardest.

Several criteria ask for a second pair of eyes on something. The pattern for that —
a separate agent in fresh context, given the sources and asked to disconfirm rather
than to agree — is set out in full under C7, and the criteria that need it point
back there.

---

## Judging work against this rubric

These hold for every judgement made against this rubric, whichever skill is making
it, and they live here rather than in each skill so there is one wording of them.

**A judgement from outside is what counts.** The agent that did the work is the
softest possible judge of it, so the judgement that carries weight comes from a
subagent with fresh context that receives the raw sources and this file, and no
expected outcome, no earlier conclusion and no summary written for it. A session may
read its own work against these criteria and say what it finds — `advise-me` does
exactly that, in chat, while the work runs — but it does so alongside an isolated
judgement, never instead of one, and it never presents its own read as the verdict.
If an isolated judge cannot be spawned at all, say so where the answer lands rather
than letting a self-judgement stand as if it came from outside.

**The strongest reasoning model.** Every judging role — reviewer, falsifier, adviser
— runs on the strongest reasoning model the platform offers. In Claude Code that is
Opus 5 (`claude-opus-5`), or Opus 4.8 (`claude-opus-4-8`) when Opus 5 is out of
reach; in Codex it is the strongest model your install offers, `gpt-5.6-sol` at the
time of writing; on another platform it is that platform's own strongest reasoning
model. The names are the example, the strength is the rule — a platform that is not
named here still has a strongest model, and a name that has aged out does not excuse
running on a weaker one. Where
the platform does not let you choose — a Codex fork inherits the session's model and
takes no override — the run happens on the session's model, and that is said where
the answer lands instead of claiming the requirement was met. Never quietly fall back
to a lighter or faster model: a downgraded judge produces thinner challenges and
softer findings, and nothing in the answer would say so. When the strongest model
cannot be used at all, because it is unavailable or usage limits block it, say which
model did run, or stop and say it cannot run under the current limits.

**Read this file whole.** Hand the judging subagent the complete rubric. Do not
summarise it first; a summary of the rubric is a second rubric.

**Name the basis you compared against.** Uncommitted work is compared against `HEAD`;
where everything is committed, against the commit the session or task started from —
`HEAD~n` when nothing better identifies it. Whichever it is, say it where the answer
lands, in the form `Diff basis: <ref> (<why>)`. The developer is the one who
knows where the task really began, and naming the basis is what lets them correct it.

**Prose remains the judgement.** The reader has to be able to disagree with a
sentence about what is good, weak or missing, so a mark never replaces or compresses
the written findings. `advise-me` stays entirely score-free. Only `review-my-work`
may add a numeric score and per-criterion scoring record after the prose judgement;
its own skill owns that route-specific machinery. A criterion nothing useful can be
said about stays visibly unknown rather than receiving an invented judgement.

**A finding names its remedy.** Every point a judgement raises comes with what to
actually do about it, concretely enough to start: which mechanism, over which claim
or file, which check. The guidance under each criterion is the first place to look
for that mechanism; a better fit that is not in the guidance is equally welcome, as
long as it is named. That the guidance offers suggestions and never demands is a
rule about the standard, not about the advice: the rubric does not demand a method
of everyone, but advice to this developer, about this work, right now, is exactly
where naming a specific mechanism is the point. "Your verification is weak" is half
a finding; the whole one says which check to make able to fail, over which
behaviour, and how to show it went red.

---

## Criteria

Each criterion lives in its own file in `criteria/`, so a reviewer can load only the criteria that apply instead of the whole rubric.

- [C1 — Context checked and carried forward](criteria/C1-context-checked-and-carried-forward.md)
- [C2 — Open choices researched and settled](criteria/C2-open-choices-researched-and-settled.md)
- [C3 — Acceptance criteria that carry the intent](criteria/C3-acceptance-criteria-that-carry-the-intent.md)
- [C4 — The delivered behaviour meets the requirements](criteria/C4-the-delivered-behaviour-meets-the-requirements.md)
- [C5 — Tests that cover what matters](criteria/C5-tests-that-cover-what-matters.md)
- [C6 — Verification that can actually fail](criteria/C6-verification-that-can-actually-fail.md)
- [C7 — Evidence someone else can check](criteria/C7-evidence-someone-else-can-check.md)
- [C8 — What the work leaves behind stays followable](criteria/C8-what-the-work-leaves-behind-stays-followable.md)
- [C9 — No more than the task asked for](criteria/C9-no-more-than-the-task-asked-for.md)

---

## Adapting this rubric

Teams may reword criteria, add local examples, drop a criterion that does not apply
to their work, or add one that does. Version a meaningful change and keep criterion
identifiers stable within a version, so a later reader can tell which rubric a piece
of feedback came from.
