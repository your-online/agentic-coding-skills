---
name: falsify
description: Try to refute a set of claims, hypotheses, or findings against their supplied evidence — a generic falsifier that ALWAYS runs in a freshly spawned subagent, never in the session that invoked it. ALWAYS use this skill when asked to falsify, attack, stress-test, or independently verify claims, conclusions, evidence, or another agent's findings ("does this evidence hold up", "check these findings", "second opinion on this conclusion", "probeer dit te weerleggen"), and when another skill (such as create-verification) dispatches a falsifier round. Not for reviewing code style or process — this is strictly about whether claims survive an attempt to disprove them.
---

# Falsify

This skill has two roles. Which one you are is decided by one marker, nothing else:

- Your brief (the prompt you were spawned with) starts with the line `ROLE: FALSIFIER` →
  you are the **falsifier**. Skip to "Part B".
- Otherwise → you are the **dispatcher**. Follow "Part A". This is the case whenever a user
  types `/falsify ...` in a session, and whenever another skill invokes this one.

Do not reason your way out of this. The session that invokes `/falsify` almost always has
produced the claims, collected the evidence, or read how that was done, and is therefore
disqualified from judging them. Even when you think you are neutral, you are not the
judge: you spawn one. Never do the falsification yourself as the dispatcher, never
"quickly check a few claims first", and never explain that you are not the right
reviewer — that is already known; the skill exists because of it. Do not commit, stash,
reset, or otherwise change the working tree in order to obtain a version identifier.

## Part A — Dispatcher

Do this in one turn, without asking the user unless step 1 fails.

1. **Assemble the four inputs** from the session and the user's arguments:
   - **Claims**: numbered, each stated as something that can be false. If the user gave a
     loose phrase ("dat het goede seedscenarios zijn"), turn it into concrete numbered
     claims yourself from what the session produced (which files, what property each
     claim asserts). Do not ask the user to reformulate.
   - **Evidence per claim**: file paths, script output, logs, a run document. Pointers,
     not summaries.
   - **Version identifier**: the HEAD commit SHA. If the tree is dirty, freeze the
     uncommitted state into a snapshot file in your scratch directory and pass its path
     next to the SHA: `git status --porcelain` followed by `git diff HEAD` and the full
     contents of every untracked file (`git ls-files --others --exclude-standard`),
     or simply an archive of the working tree (`tar czf <scratch>/tree-<timestamp>.tgz
     --exclude .git .`). Do not use `git stash create`: it silently skips untracked
     files. Outside a git repo: the archive plus the current timestamp.
   - **What may be inspected**: repository path, machine, running system, commands the
     falsifier may rerun.
   Ask the user only when a claim cannot be stated at all or the evidence genuinely does
   not exist. Missing structure is not a reason to ask.

2. **Spawn one fresh subagent** with the `Agent` tool (subagent type `general-purpose`, or
   the strongest available model; add `model: "opus"` or better when the choice is yours).
   Run it in the foreground: the verdict is the deliverable of this turn. The prompt is
   exactly:

   ```
   ROLE: FALSIFIER
   Invoke the skill `falsify` and follow Part B of it.

   CLAIMS
   1. ...
   2. ...

   EVIDENCE
   1. <paths / output / run document location>
   2. ...

   VERSION
   commit <sha> [snapshot <stash sha>, uncommitted: <paths>]

   MAY INSPECT
   <repo path, machine, systems, commands allowed>

   REQUIREMENT PROVENANCE (optional)
   <user decisions, stakeholder answers, why a criterion exists>

   WRITE VERDICT TO
   <run-document field | "return as numbered list">
   ```

   What must **never** go into the prompt: your reasoning, the transcript, or the chain of
   thought that produced the claims or the evidence. A falsifier that has read the maker's
   reasoning starts confirming it. Requirement provenance is allowed: it is input material,
   not the maker's reasoning.

3. **For high stakes** (access, security, money): spawn two or more falsifiers in parallel
   from different angles, or one on a different model family than whoever produced the
   claims. A single LLM verdict is manipulable and non-deterministic.

4. **Relay the verdict verbatim** to the user: the numbered VALID/REFUTED list and any
   residual-risk notes. Do not soften, reinterpret, or append your own agreement or
   defence. If the falsifier reports REFUTED, that is the result; fixing is a separate
   request. When the verdict was written into a run document, say so and where.

## Part B — Falsifier

You were spawned with fresh context for one purpose: refute the claims in your brief. Not
"are they correct?" but "show that they are not". A claim that survives a serious
refutation attempt is worth more than a claim that was merely confirmed — confirmation
looks for support and finds it; falsification looks for the hole, and not finding one
means something.

### Inputs

Your brief supplies the claims, the evidence per claim, the version identifier, and what
you may inspect. If one of these four is missing, ask the dispatcher for it before
judging; do not fill the gap with assumptions. What may also come along is the provenance
of the requirements (user decisions, stakeholder answers, why a criterion exists): that is
input material, not the maker's reasoning, and without it real gaps stay invisible — a
requirement can be met to the letter while missing the decision behind it. What must not
be in your brief is the maker's reasoning or transcript; if it is, say so and judge from
the evidence alone.

Isolation: never falsify claims you helped produce or evidence you helped collect. If
anything in your context shows you did, stop and report that instead of a verdict. Run on
the machine where the evidence was produced whenever the claims refer to local state.

### Test hard

Per claim:

- **If the claim were false, would this evidence still look exactly the same?** A green
  run without output, "tested and works" without a run, a check that cannot turn red: those
  survive a false claim and therefore prove nothing.
- **Who produced the evidence?** Text from the agent making the claim is a reference to
  evidence, never the evidence itself.
- **Does the evidence belong to exactly this version, or could it be older?** No
  fingerprint or commit/digest in the output means staleness cannot be ruled out.
- **Is there an untested path to the same result**, and are the unchecked parts named,
  rather than silence that reads as coverage?
- **Were tests changed, narrowed, or removed?** That is a finding until someone shows the
  contrary.

You may inspect the implementation and rerun checks — on the version identifier you were
given, never on a moving tree. A check that no longer applies to that version (such as a
mutation patch that misses) is a red result, not a skip. Do not be perfectionist: if you
cannot refute a claim, or barely can, it stands and you say so.

### Verdict

Per claim, binary: **VALID** or **REFUTED**, plus your reasoning in at most three
sentences, each pointing at something inspectable (a file line, a log line, an output
fragment). No scores, no hedging scale, no reward for length. Write the verdict where the
brief asks for it (for a run document: the Falsifier agent verdict field of that
criterion); otherwise return it as a numbered list matching the claims.

Beyond the verdict itself, mention — freeform, and ONLY when actually present, never as
empty boilerplate headers:

- what you could not check yourself, and why;
- what the test or evidence does not cover: the residual risk the reviewer inherits,
  whether they should check something by hand, and whether extra acceptance criteria or
  tests seem needed.

You write the verdict yourself, so write it in your own observational voice — "verified on
the server that the copy is now present", "could not repeat the run myself" — stating what
was established, objectively. Never refer to yourself in the third person ("the falsifier
found…"): that reads as someone else reporting about you.

The reader is a human reviewer deciding what still needs their own attention. Write
plainly, for a non-technical reader; technical detail only when it is essential to the
point or the criterion itself is deeply technical. In practice: no commit hashes, file
names, timestamps, or references to evidence files in the verdict text — those details
already live in the evidence field; the verdict says at a conceptual level what you
checked, what you found, and what that means for the reviewer. Do not impose structure or
fixed headings on this — one or two plain sentences inside the verdict is the norm.

Your verdict is evidence for a human decision, not the decision itself.
