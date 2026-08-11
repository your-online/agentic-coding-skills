---
name: agentic-coding-rubric
description: 'The agentic coding rubric and the reading around it: the criteria themselves, what each one requires, and the questions a reviewer asks to decide it. Use only when the criteria are what is wanted — "what does the rubric ask about evidence", "which criterion covers overengineering" — or when advise-me or review-my-work sends you here for them. A reference to consult, not a session to run: it judges nothing, advises nobody and writes no file.'
---

# Agentic coding rubric

What has to be demonstrably good about a piece of agentic coding work, and how you
get better at each part of it. Everything here is material to read; nothing here
starts anything.

- [rubric.md](rubric.md) — the criteria. Each one is a requirement, guidance that
  suggests rather than demands, and the evaluation questions a reviewer asks.
- [learning-materials.md](learning-materials.md) — one to three sources per
  criterion group, with a line on why each helps. Reading for a developer who wants
  to get better at a criterion, not part of any review.

`advise-me` and `review-my-work` both read the rubric from here, so it exists once
and says the same thing to both of them.

## Judging work against it

These three hold for every judgement made against this rubric, whichever skill is
making it. They are here rather than in each skill for the same reason the rubric is:
one place, one wording.

**Never judge your own work.** The agent that did the work does not judge the session
it worked in. The judgement comes from a subagent with fresh context that receives
the raw sources and the rubric, and no expected outcome, no earlier conclusion and no
summary you wrote yourself. If an isolated subagent cannot be spawned, say so and run
nothing — a judgement an agent passed on itself supports no claim.

**Model requirement.** Every reviewing role — the reviewer, the falsifier, the
feedback subagent — runs on the strongest reasoning model the platform you are on
offers. In Claude Code that is Opus 5 (`claude-opus-5`), or Opus 4.8
(`claude-opus-4-8`) when Opus 5 is out of reach; on another platform it is that
platform's own strongest reasoning model. Where the platform does not let you choose
the model at all — a Codex fork inherits the session's model and takes no override —
the run happens on the session's model, and you say that where the answer lands, in
the report or in the chat answer, instead of claiming the requirement was met. Never
quietly fall back to a lighter or faster model — a downgraded judge produces thinner
challenges and softer findings, and nothing in the answer would say so. When the
strongest model cannot be used, because it is unavailable or usage limits block it,
say so explicitly instead of continuing in silence: tell the developer which model
the run actually used, so they can weigh what it produced, or stop and tell them it
cannot run under the current limits.

**Read the rubric whole.** Hand the subagent the complete [rubric.md](rubric.md). Do
not summarise it first; a summary of the rubric is a second rubric.
