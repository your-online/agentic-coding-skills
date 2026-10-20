---
name: repo-hygiene
description: Try to refute the claim that a push contains no files that do not belong in the repository — build output, caches, local databases and logs, eval runs, analyses, plans, mockups, screenshots, temp and backup files — with a freshly spawned falsifier, never in the session that made the changes. Use it on every git push as part of a push gate, next to the sensitive-data check, and whenever asked about clutter in a push or a repository ("check de netheid", "staat er rommel in deze push", "is this push clean"). Exceptions come only from the AGENTS.md files on the path. It never pushes and never approves a push.
---

# Repo hygiene

Shared and production codebases fill up with files that helped someone once: a run log, an
analysis, a mockup, a screenshot. This skill tries to refute one claim before a push — **"this
push contains no files that do not belong in this repository"** — so that clutter is caught
while it is one commit old.

You are the dispatcher. You collect the list of files and hand it to a freshly spawned
falsifier; you never judge whether a file belongs. The session that pushes is the session
that made the changes, and it is disqualified for the same reason `falsify` exists: it knows
why every file seemed fine. Do not pre-filter the list, do not "quickly check the obvious
ones", and do not read the rules file meant for the falsifier.

This check runs **beside** the sensitive-data check of a push gate, not instead of it. It
never runs `git push`, and it never approves one: whether the push goes ahead stays with the
developer and the gate.

## 1. Determine the scope

Take the remote and the ref being pushed from the push command (default: the upstream of the
current branch). Run `git fetch <remote>` first, so the remote-tracking refs are current.

- **Normal push** — the remote already has refs (`git ls-remote <remote>` returns any). The
  scope is every file added, modified, renamed or copied by the commits not yet on that
  remote, including files a later commit in the same push deletes again — they still travel
  in the history:
  `git log --format= --name-only --diff-filter=AMRC <ref> --not --remotes=<remote> | sort -u`
- **First push to a new remote** — `git ls-remote <remote>` returns nothing. The scope is the
  whole tree (`git ls-tree -r --name-only <ref>`) **and** every path that ever existed in
  the history but is gone from the tree:
  `git log --format= --name-only --no-renames --diff-filter=A <ref> | sort -u`, minus the tree
  list (`--no-renames` makes a renamed or copied path count as added, so it is not missed).
  Keep the two lists apart; history-only files need a different remedy.

Write each list to a file in your scratch directory. An empty scope means there is nothing to
check: say so and stop.

## 2. Spawn one fresh falsifier

Group the scope into claims, one per top-level folder (files at the root together as one),
and on a first push one more claim for the history-only list. Each claim reads: "every file
in `<folder>/` in this push belongs in the repository". Use the `Agent` tool with the
strongest model available; it may run in the background, but the push waits for its verdict.

Resolve the three paths to absolute ones first. `<skills directory>` is the directory that
holds this skill's base directory; the falsifier's own instructions are the ones the `falsify`
skill ships.

```
Read <skills directory>/falsify/references/falsifier.md and follow it. You are the falsifier.
Evidence rules: <skills directory>/references/evidence-rules.md
What "belongs" means: <skill base directory>/references/rules.md

CLAIMS
1. Every file in <folder>/ in this push belongs in the repository.
2. ...
[n. No file that exists only in the history of <ref> is clutter.]

EVIDENCE
The file lists: <scratch path(s)>. The files themselves, and every AGENTS.md on the path from
each file's folder to the root, at the commit below.

VERSION
commit <sha of the ref being pushed>

MAY INSPECT
<repository path>, read-only: git show, git log, git ls-tree, reading files, searching the
code for what refers to a file. No commits, no checkouts, no changes.

WRITE VERDICT TO
return as numbered list, every offending path listed under a REFUTED claim
```

Never put in the brief why a file was added, what it was for, or anything else from this
session: that is the maker's reasoning, and a falsifier that reads it starts agreeing.

## 3. After the verdict, in this session

Relay the verdict as written. If every claim SURVIVED, say so in one line and leave the push
to the gate. For each path under a REFUTED claim, ask the developer **keep or remove**, one
path or folder per question, as a choice rather than a paragraph. Then:

- **Keep** — the file belongs after all, so the reason has to be written down. Propose one
  line under `## Hoort in de repo` in the `AGENTS.md` of that file's folder (create the
  heading, or the file, if it is not there), in the form `pad-of-map/ : reden`, and ask:
  "Zal ik dat erin zetten?" Write it only after a yes. The exception goes in `AGENTS.md`
  because every agent and every developer reads that file; never in `CLAUDE.md`.
- **Remove** — `git rm --cached <path>` (`-r` for a folder), which keeps the local file and
  takes it out of the repository, and propose the matching `.gitignore` line; write that
  line only after a yes.
- **Remove, first push, history-only or already in earlier commits** — removing it from the
  tree does not remove it from what the push carries. Propose rewriting the history (for
  example `git filter-repo --invert-paths --path <path>`) and explain the cost before
  asking: every commit from the first one that touched the file gets a new hash, existing
  clones and open branches no longer line up with it, and signed commits lose their
  signature. Never rewrite history without an explicit yes on exactly that.

Any of these changes means a new commit, and a new commit means the push gate starts over,
this check included. Do not carry the old verdict over to the new commit.
