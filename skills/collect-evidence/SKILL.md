---
name: collect-evidence
description: Fill in the evidence fields of a VERIFICATION.html run document with fresh context — execute the checks, paste literal output with an environment fingerprint, and never judge your own entries. Use when dispatched by the create-verification skill, or when asked to collect or fill in evidence for acceptance criteria ("vul het run-document in", "collect the evidence for these criteria") in a run document or verification page.
---

# Collect evidence

Fill in the evidence fields of a run document. You execute checks and record what happened;
you never judge whether it is good enough — that is the falsifier's and the human's job, and
an agent that judges its own entries confirms its own work.

Where a check is a script, the script writes its own output into the record; no agent is
involved and that is preferred. You are dispatched for the rest: checks that need driving,
files that need capturing, findings where nothing programmatic exists.

Before you start, read the evidence rules in `references/evidence-rules.md` — the
`references` directory that sits beside this skill's own directory — for the strength ladder,
the hard requirements, and the pitfalls.

## Per criterion

- Execute the check that is stated under the criterion.
- Paste the **literal** output into the field, including the command that produced it. Do not
  shorten or rewrite it — a summary is a claim, not evidence.
- Have the script print as its first lines the **environment fingerprint**: hostname, OS
  version, user, timestamp, and the unique version identifier of what is tested (commit SHA or
  image digest). The machine, the moment, and the version must be visible in the output
  itself.
- Collect on a clean, committed tree. Evidence files you generate (`evidence/<ID>.txt`) do not
  count as dirt: keep them gitignored and check cleanliness with
  `git status --porcelain -uno`, so your own collection run does not poison the version
  binding.
- If you cannot capture something yourself, leave the field empty and note that a person must
  supply that file.
- If a check fails to run, leave the field empty and note why. An empty field with an
  explanation is good; a filled-in assumption is fraud against the document.
- Evidence is a reference, not an assertion: "tested and works" is not evidence; output or a
  file is.
- One strong piece of evidence beats three weak ones.
- Never fill in an assumption, and never judge your own entries.

## Agent findings

If a criterion cannot be demonstrated programmatically, deliver findings instead. Look
objectively at code, behavior, or images and report what you do and do not find; "no evidence
found" is a valid result. Every claim points at something inspectable: a file line, a log
line, a screenshot. Afterwards the executor dispatches the `falsify` skill on your findings —
that is a separate step you are not part of, with "the claims are correct" as its hypothesis.
