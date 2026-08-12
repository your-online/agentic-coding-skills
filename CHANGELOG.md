# agentic-coding-skills

One number for the package: the skills and the rubric ship together, so they move
together. Before 2.4 they were counted separately — the skills 1.0 through 2.3, the
rubric 1.0 and 1.1 — and every file carried its own number and its own changelog.
Those two lines are merged here, and the files carry neither.

## 2.6

- **agentic-coding-rubric** rewrites C1 around checking the relevant reality and
  carrying that understanding into later sessions. It now names when the criterion
  matters, distinguishes unknowns from the material open choices handled by C2, and
  gives concrete examples, anti-examples and possible evidence for source-backed
  context and durable decisions.
- **agentic-coding-rubric** rewrites C2 as "Open choices researched and settled". It
  defines when a choice is material through consequence and ownership with a code
  example, replaces "exhausts" with observable research per open point, routes each
  remaining question to whoever can actually decide it rather than a fixed role,
  requires choices settled before work is built on them, separates small named
  assumptions from material ones in the artefact, and names its boundary with C1
  from both sides.

## 2.5

- **agentic-coding-rubric** points at the falsifier pattern from the places that need it, instead of
  asking for a second pair of eyes and leaving the reader to find out later how that
  is done. The introduction names C7 as the shared home of the pattern; C1 says an
  assumption is phrased sharply enough when the attack can be pointed at it; C5 says
  a suite is least able to see which scenario it misses; C8 says the same of the
  agent that built the layout. C3 and C6 already carried the reference and are
  unchanged.

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

## Before these skills

What came before was a heavier reviewer: one skill that ran an evidence-based
final review with isolated evaluators and a falsification round, and wrote its
verdict into a canonical three-sheet Excel workbook, scored by a deterministic
scorer with blocking musts and gates. These skills took its rubric and its
approach and dropped the machinery. Its two tracks — the rubric, which is the
measure, and the workflow, which is how a review is run — were versioned
separately and are listed separately here. Nothing below ships in this package;
it is kept so the line of thinking stays readable.

### Rubric

- **v0.7.0 → v0.8.0** — W4b widened from a norm for a lone agent to one that
  includes the person picking up the story: search the sources first, then work
  the rest out together, and only what nobody present can answer becomes an
  addressed question. Evidence via the transcript or via one durable artefact,
  each enough on its own.
- **v0.6.1 → v0.7.0** — new criterion W4b: exhaust the sources yourself before
  asking, and record what remains as an addressed refinement question rather
  than a chat message that evaporates next session.
- **v0.6.0 → v0.6.1** — O1a and O6 suggest an evidence folder per criterion as a
  way to order proof, explicitly not a requirement; documenting evidence neatly
  deliberately did not become a 22nd criterion.
- **v0.5.4 → v0.6.0** — `PENDING` dropped along with the checkpoint that was its
  only reason to exist; conditions resolve to true or false and nothing else.
- **v0.5.3 → v0.5.4** — the abbreviation leaves every human-facing sentence, so a
  reader who does not know the project still knows what is being measured.
- **v0.5.2 → v0.5.3** — learning sources per criterion, which had quietly fallen
  out, return as their own reference file; they are not scored.
- **v0.5.1 → v0.5.2** — the adaptability section stopped promising report shapes
  the workflow does not allow: teams restyle the canonical workbook, and that is
  the whole freedom.
- **v0.5 → v0.5.1** — every criterion gets a second anti-example with a
  materially different failure mode, and scorer jargon leaves the text that is
  copied verbatim into the workbook.
- **v0.4 → v0.5** — three questions that were tangled in one criterion come
  apart: whether acceptance criteria are good (W4), whether verification is
  agreed before building (W4a), and whether usable verification was actually
  delivered (O1a, with O6 for evidence integrity).
- **v0.3 → v0.4** — the rubric becomes machine-checkable: criticality,
  applicability conditions and gates per criterion, W11 and O7 new, and trusted
  versioned metadata behind a deterministic scorer.

### Workflow

- **v0.7.0 → v0.8.0** — evidence gets a fixed place: shared artefacts once, one
  short note per scored row, and a deterministic check that withholds the
  workbook while a scored row has none. The falsifier is asked whether the
  evidence would look different if the claim were false, and the model
  requirement fails hard instead of quietly dropping to a lighter model.
- **v0.6.2 → v0.7.0** — the mid-run checkpoint disappears. It cost as much as a
  full review while only the final one guards the handoff, and every mode-related
  failure came from having two modes.
- **v0.6.1 → v0.6.2** — the abbreviation leaves the workflow files too; technical
  identifiers and historical artifacts stay as they are.
- **v0.6.0 → v0.6.1** — the workbook is a copy of the template, filled in. The
  template itself is never written to, and no script generates it.
- **v0.5.7 → v0.6.0** — after a real run went wrong, four paths close: dispatch
  moves ahead of every other section, a final review becomes non-blocking too,
  the immutable snapshot gets a method that can actually be followed, and
  `versions.json` becomes the one place a version number lives.
- **v0.5.6 → v0.5.7** — a review runs only when the developer asks for one; the
  agent never starts one on its own, and "enough work exists to inspect" is a
  suitability condition rather than a start signal.
- **v0.5.5 → v0.5.6** — the last English column header in the developer-facing
  workbook is translated.
- **v0.5.4 → v0.5.5** — the internal scorer percentages leave the workbook and
  the notification: both mix verdict severity with assessability and measure
  neither cleanly. The evidence column says what was inspected.
- **v0.5.3 → v0.5.4** — exactly three tabs in a fixed order, technical and
  version data only on `Metadata`, verdicts shown in plain language, and status
  colour only inside verdict cells.
- **v0.5.2 → v0.5.3** — the explanatory block above the table is removed; the
  header starts on its own row.
- **v0.5.1 → v0.5.2** — each row carries the criterion's canonical standard
  paragraph verbatim; evaluator-written summaries are forbidden.
- **v0.5 → v0.5.1** — one category per criterion kind, process or delivered
  result; the third category that measured evidence strength is dropped, since
  verdicts and assessability already say that.
- **v0.4.1 → v0.5** — the Excel workbook becomes the only durable report and
  generated HTML and Markdown go; `confidence` is replaced by a statement of what
  could and could not be assessed; delivery is one short notification with one
  action.
- **v0.4 → v0.4.1** — a checkpoint dispatches exactly one fresh-context
  background orchestrator instead of running evaluation, falsification and
  scoring in front of the developer, which had made it too disruptive to use
  mid-implementation.
