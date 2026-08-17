# agentic-coding-skills

One number for the package: the skills and the rubric ship together, so they move
together. Before 2.4 they were counted separately — the skills 1.0 through 2.3, the
rubric 1.0 and 1.1 — and every file carried its own number and its own changelog.
Those two lines are merged here, and the files carry neither.

## 2.15

- **references** — the rubric names Codex's model beside Claude's in the judging rules: `gpt-5.6-sol`.
  The rule was already the strength of the judge rather than a vendor, but only the
  Claude models were spelled out — so a Claude reader got two identifiers and a Codex
  reader got a general clause to derive theirs from, and the rule read as Claude's
  with an exemption for everyone else. Both installed platforms are named now, and one
  line says outright that the names are the example and the strength is the rule, so a
  platform that is not listed is not thereby excluded.

## 2.14

- **rubric** drops C10, "Autonomy within agreed bounds". Most of it was a team's
  standing configuration — sandboxes, least-privilege credentials, stepped autonomy —
  which a reviewer answers identically for every piece of work, so it carried almost
  no signal per review and belonged to governance rather than to what this rubric
  measures. It arrived as a side effect of absorbing an AI-adoption article. Nine
  criteria now, which the shape test already allowed.
- **rubric** keeps the half of C10 that is a property of the work rather than of the
  environment, under C9, where "no more than the task asked for" already lives: a
  push, a merge, a deploy or a schedule that starts running, where nobody asked for
  it, is more than the task asked for however well it was executed. C9's first
  question now follows every lasting action outside the working tree as well as every
  changed line, and its guidance offers agreeing what a run may touch beforehand. Two
  incidents in one week made the case that the concern is real: a paid pipeline
  restarted on a production host after the spend had been paused, and subagents
  moving git HEAD onto main in a live repository.
- **references** gain two more criteria examples and rename the first. The one that
  existed is `criteria-example-2.md`; `criteria-example-1.md` carries the shape used
  in practice — the criterion as the summary line of a toggle, with source, expected
  behaviour and evidence path inside it, decisions above, and a dropped criterion
  kept as a struck-through toggle so what it was stays readable. `criteria-example-3.md`
  keeps open questions in front of the decisions, and says in one line what separates
  them from a requirement: a requirement is checkable against the product, a decision
  only against the conversation. The ceiling per example moves from 35 to 55 lines,
  which a criteria file needs before it stops showing its own shape.

## 2.13

- **rubric** widens C8 from the implementation to everything the work leaves behind,
  including what it writes for people: criteria, decisions, open questions, the pull
  request description. Each says what its reader needs in order to check, decide or
  continue, outcome first, and stops there. Two questions were added — does it open
  with its outcome and which sentences would cost the reader nothing, and does it
  restate what another artefact already carries. The concern was nearly a C11; it is
  C8 because C8 already covers what a maintainer has to follow, and the ceiling of
  ten criteria exists to resist exactly the pull that a first exception starts.
- **references** ship `example-formats/`: four worked examples, one scenario across
  all of them, each under 35 lines. They are examples and say so on their first
  line, because the house format is for the people who own it to settle and these
  exist to give them something concrete to react to. A first draft restated the same
  open question in all four files, which is what the new question 5 condemns; they
  point at one another now.
- **CRITERIA.md** puts the requirement first in the two points that read as memoir,
  with the history compressed to a trailing clause. It failed the criterion this
  release adds, which was the argument for adding it.

## 2.12

- **install.sh** removes what this package installed before and no longer ships. It
  only ever replaced the directories it was about to install, so a renamed skill
  stayed on the machine for ever: everyone who installed 2.7 or earlier still has a
  dead `agentic-coding-rubric` in their skill list, offering a slash command over a
  rubric that moved in 2.8. The installer now writes a manifest per platform of what
  it put there and prunes from it on the next run, with the names retired before the
  manifest existed named in the script — that line is the only thing that can reach
  the machines this bug is already on. It never touches a directory it did not
  install: `references` is a name anything could own, and the installer deletes its
  own targets outright.
- **evals** cover the two cases that were failing and the one that must keep working:
  a stale `agentic-coding-rubric` seeded in a throwaway home is gone after an upgrade,
  a skill dropped from the source is pruned on the next run, and a directory the
  installer never placed survives two runs. The first two fail against the previous
  `install.sh`; the third passes either way and is there to stop the pruning growing
  teeth it should not have.

## 2.11

- **rubric** takes in the last two rules that were written twice. The no-labels rule
  stood in **advise-me** in one wording and in **review-my-work** in another, and the
  procedure for deciding which range to compare against stood in both; the same rule
  in two phrasings is where drift starts. Both bind every judgement, so both are
  judging rules now and the skills point at them. The rubric cannot say the word it
  bans, so the shape rule reads "no number standing in for a judgement".
- **evals** gain the half the move left out. `OneWordingTests` only ever checked that
  the skills no longer restate the two rules, which a rubric that lost both paragraphs
  would also satisfy; `SharedOutputRules` now asserts the rubric carries them.
  `ReviewMyWorkTests::test_the_diff_basis_is_derived_and_always_reported` went with the
  rule it guarded, and that assertion is what replaced it. `CriteriaGuardTests` reads
  every test name `CRITERIA.md` promises and fails on one that no longer exists — two
  had already gone stale unnoticed, one renamed with the question ceiling and one
  deleted with the diff-basis rule, and the suite stayed green through both because
  nothing read that file. Every assertion added across 2.10 and 2.11 was confirmed red
  against the previous version of the skills before being trusted: with the new skill
  files stashed, 23 fail; with them in place, none do.
