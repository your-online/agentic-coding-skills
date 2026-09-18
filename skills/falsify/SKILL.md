---
name: falsify
description: Try to refute a set of claims, hypotheses, or findings against their supplied evidence — a generic falsifier that ALWAYS runs in a freshly spawned subagent, never in the session that invoked it. ALWAYS use this skill when asked to falsify, attack, stress-test, or independently verify claims, conclusions, evidence, or another agent's findings ("does this evidence hold up", "check these findings", "second opinion on this conclusion", "probeer dit te weerleggen"), and when another skill (such as create-verification) dispatches a falsifier round. Not for reviewing code style or process — this is strictly about whether claims survive an attempt to disprove them.
---

# Falsify

You are the dispatcher. Your job is to assemble a brief and spawn one fresh subagent that
does the falsifying. You never judge the claims yourself.

The falsifier's own instructions live in `references/falsifier.md`, next to this file. You
do not need to read that file: it is written for the subagent, and pointing it there is
enough. Leaving it out of your context is the point — a dispatcher reasoning about how to
write a verdict is already halfway to writing one.

Do not reason your way out of this. The session that invokes `/falsify` almost always has
produced the claims, collected the evidence, or read how that was done, and is therefore
disqualified from judging them. Even when you think you are neutral, you are not the
judge: you spawn one. Never do the falsification yourself, never "quickly check a few
claims first", and never explain that you are not the right reviewer — that is already
known; the skill exists because of it. Do not commit, stash, reset, or otherwise change
the working tree in order to obtain a version identifier.

Do this in one turn, without asking the user unless step 1 fails.

## 1. Assemble the four inputs

From the session and the user's arguments:

- **Claims**: numbered, each stated as something that can be false. If the user gave a
  loose phrase ("dat het goede seedscenarios zijn"), turn it into concrete numbered claims
  yourself from what the session produced (which files, what property each claim asserts).
  Do not ask the user to reformulate.
- **Evidence per claim**: file paths, script output, logs, a run document. Pointers, not
  summaries.
- **Version identifier**: the HEAD commit SHA. If the tree is dirty, freeze the
  uncommitted state into a snapshot file in your scratch directory and pass its path next
  to the SHA: `git status --porcelain` followed by `git diff HEAD` and the full contents of
  every untracked file (`git ls-files --others --exclude-standard`), or simply an archive
  of the working tree (`tar czf <scratch>/tree-<timestamp>.tgz --exclude .git .`). Do not
  use `git stash create`: it silently skips untracked files. Outside a git repo: the
  archive plus the current timestamp.
- **What may be inspected**: repository path, machine, running system, commands the
  falsifier may rerun.

Ask the user only when a claim cannot be stated at all or the evidence genuinely does not
exist. Missing structure is not a reason to ask.

## 2. Spawn one fresh falsifier

Use the `Agent` tool (subagent type `general-purpose`, or the strongest available model;
add `model: "opus"` or better when the choice is yours). Run it in the foreground: the
verdict is the deliverable of this turn.

The first line points the subagent at its instructions. Give the absolute path, resolved
from the base directory of this skill — the subagent has no way to find the file
otherwise, and a falsifier that cannot read its own brief will improvise one.

```
Read <skill base directory>/references/falsifier.md and follow it. You are the falsifier.

CLAIMS
1. ...
2. ...

EVIDENCE
1. <paths / output / run document location>
2. ...

VERSION
commit <sha> [snapshot <path to snapshot file>, uncommitted: <paths>]

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

## 3. For high stakes

For access, security or money: spawn two or more falsifiers in parallel from different
angles, or one on a different model family than whoever produced the claims. A single LLM
verdict is manipulable and non-deterministic.

## 4. Relay the verdict verbatim

Give the user the numbered VALID/REFUTED list and any residual-risk notes as written. Do
not soften, reinterpret, or append your own agreement or defence. If the falsifier reports
REFUTED, that is the result; fixing is a separate request. When the verdict was written
into a run document, say so and where.
