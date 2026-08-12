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

---

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

---

## C3 — Acceptance criteria that carry the intent

**Requirement.** There is a set of acceptance criteria that is concrete, observable
and testable, that covers the normal, the awkward and the failing paths, and that
traces back to confirmed intent rather than to what happened to get built. Missing
criteria are asked for, not invented.

**Guidance.** Having the agent [interview you before it writes
anything](https://code.claude.com/docs/en/best-practices#let-claude-interview-you)
tends to surface more than writing criteria yourself; so does letting it [grill the
criteria](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md#L22)
afterwards for the scenario you did not name. Corrections you make mid-conversation
are criteria too — they are the ones most often lost. Writing criteria down before
implementation is what makes the difference visible between criteria that shaped the
build and criteria reverse-engineered from it afterwards. Before implementation means
before the slice you are about to build, not before the whole project: you cannot
know everything at the start, so you settle what would finish this slice and how you
would show it, build that, and let what it teaches you sharpen, adjust or drop
criteria for the next one. Criteria that move that way are the work going well; the
ones that only appear once the code exists are what this asks about.
[Non-goals](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md#L67-L69)
are worth as much as goals. Criteria repay the attack C7 describes as much as claims
do: give them to someone who did not write them and ask what an implementation could
do that satisfies every one of them and is still the wrong thing.

**Evaluation questions.**

1. Can each criterion be read as an observable outcome, or does it need
   interpretation before anyone can tell whether it holds?
2. Which confirmed intent and which mid-conversation corrections made it into the
   criteria, and which quietly did not?
3. Do the criteria reach beyond the happy path to the edge and failure behaviour
   that matters here?
4. Were the criteria for a slice written before that slice was built, or fitted to it
   afterwards?

---

## C4 — The delivered behaviour meets the requirements

**Requirement.** The thing that was built actually does what the criteria describe,
on the version that is being handed over — including the awkward paths, not only the
main one.

**Guidance.** Walking each criterion against an observation of the real behaviour is
usually enough; the gaps show up as criteria you cannot point at anything for.
[Judging the reached end
state](https://www.anthropic.com/engineering/multi-agent-research-system#appendix)
rather than whether the agent followed a particular route keeps this honest. Where
output is textual or user-facing, [checking it against the
source](https://www.anthropic.com/engineering/multi-agent-research-system#effective-evaluation-of-agents)
rather than against how convincing it reads catches invented entities and numbers.

**Evaluation questions.**

1. For each material criterion, what was observed that shows it holds on this
   version?
2. Which criteria are supported only by [the assertion that they
   hold](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work)?
3. Where behaviour is user-facing or semantic, was the real result inspected rather
   than a proxy for it?

---

## C5 — Tests that cover what matters

**Requirement.** The material acceptance criteria have verification that was
actually built and actually runs, covering the scenarios that matter for each one.
Where a criterion has no automated check, that is a stated gap rather than a silence.

**Guidance.** Deciding per criterion how it will be shown to work, before building,
tends to produce a [thinner and better-aimed
suite](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L22)
than writing tests afterwards. That decision is taken per slice: writing all the
tests first and all the implementation after produces bulk tests of imagined
behaviour, which check the shape of things rather than what anyone does with them and
go numb to real change. Working in [vertical
slices](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L40)
instead — one criterion, the check that shows it, the code that satisfies it, then
the next — keeps each check aimed at behaviour someone asked for, and lets the slice
you just finished inform the criteria for the one after it. Coverage per criterion
says more than a test count: a
large generated suite can still miss the one scenario the feature exists for, and
[coverage and mutation figures over a generated
suite](https://arxiv.org/abs/2607.22880) stop being reliable indicators where the
code under test may itself be faulty. Which scenario a suite misses is the hardest
thing to see from inside it, so it repays the attack C7 describes: hand the criteria
and the verification to a fresh agent that built neither, and let it argue that the
one does not cover the other. Not everything needs a unit test — [an
inspection, a recorded run or a
demo](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work)
can be the right verification, as long as someone other than the author can repeat
it.

**Evaluation questions.**

1. Which criterion does each material test map to, and which criteria map to nothing?
2. Do the tests exercise the awkward inputs and the failure paths, or only the shape
   the feature was designed around?
3. Are there tests that skip themselves, run only under certain conditions, or were
   never executed on this version?

---

## C6 — Verification that can actually fail

**Requirement.** The checks that support the important claims are able to fail, and
it has been shown that they do — a check that cannot go red proves nothing. Material
findings from review or from production become a lasting check where that is
practical.

**Guidance.** [Seeing a test red before the implementation makes it
green](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L36)
is the cheapest demonstration there is. Where that moment has passed, breaking the
behaviour on purpose and watching the check catch it does the same job; so does
[mutating the
implementation](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf),
or feeding the checker a known-bad input and confirming it rejects it. The question
worth asking of any test is: if this test claims to protect X, how would I show that
it does not — a question someone other than its author answers better, which is the
move C7 describes for the claims themselves. A test that was changed, narrowed or removed is a finding until someone
shows otherwise, and the showing falls to whoever changed it: that the requirement
itself moved or the test was demonstrably wrong, that the check standing in its place
was seen red before it went green, and that the coverage which survives is equal or
better and named rather than asserted. Short of all three, what you are looking at is
a test weakened to get past a failure, which is the thing this criterion exists to
catch. A repair made in the same movement as the fix hides exactly that, so it is
made visible on its own — its own commit, its own line in the handover — where a
reader can still see which came first.

**Evaluation questions.**

1. For the important claims, what shows that the supporting check can go red?
2. Is there a check whose logic makes failure impossible — [an assertion that
   repeats the implementation](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L31),
   a mock of the very integration under test?
3. Was any test changed, narrowed or removed — and for each one, what shows that the
   requirement moved or the test was wrong, that its replacement went red first, and
   which coverage took its place?
4. Did the findings that came out of review or from a bug leave a lasting check
   behind?

---

## C7 — Evidence someone else can check

**Requirement.** Every material claim about the result rests on something inspectable
that came from outside the agent making the claim: command output, a response, a log,
a screenshot, an object in the target system, a deterministic check. The evidence is
tied to the exact version being handed over, and it would look different if the claim
were false. Prose from the agent is a pointer to evidence, [never the
evidence](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work).

**Guidance.** The discriminating question is worth applying to each piece: if this
claim were untrue, would this artefact still look like this? A green run with no
output, an HTTP 200 with no payload, "tests pass" with no run — these survive a false
claim, which is what makes them weak. Independent expected values, boundary cases, a
cross-check against a separate source, invariants and property assertions all buy
discrimination. Version binding is the other half: a commit, a build or an artefact
identity next to the evidence is what stops yesterday's proof from covering today's
code. Collecting the artefacts per criterion in one place, with exact locators, saves
the argument about whether something is "somewhere" — one useful shape is a folder
per criterion, but any arrangement someone else can navigate works.

One approach works particularly well on the claims themselves, once they exist and
before anyone else has to take them at face value. Hand the same raw sources to a
separate agent in fresh context — not the one that did the work, and not the one that
drew the conclusion — and give it a single, openly disconfirming job: try to falsify
this claim. Not "does this hold", which invites agreement, but "show me it does not"
— a claim nothing supports, evidence that does not carry the conclusion it is
attached to, a check applied where it does not fit, a gap the account reads straight
over. It gets the sources and the claim, never the reasoning that produced the claim,
so it has nothing to agree with. Several of them at once, each attacking from a
different angle, find more than one working alone, and the role deserves the
strongest reasoning model available to you: a weaker attacker returns weaker
objections and the answer looks the same either way. One round is often enough; where
a lot rests on the claim, keep going until it comes back with nothing.

What comes back is not a verdict to adopt. Check each objection yourself and answer
the ones that do not survive with counter-evidence, in words. A claim that comes out
of this held up more firmly than it went in is a normal result, not a sign the
exercise failed. What makes it worth the trouble is what an attacker finds first:
false green — evidence that looks like proof and is not. A check that never ran, a
comparison that quietly favoured one side, a suite that stays green over an
implementation with nothing in it. That is exactly the failure the person who
assembled the evidence cannot see, because from where they stand it looks like
success.

**Evaluation questions.**

1. Which system produced each piece of evidence, and is it [a different one from the
   agent asserting the
   claim](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents#the-structure-of-an-evaluation)?
2. If the claim were false, would this evidence look different — and how do you know?
3. Is the evidence bound to the exact version under review, or could it predate it?
4. Are the parts that were not checked named, rather than left as a silence that
   reads like coverage?

---

## C8 — An implementation that stays maintainable

**Requirement.** The change respects the conventions and boundaries of the codebase
it lands in, and leaves behind structure that a maintainer can follow. Where it
departs from what exists, the departure is deliberate and stated.

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

**Evaluation questions.**

1. What does this change do to the boundaries and dependencies that already existed?
2. Would a maintainer who did not write this find their way, and is anything left
   that only its author can explain?
3. Where the change departs from local convention, is the reason stated somewhere
   durable?

---

## C9 — No more than the task asked for

**Requirement.** The solution is the simplest one that satisfies the criteria, and
the change touches only what the task requires. Every changed line traces back to the
request, or to cleaning up what this change itself made redundant. No speculative
abstractions, no unrequested features, no drive-by refactors of code that was not
broken.

**Guidance.** This is the failure mode agents are worst at. Andrej Karpathy, writing
about [two months of agent
coding](https://x.com/karpathy/status/2015883857489522876), put it plainly: they
"really like to overcomplicate code and APIs, they bloat abstractions, they don't
clean up dead code after themselves". He describes the same agent producing a bloated
construction over a thousand lines, being asked "couldn't you just do this instead?",
and cutting it to a hundred without protest — so asking is cheap and usually works.
He notes the second half too: agents "change/remove comments and code they don't
sufficiently understand as side effects, even if orthogonal to the task". (The
[widely shared CLAUDE.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md)
that followed his post was written by others from his observations, not by him.)

Matt Pocock offers two questions that turn this into something you can check.
[The deletion
test](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md#L63):
imagine deleting the module — if complexity vanishes, it was a pass-through; if
complexity reappears across its callers, it was earning its keep. And on seams: [one
adapter means a hypothetical seam, two adapters means a real
one](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md#L65)
— so do not introduce a seam unless something actually varies across it. He files
[speculative generality, the middle man and shotgun
surgery](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md#L51-L55)
as smells worth naming when you see them.

One way to get there, offered as an example and not as a step to follow: get robust
acceptance criteria and tests in place for the slice you are on, then minimise the
lines of code
iteratively against the green suite — simplify or delete, re-run, and when the suite
goes red you went too far, so take a small piece back. What survives is what was
needed, with the suite as the boundary. It only works if the suite is trustworthy
first, which is C5 and C6, and it is one route among several.

**Evaluation questions.**

1. Does every changed line trace to the request or to cleaning up what this change
   itself orphaned?
2. Which abstraction, parameter or layer exists for a need the criteria do not have —
   and what happens to complexity if you delete it?
3. Was adjacent code, formatting or commentary changed without being asked, or
   pre-existing dead code removed as a side trip?
4. Could a smaller version of this solution satisfy the same criteria, and what would
   break if you tried?

---

## C10 — Autonomy within agreed bounds

**Requirement.** Where the agent acts on real sources, data or external systems, it
does so with explicit authorisation and inside limits on tools, data, permissions,
cost and recovery that fit the risk. Nothing lasting happens outside the agreed
branch, scope or environment merely because the tooling allowed it.

**Guidance.** Deciding the bounds before the run beats judging each action while it
is happening: which tools, which branch, which data, what is a dry run, what is the
way back.
[Sandboxes](https://www.anthropic.com/engineering/claude-code-sandboxing#sandboxing-a-safer-and-more-autonomous-approach)
and least-privilege credentials make the bound structural rather than a matter of the
agent's discipline. Stepped autonomy — [read-only
first](https://code.claude.com/docs/en/security#permission-based-architecture), then
free within a sandbox, with [an escalation when the agent wants past the
edge](https://www.anthropic.com/engineering/claude-code-sandboxing#sandboxed-bash-tool-safe-bash-execution-without-permission-prompts)
— keeps the review effort where the risk is. Broad production rights want a reason
and a recovery route, not just a working session.

**Evaluation questions.**

1. What could this agent reach during the run, and what was the reason for the widest
   permission it had?
2. Was there explicit authorisation for the lasting writes, and can each one be traced
   back to what was agreed?
3. If a step had gone wrong, what was the way back — and had anyone established that
   before the run?

---

## Adapting this rubric

Teams may reword criteria, add local examples, drop a criterion that does not apply
to their work, or add one that does. Version a meaningful change and keep criterion
identifiers stable within a version, so a later reader can tell which rubric a piece
of feedback came from.
