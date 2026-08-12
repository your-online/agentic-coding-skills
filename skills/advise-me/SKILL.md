---
name: advise-me
description: Advise a developer, in chat, on how they are working right now against the agentic coding rubric — what to do differently from here on. Use only when the developer asks about their own approach while the work is still going on, including before any code exists — "how am I doing so far", "feedback on my approach", "am I going about this the right way". Writes no file and gives no verdict on finished work; a review of what was built, with a written report, is what the review-my-work skill is for.
---

# Advise me

For the criteria, and for the rules that hold for every judgement made against them —
an isolated judge, the strongest model of the platform, the rubric read whole — use
the `/agentic-coding-rubric` skill. It is the shared source of those rules and of the
learning materials behind them, and it is a reference to consult, not a session to
run. Read it before you start.

This is the light route: forward-looking feedback in chat, no file, no falsifier,
no verdict. It works at any moment, including before there is a single line of
code.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that feedback is due.

The other half of this pair is `review-my-work`: the full review of what was built,
which reads the diff, runs a falsifier and writes one Markdown report. When the
developer wants a verdict on finished work, that is the skill; this one only looks
ahead.

## Sources

The whole transcript — the pattern in how this is being approached so far — plus the
diff if there is one. The diff is optional; this route is also used before any code
exists.

## Run it

Load the complete rubric into this session and advise from here, in the main context.
Spawn nothing: an extra hop roughly doubles the wait for advice that is meant to be
read in the middle of the work, and the rubric is more use in the context that keeps
going than in one that ends with the answer. No falsifier, no revision round. Write
no file; the answer is in chat only.

The price of that is real and it fixes the boundary of this route. Advising in the
context that did the work means advising on your own choices, and the agent that
picked an approach is the last one to name it as the thing to drop. So this route
looks ahead only: it never doubles as a verdict on what has been built, however the
question is phrased. Say plainly which model this session is on when it is not the
platform's strongest, and when what the developer actually wants is a judgement of
finished work, that is `review-my-work` with its isolated reviewer.

The output is forward-looking: what would you do differently or better from here on
to satisfy the rubric. Not a verdict on what has happened. Name the two or three
things that would help most, say why, and keep it short enough to read in the middle
of the work.
