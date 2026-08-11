# Agentic coding rubric — version 1.0

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

---

## C1 — Context and assumptions

**Requirement.** The work is grounded in the situation it actually lands in: the
existing code, the surrounding systems, the constraints and the users. The
assumptions it rests on are written down somewhere durable, not carried silently in
someone's head or in a chat window that scrolls away.

**Guidance.** Before building, you could have the agent read the parts of the repo
the change touches, the relevant documentation, the ticket history and earlier
decisions, and report what it found with locators rather than impressions. Recording
assumptions can be as light as a short section in the ticket or a paragraph in the
plan; the useful bit is that each assumption is phrased so it could later turn out
false. When an assumption is load-bearing and cheap to check, checking it beats
recording it. A summary you wrote yourself earlier is not a source — re-read the
original when you rely on it.

**Evaluation questions.**

1. Which parts of the existing system did the work actually inspect, and can you
   point at where that shows?
2. Are the assumptions stated somewhere a second person would find them, and is each
   one phrased sharply enough to be proven wrong?
3. Did anything get treated as settled that was never checked against a source?

---

## C2 — Own research, collaboration and open questions

**Requirement.** When the source task leaves material choices open — architecture,
business logic, scope — the agent first exhausts what it can find out by itself, and
resolves the rest together with the person picking up the work, who is not
necessarily the person who wrote the ticket. What stays materially unanswerable
after that goes as an explicit question to the author or product owner. A material
choice never quietly becomes an assumption or the agent's own decision.

**Guidance.** The form is free and one artefact is enough: the chosen
interpretation, what it rests on, the assumptions, the decisions with their
rationale, and the remaining questions with an addressee. It can live in the story,
a refinement note, the plan or a ticket comment. A transcript can demonstrate the
same thing: the agent searching sources with locators per open point, and the
back-and-forth with the person about what was left. Asking the author something the
repo, the backlog or an earlier decision already answers wastes the one channel that
is slow; asking nothing at all and guessing is worse. "The user can correct an
invoice" is the classic case — a weak reading jumps straight to editing an amount, a
strong one asks whether a finalised invoice is in scope at all.

**Evaluation questions.**

1. For each open point, is it visible that the sources were searched before anyone
   was asked?
2. Do the questions that went to the author genuinely need the author, and does each
   one have an addressee?
3. Is there any material choice about architecture, business logic or scope that was
   simply decided along the way, without anyone confirming it?

---

## C3 — Acceptance criteria that carry the intent

**Requirement.** There is a set of acceptance criteria that is concrete, observable
and testable, that covers the normal, the awkward and the failing paths, and that
traces back to confirmed intent rather than to what happened to get built. Missing
criteria are asked for, not invented.

**Guidance.** Having the agent interview you before it writes anything tends to
surface more than writing criteria yourself; so does letting it grill the criteria
afterwards for the scenario you did not name. Corrections you make mid-conversation
are criteria too — they are the ones most often lost. Writing criteria down before
implementation is what makes the difference visible between criteria that shaped the
build and criteria reverse-engineered from it afterwards. Non-goals are worth as
much as goals.

**Evaluation questions.**

1. Can each criterion be read as an observable outcome, or does it need
   interpretation before anyone can tell whether it holds?
2. Which confirmed intent and which mid-conversation corrections made it into the
   criteria, and which quietly did not?
3. Do the criteria reach beyond the happy path to the edge and failure behaviour
   that matters here?
4. Were the criteria written before the implementation, or fitted to it afterwards?

---

## C4 — The delivered behaviour meets the requirements

**Requirement.** The thing that was built actually does what the criteria describe,
on the version that is being handed over — including the awkward paths, not only the
main one.

**Guidance.** Walking each criterion against an observation of the real behaviour is
usually enough; the gaps show up as criteria you cannot point at anything for.
Judging the reached end state rather than whether the agent followed a particular
route keeps this honest. Where output is textual or user-facing, checking it against
the source rather than against how convincing it reads catches invented entities and
numbers.

**Evaluation questions.**

1. For each material criterion, what was observed that shows it holds on this
   version?
2. Which criteria are supported only by the assertion that they hold?
3. Where behaviour is user-facing or semantic, was the real result inspected rather
   than a proxy for it?

