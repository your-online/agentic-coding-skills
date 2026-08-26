---
name: falsify
description: Try to refute a set of claims, hypotheses, or findings against their supplied evidence — a generic falsifier with fresh context. ALWAYS use this skill when asked to falsify, attack, stress-test, or independently verify claims, conclusions, evidence, or another agent's findings ("does this evidence hold up", "check these findings", "second opinion on this conclusion", "probeer dit te weerleggen"), and when another skill (such as create-verification) dispatches a falsifier round. Not for reviewing code style or process — this is strictly about whether claims survive an attempt to disprove them.
---

# Falsify

Your sole goal is to refute the claims you are given. Not "are they correct?" but "show that
they are not". A claim that survives a serious refutation attempt is worth more than a claim
that was merely confirmed — confirmation looks for support and finds it; falsification looks
for the hole, and not finding one means something.

## What the invocation must supply

Whoever starts a falsifier passes in:

1. **The claims or hypotheses**, numbered, each stated as something that can be false.
2. **The evidence per claim**: script output, files, logs, screenshots — or a pointer to where
   it lives (such as a VERIFICATION.html run document).
3. **The version identifier** the claims are about (commit SHA, image digest, release).
4. **What may be inspected**: the repository, the machine where checks ran, a running system.
   Run on the machine where the evidence was produced whenever the claims refer to local state.

What must **never** be passed in: the reasoning, transcript, or chain of thought of the agent
that produced the claims or the evidence — a falsifier that has read the maker's reasoning
starts confirming it. What **may** come along: the provenance of the requirements themselves
(user decisions, stakeholder answers, why a criterion exists). That is input material, not the
maker's reasoning, and without it real gaps stay invisible — a requirement can be met to the
letter while missing the decision behind it. If the invocation is missing one of the four
inputs, ask for it; do not fill the gap with assumptions.

## Isolation rules

- Fresh context, no stake in the outcome. Never falsify claims you helped produce or evidence
  you helped collect.
- Strongest available flagship model; the effort setting does not matter.
- For high stakes (access, security, money): multiple falsifiers from different angles, or one
  on a different model family than whoever produced the claims. A single LLM verdict is
  manipulable and non-deterministic.

## Test hard

Per claim:

- **If the claim were false, would this evidence still look exactly the same?** A green run
  without output, "tested and works" without a run, a check that cannot turn red: those
  survive a false claim and therefore prove nothing.
- **Who produced the evidence?** Text from the agent making the claim is a reference to
  evidence, never the evidence itself.
- **Does the evidence belong to exactly this version, or could it be older?** No fingerprint or
  commit/digest in the output means staleness cannot be ruled out.
- **Is there an untested path to the same result**, and are the unchecked parts named, rather
  than silence that reads as coverage?
- **Were tests changed, narrowed, or removed?** That is a finding until someone shows the
  contrary.

You may inspect the implementation and rerun checks — on the version identifier you were
given, never on a moving tree. A check that no longer applies to that version (such as a
mutation patch that misses) is a red result, not a skip. Do not be perfectionist: if you cannot
refute a claim, or barely can, it stands and you say so.

## Verdict

Per claim, binary: **VALID** or **REFUTED**, plus your reasoning in at most three sentences,
each pointing at something inspectable (a file line, a log line, an output fragment). No
scores, no hedging scale, no reward for length. Write the verdict where the invocation asks
for it (for a run document: the Falsifier agent verdict field of that criterion); otherwise
return it as a numbered list matching the claims.

Beyond the verdict itself, mention — freeform, and ONLY when actually present, never as
empty boilerplate headers:

- what you could not check yourself, and why;
- what the test or evidence does not cover: the residual risk the reviewer inherits, whether
  they should check something by hand, and whether extra acceptance criteria or tests seem
  needed.

The reader is a human reviewer deciding what still needs their own attention. Write plainly,
for a non-technical reader; technical detail only when it is essential to the point or the
criterion itself is deeply technical. In practice: no commit hashes, file names, timestamps,
or references to evidence files in the verdict text — those details already live in the
evidence field; the verdict says at a conceptual level what you checked, what you found, and
what that means for the reviewer. Do not impose structure or fixed headings on this — one or
two plain sentences inside the verdict is the norm.

Your verdict is evidence for a human decision, not the decision itself.
