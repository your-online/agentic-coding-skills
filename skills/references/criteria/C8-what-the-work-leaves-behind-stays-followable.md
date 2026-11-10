## C8 — What the work leaves behind stays followable

**Requirement.** The change respects the conventions and boundaries of the codebase
it lands in, and leaves behind structure that a maintainer can follow. Where it
departs from what exists, the departure is deliberate and stated. The same holds for
what the work writes for people rather than for machines — criteria, decisions, open
questions, the pull request description: each says what its reader needs in order to
check, decide or continue, outcome first, and stops there.

**Guidance.** Checking what the change does to existing boundaries and dependencies
catches more than reading the new lines alone. Codifying the house rules where the
agent always sees them — [a
CLAUDE.md](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md),
a conventions file, a linter — keeps changes inside them without repeating yourself
every session; a CLAUDE.md is read at the start of every conversation, which is also
why it only pays off while it stays short enough to be followed. A separate,
iterative sanity check on the repository structure works well here: ask the agent
whether the layout is still logical, have it propose a sorting, have it point at what
could be removed, and repeat. It returns more from the fresh context and the openly
disconfirming job C7 describes than from the agent that built the layout, which can
no longer read it as a stranger would. Do that as its own agreed change rather than as a side
effect of building a feature — a structural clean-up is by nature a broad change,
and smuggling it into a feature diff is exactly what C9 objects to.

The written artefacts have their own version of the same failure, and an agent
produces it readily: everything true, nothing left out, and nobody finishing it.
Two moves keep it in hand. Put the outcome in the first sentence of the document
and of each section — the decision, the result, the thing being
asked — so a reader who stops there still has the point. Then apply C9's deletion
test to prose: take a sentence away and ask what the reader lost. A sentence whose
removal costs no decision, fact, constraint or instruction was written for the
author. The reasoning behind a choice is worth one clause, not a paragraph;
`example-formats/` beside this file shows the length and shape that tends to work.
Reusing the shape of the last artefact of its kind is what stops the format changing
every run.

**Evaluation questions.**

1. What does this change do to the boundaries and dependencies that already existed?
2. Would a maintainer who did not write this find their way, and is anything left
   that only its author can explain?
3. Where the change departs from local convention, is the reason stated somewhere
   durable?
4. Does each written artefact open with its outcome, and which of its sentences
   would cost the reader nothing if deleted?
5. Does it restate what another artefact already carries, instead of pointing at
   it — and is it the same shape as the last artefact of its kind here?
