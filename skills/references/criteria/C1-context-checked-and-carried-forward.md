## C1 — Context checked and carried forward

**Requirement.** Before a solution decision is acted on, the work has checked the
relevant situation against its sources: the users and their goals, the scope and
constraints, the existing code and the surrounding systems. Material facts,
constraints and decisions that shape the work are recorded somewhere durable, with
the source or person that established them, so a later session can continue from the
same understanding. What is not known remains visible as unknown. A material open
choice about architecture, business logic or scope is handled under C2, not quietly
turned into a fact or an assumption.

**Guidance.** This matters before the first solution decision for each slice, and
again when new information changes the understanding of the work. A plausible
solution to the ticket can still be wrong when the ticket, the existing system and
the user's actual situation do not agree.

You could have the agent inspect the sources that matter for the particular change
and report what it found with [locators rather than
impressions](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/research_codebase.md#L80).
For an API change, that might mean its callers, the current handler and schema, an
earlier architecture decision and observed production behaviour. For a user-facing
change, it might also mean the current flow, user documentation, support reports and
the product decision behind it. One option for sharpening domain language and
recording consequential decisions is
[`grill-with-docs`](https://github.com/mattpocock/skills/blob/main/docs/engineering/grill-with-docs.md#what-it-does),
with other decisions kept in the ticket, criteria, plan or specification.

A useful recorded decision says what was decided, when, and which source or person
established it. “Finalised invoices remain immutable — confirmed by Maria in story
comment 12 on 12 August” carries more context than “we assume finalised invoices
cannot be edited.” A provisional statement can also be useful when it stays visibly
provisional: “Luc recalls these three columns; verify them against the meeting
transcript, and ask Luc to decide again if it differs.”

Possible evidence includes exact code, document, ticket or decision locators;
observations of current behaviour; a durable decision entry with its provenance; or
a recorded hypothesis with its verifier and consequence. A file or section existing
is not enough if its contents do not support the understanding attributed to it.
Merely repeating the ticket, scanning the top level of a repository, or relying on
an earlier summary you wrote yourself [instead of returning to the
source](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md#L10)
does not demonstrate this criterion.

**Evaluation questions.**

1. What did the work need to understand about the users, goals, scope, constraints,
   existing code and surrounding systems, and which original sources did it inspect?
2. Which material facts, constraints and decisions shaped the work, where are they
   recorded, and can another person trace them to the source or person that
   established them?
3. What remained unknown, what could that uncertainty affect, and was any missing
   knowledge treated as settled fact or as a material assumption that belongs under
   C2?
