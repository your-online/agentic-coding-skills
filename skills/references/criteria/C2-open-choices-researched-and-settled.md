## C2 — Open choices researched and settled

**Requirement.** When the task — a story, a ticket or a bare description — leaves a
material choice open about architecture, business logic or scope, that choice is
settled before anything is built on it. The agent and the person doing the work
search the sources that could answer it and settle together what their knowledge
covers. What neither can settle goes as an explicit question to someone who can
actually decide it — the ticket's author, a product owner, a team lead, a
stakeholder — with, per question, why the answer was out of reach. A material choice
never quietly becomes an assumption or the agent's own decision.

**Guidance.** This matters from the moment a ticket underdetermines the work until
each open choice is settled — usually before the slice that depends on it. Without
it the failure is quiet: the agent picks the plausible reading, builds on it, and
the person who owned the choice finds out at review, or in production, that they
never made it.

A choice is material when a wrong guess does not stay local — reversing it later
means rework, different user-visible behaviour, or a different architecture or
scope — or when someone else would have expected a say in it. A retry count is
neither. "Add an endpoint to delete a user" hides one that is both: a weak reading
drops the database row and moves on; whether deletion is soft or hard changes what
can ever be recovered, and that call belongs to someone else.

Who settles a choice follows ownership, not job titles. The person doing the work
is not necessarily the person who wrote the ticket, and writing the ticket does not
confer ownership of every choice in it: an architectural decision may belong to a
team lead the author never consulted. Asking someone something [the repo, the
backlog or an earlier decision already
answers](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md#L136)
wastes the one channel that is slow; asking nothing at all and guessing is worse.

The research half is visible when the agent [searches sources with locators per
open
point](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/create_plan.md#L50-L61)
rather than asserting that it looked. The sources in view are not automatically all
the sources — for example, a company can hold dozens of repositories the developer
never cloned, and systems the agent could reach through its connected tools but
does not open on its own. A strong transcript shows the agent naming what it could
not reach and asking whether it matters, instead of treating the visible world as
the whole one; where the reasonable boundary lies is a judgement call.

One artefact is enough to show all of this — in the story, a refinement note, the
plan, a ticket comment or an .md file: the chosen interpretation and what it rests
on, the settled choices each with who settled them, the open questions each with
who can decide them, and the small assumptions knowingly left standing, named so a
reader can see them. Anything material does not belong among those assumptions; it
appears as a settled choice or an open question. C1 covers the facts and decisions
that were checked and carried forward; the unknown that C1 says may not be dressed
up as a fact is settled here.

**Evaluation questions.**

1. For each open point, which sources could have answered it, and does the
   transcript or artefact show them searched with locators — including sources the
   agent could reach but never opened?
2. Did each question that went out go to someone who can actually decide it, and
   was the answer genuinely out of reach of the sources and the people already at
   hand?
3. Which material choices were settled, by whom, and before or after work was built
   on them — and is there one that was simply decided along the way?
