# agentic-coding-skills

One number for the package: the skills and the rubric ship together, so they move
together. Before 2.4 they were counted separately — the skills 1.0 through 2.3, the
rubric 1.0 and 1.1 — and every file carried its own number and its own changelog.
Those two lines are merged here, and the files carry neither.

## 2.4

- **agentic-coding-rubric** is a new skill and the rubric's only home: `rubric.md`
  and `learning-materials.md` live there, and it starts nothing — it is a reference
  to consult, not a session to run. **advise-me** and **review-my-work** each used to
  carry their own copy of both files, kept identical by a test; they name the skill
  now, and the copies and the test that guarded them are gone.
- The rules that hold for any judgement made against the rubric — an isolated judge,
  the strongest reasoning model the platform offers, the rubric read whole — move out
  of **advise-me** and **review-my-work** into **agentic-coding-rubric**. Each of the
  two keeps only what makes it different: its sources, its falsifier, its output.
- Version lines and per-skill changelogs leave the skills and the rubric for this
  file, and the maintenance instructions leave them for `AGENTS.md`.
- **review-my-work**'s description said it "never triggers itself". It was meant as
  "does not start a review on its own", but it reads as a request never to be
  invoked; it now says it reviews only what the developer asked it to review.
- The rubric's C6 turns the burden of proof around on test repair. A changed,
  narrowed or removed test is a finding unless whoever changed it shows that the
  requirement moved or the test was wrong, that the replacement went red before it
  went green, and which coverage survived — and a repair made in the same movement as
  the fix is made visible on its own.
- The rubric's C7 describes the falsification round in its guidance: a separate agent
  in fresh context, told to disconfirm a claim rather than review it, on the evidence
  once it exists. C3 and C6 point at it with the question that fits their own object.
  The pattern was in how these skills work and nowhere in the rubric they measure by.
- The rubric's C3, C5 and C9 say what "before implementation" means: before the slice
  you are about to build, not before the whole project. Criteria that sharpen, change
  or disappear per slice are the work going well. C5 links the source for vertical
  slices on the term.
- `install.sh` installs whatever `skills/` holds instead of a list of names, so a new
  skill cannot arrive in the repository and silently stay home.
- The rubric weaves its sources into the running text as links on the terms that were
  already there, so a reader can go from a sentence to the passage behind it. No
  criterion was added, removed or reworded in substance. (This was rubric version
  1.1; it landed after skill version 2.3 and never had a release of its own.)

## 2.3

- The frontmatter of every skill is valid YAML. **review-my-work**'s description
  carried a `: ` of its own — `look ahead: that` — which YAML reads as a nested
  mapping, so GitHub showed a parse error instead of the skill. The value is quoted,
  the wording is unchanged, and a regression test parses every frontmatter block.

## 2.2

- `install.sh` copies beside the target and only moves it into place once the copy
  succeeded, so an upgrade that fails leaves the working version standing.
- **advise-me** and **review-my-work** are honest where the platform allows no model
  choice: a Codex fork inherits the session's model and takes no override, so the run
  happens on that model and says so instead of claiming the requirement was met.

## 2.1

- Installation is one command. `./install.sh` detects the platforms present,
  `~/.claude` and `~/.codex`, and installs into each, replacing any existing version.

## 2.0

- The two-route `agentic-coding` skill splits in three: **advise-me** is the feedback
  round, **review-my-work** is the full review, and **log-feedback** is new — it
  records what the developer says about the process and judges nothing. The model
  requirement becomes platform-agnostic instead of two named Claude models.

## 1.0

- First version: the `agentic-coding` skill with two routes, and the rubric that both
  of them use — ten criteria, each a requirement, guidance and evaluation questions,
  in ordinary language. Derived from the twenty-two criterion review rubric that
  preceded it: the process side compressed into C1, C2 and C10, the output side into
  C4 through C8, and C9 new — overengineering and minimally invasive change, drawing
  on Karpathy's failure-mode observations and Pocock's deletion test.