---

## C5 — Tests that cover what matters

**Requirement.** The material acceptance criteria have verification that was
actually built and actually runs, covering the scenarios that matter for each one.
Where a criterion has no automated check, that is a stated gap rather than a silence.

**Guidance.** Deciding per criterion how it will be shown to work, before building,
tends to produce a thinner and better-aimed suite than writing tests afterwards.
Coverage per criterion says more than a test count: a large generated suite can
still miss the one scenario the feature exists for. Not everything needs a unit
test — an inspection, a recorded run or a demo can be the right verification, as long
as someone other than the author can repeat it.

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

**Guidance.** Seeing a test red before the implementation makes it green is the
cheapest demonstration there is. Where that moment has passed, breaking the
behaviour on purpose and watching the check catch it does the same job; so does
mutating the implementation, or feeding the checker a known-bad input and confirming
it rejects it. The question worth asking of any test is: if this test claims to
protect X, how would I show that it does not? Repairing a test is legitimate when
equivalent coverage survives and the repaired test is demonstrably red before it is
green — weakening one to get past a failure is the thing this criterion exists to
catch.

**Evaluation questions.**

1. For the important claims, what shows that the supporting check can go red?
2. Is there a check whose logic makes failure impossible — an assertion that repeats
   the implementation, a mock of the very integration under test?
3. Was any test weakened, removed or narrowed between red and green, and did
   equivalent coverage survive?
4. Did the findings that came out of review or from a bug leave a lasting check
   behind?

---

## C7 — Evidence someone else can check

**Requirement.** Every material claim about the result rests on something inspectable
that came from outside the agent making the claim: command output, a response, a log,
a screenshot, an object in the target system, a deterministic check. The evidence is
tied to the exact version being handed over, and it would look different if the claim
were false. Prose from the agent is a pointer to evidence, never the evidence.

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

**Evaluation questions.**

1. Which system produced each piece of evidence, and is it a different one from the
   agent asserting the claim?
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
agent always sees them — a CLAUDE.md, a conventions file, a linter — keeps changes
inside them without repeating yourself every session. A separate, iterative sanity
check on the repository structure works well here: ask the agent whether the layout
is still logical, have it propose a sorting, have it point at what could be removed,
and repeat. Do that as its own agreed change rather than as a side effect of building
a feature — a structural clean-up is by nature a broad change, and smuggling it into
a feature diff is exactly what C9 objects to.

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
about two months of agent coding, put it plainly: they "really like to overcomplicate
code and APIs, they bloat abstractions, they don't clean up dead code after
themselves". He describes the same agent producing a bloated construction over a
thousand lines, being asked "couldn't you just do this instead?", and cutting it to a
hundred without protest — so asking is cheap and usually works. He notes the second
half too: agents "change/remove comments and code they don't sufficiently understand
as side effects, even if orthogonal to the task". (The widely shared CLAUDE.md that
followed his post was written by others from his observations, not by him.)

Matt Pocock offers two questions that turn this into something you can check.
The deletion test: imagine deleting the module — if complexity vanishes, it was a
pass-through; if complexity reappears across its callers, it was earning its keep.
And on seams: one adapter means a hypothetical seam, two adapters means a real one —
so do not introduce a seam unless something actually varies across it. He files
speculative generality, the middle man and shotgun surgery as smells worth naming
when you see them.

One way to get there, offered as an example and not as a step to follow: get robust
acceptance criteria and tests in place first, then minimise the lines of code
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
way back. Sandboxes and least-privilege credentials make the bound structural rather
than a matter of the agent's discipline. Stepped autonomy — read-only first, then
free within a sandbox, with an escalation when the agent wants past the edge — keeps
the review effort where the risk is. Broad production rights want a reason and a
recovery route, not just a working session.

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

## Changelog

- **1.0** — First version. Ten criteria, each a requirement, guidance and evaluation
  questions, in ordinary language. Derived from the 22-criterion review rubric that
  preceded it: the process side is compressed into C1, C2 and C10, the output side
  into C4 through C8, and C9 is new — overengineering and minimally invasive change,
  drawing on Karpathy's failure-mode observations and Pocock's deletion test.