- **AGENTS.md** writes down where a change goes: a rule that binds every judgement
  belongs in the rubric's judging section, machinery that exists because of one
  route's shape belongs in that route's file, and a skill never invokes another
  skill. The chain considered here — review-my-work invoking advise-me to share
  logic — was measured and rejected: it makes the review route read three files
  before the rubric instead of two, and drags advise-me's triggers, chat answer and
  automatic background judge into a run that wants none of them.

## 2.10

- **references** adds a fourth judging rule to `rubric.md`: a finding names its
  remedy. Every point a judgement raises comes with what to actually do about it —
  which mechanism, over which claim or file, which check — with the criterion's
  guidance as the first place to look and a better fit from outside it equally
  welcome as long as it is named. The rule exists because "Suggestions and
  patterns, never demands" was being read as a reason to advise abstractly: the
  mechanisms the guidance already carries — the falsifier round under C7, the ways
  under C6 to show a check can go red, the deletion test under C9 — never reached
  the developer as advice, and "your verification is weak" stopped there. The
  distinction is now written down where it was being lost: the rubric as a standard
  demands no method of anyone; advice to this developer, about this work, names one.
- **advise-me** and **review-my-work** each ask that remedy of their own output —
  advise-me of its answer in chat and of the judge it sends to the background,
  review-my-work of its report — by pointing at the new judging rule rather than
  restating it, so the wording keeps living once. The report stays free-form and
  unlabelled; no section or template was added.
- **advise-me** may close, once its own answer and the background judgement are
  both on the table, with a single-line offer of one more round: a falsifier in
  fresh context, handed the same raw sources and the advice, told to attack the
  advice itself. Nothing runs until the developer says yes — never a default, never
  a spawn on the skill's own initiative, never a question in front of the advice —
  and the automatic background judge is unchanged. This release is 2.10 rather
  than 3.0 because nothing about how the skills run moved without the developer
  asking: the same routes, the same automatic spawns, the same outputs in the same
  places — what changed is what a finding has to contain, plus one offer the
  developer can decline by saying nothing.

## 2.9

- **rubric** anchors what "simplest" is counted in, at C9: parts, layers and special
  cases a maintainer has to hold in their head, not lines. The guidance dangles
  minimising lines of code as one route, and without a unit in the requirement that
  invites reading short as simple. A second sentence forbidding shorter-by-thinner
  tests was drafted and dropped: C6 deliberately allows a test to be changed or
  removed with its three showings, so the same act would have had two criteria
  pointing different ways, and test-weakening is already C6's and C3's — the file
  says a thing once, under the criterion where it bites hardest.
- **rubric** splits C9's third evaluation question in two. Unrequested edits to
  adjacent code and pre-existing dead code removed as a side trip were asked in one
  breath, which let one answer cover two findings. The ceiling on questions moves
  from four to five to make room; it is there so a criterion cannot become a
  checklist, not to force two concerns into one question.

## 2.8

- **references** is what `agentic-coding-rubric` became. The skill existed to say
  where `rubric.md` was, so reading the rubric cost an invocation that returned a
  path, and having a SKILL.md put a reference in the developer's skill list beside
  three routes they can actually start. The directory carries no SKILL.md now,
  installs alongside the skills, and `advise-me` and `review-my-work` read
  `references/rubric.md` by path. The rules for judging — a judgement from outside,
  the strongest reasoning model, the rubric read whole — moved into the top of
  `rubric.md`, so they still live once and now sit in the file every judge is handed
  anyway.
- **advise-me** stops refusing the question it is asked. It read no diff, judged
  nothing and was required to say so, which in practice meant opening with a
  paragraph about which model it ran on and what it was not allowed to do — before
  any word about the developer's work. It now reads the transcript and the diff
  itself, says where the work meets the criteria and where it does not, spawns the
  isolated judge in the background before writing its own answer, and reports that
  judgement when it lands, disagreements included. What paid for advising in the
  working context is no longer "no verdict" but "not the verdict": the session's own
  read never stands alone or last. The route still answers in chat and writes no
  file, and `review-my-work` is unchanged.

## 2.7

- **advise-me** no longer spawns anything: it reads the rubric into the session that
  is working and advises from there. A spawned round was measured at roughly twice
  the wall-clock of advice read in context — three runs each, 66s against 27s
  average — and the wait fell exactly where the advice is meant to be usable, in the
  middle of the work; the rubric is also worth more in a context that continues than
  in one that ends with the answer. **agentic-coding-rubric** scopes the isolation
  rule accordingly: a judgement is a verdict on work that exists, forward-looking
  advice is not, and the price of advising in the working context — advice is
  softest on the choices that context already made — is paid by that route never
  returning a verdict. `review-my-work` keeps its isolated reviewer and falsifier
  unchanged. The model rule now names the adviser instead of a feedback subagent and
  covers advice running on whatever model the session runs on.

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
