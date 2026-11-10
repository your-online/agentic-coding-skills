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
