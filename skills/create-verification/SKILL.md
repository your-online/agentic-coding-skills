---
name: create-verification
description: Record and judge evidence per acceptance criterion in a robust VERIFICATION.html (run document). ALWAYS use this skill when acceptance criteria must be made demonstrable, when evidence needs to be captured or reviewed, when a VERIFICATION.html or run document must be created or filled in, when a rollout or delivery needs a verification page or evidence dossier, or when someone asks "how do we prove this criterion is actually met" — even when the word "evidence" is never used but green checkmarks need substantiation.
---

# Create verification

For each delivery, produce a **run document**: a fillable HTML page that records, per acceptance
criterion, (1) what evidence exists, (2) what a falsifier agent made of it, and (3) what the
human decided. The goal: someone else must later be able to trace what every green checkmark is
based on. A criterion without evidence that convinces a critical reader is not met — it is
unassessed.

The starting point is [assets/VERIFICATION-template.html](assets/VERIFICATION-template.html):
copy that file into the project (name it `VERIFICATION.html` or `VERIFICATION-<release>.html`)
and replace the example criteria with the real ones. The structure around them (metadata, three
steps per criterion, save button) is the template; the criteria are throwaway examples.

Before filling in or judging any evidence, read
[references/evidence-rules.md](references/evidence-rules.md) — the evidence-strength ladder,
the hard requirements, and the pitfalls. Filling and judging are done by two companion skills,
each run in a subagent with fresh context: `collect-evidence` (fills the evidence fields) and
`falsify` (attacks the evidence). An agent that just filled in evidence is inclined to confirm
its own work, which is why these are separate dispatches and not steps you do inline.

## The work in five steps

### 1. Test the criteria themselves first

A criterion is only sound when an agent cannot produce a "pass" without the behavior actually
existing. Rewrite vague criteria into a check with an observable outcome: what do you do, what
do you see when it is right, and — just as important — what would you see if it were wrong? A
criterion whose check cannot turn red proves nothing. For important criteria: make the check
demonstrably fail once (temporarily break the behavior, feed known-bad input) and record that
red run next to the green one. Coverage does not count as a criterion: it measures execution,
not verification.

Be pragmatic about scope. Include only the criteria genuinely needed to deliver this feature
responsibly — not every sub-aspect deserves its own criterion. Checks that measure the same
behavior belong merged into one all-in-one criterion. The number of criteria in the template is
an example, not a norm: a real run document may have more or fewer.

Give every criterion a short stable ID (A.1, M5) and carry that ID into the test names
(`test_M5_...`): evidence per criterion then becomes one filtered test run, and the binding
between check and criterion is mechanical instead of prose.

For high stakes (access, security, money): put a falsifier agent on the criteria *themselves*
before measuring anything — "could an agent get this green without the real behavior?" For
behavioral criteria, add a goal/stakeholder lens too: does this criterion measure what the
stakeholder actually needs solved, or a proxy that can be met while the real problem stays?
Criteria judged by an LLM (tone, helpfulness, classification) need the probabilistic evidence
recipe from evidence-rules.md — a golden set with hard subsets, a must-fail baseline, and an
anti-overfit stop rule.

#### Get every criterion approved before it enters the document

The criteria emerge from two sources: what the conversation established the delivery must do,
and your own analysis of what could silently be wrong. But you propose, the human decides —
a run document full of criteria the human never chose measures your idea of done, not theirs,
and the human is the one who later signs for it.

So before building the run document (step 2), present every candidate criterion through
AskUserQuestion: per criterion a plain-language explanation of what it checks and why it
matters (no test jargon — say "controleert dat een vierde sessie echt geblokkeerd wordt", not
the assertion), with options to include it or drop it. AskUserQuestion takes at most four
questions per call, so batch larger sets into rounds; multiSelect over a themed group also
works ("welke van deze vier telling-criteria neem ik op?"). Offer your recommendation per
criterion and mention gaps you deliberately did not cover — a dropped criterion belongs in the
non-goals card with the human as acceptor, so the decision stays visible instead of silently
disappearing. Only approved criteria go into the document; criteria the human adds or reshapes
in the exchange go through the same soundness test as your own (observable outcome, can turn
red).

### 2. Build the run document

- Copy the template and fill in the metadata at the top: executor, machine (hostname),
  release/version/image digest, run date, who wrote the criteria, who judges. Executor and
  judge are never the same role.
- Replace the criteria. Group by theme (`.grp`), one `<details class="row">` per criterion.
  The row anatomy is at the bottom of this file. Each criterion's `how` line states the
  concrete check plus the expected result in bold ("All three refused.").
- Set each criterion's `evhint` to the recommended evidence form — pick the strongest form that
  fits using the ladder in evidence-rules.md. Default: script output with exit code.
- Negatively phrased criteria ("X is impossible") always get a positive counter-check as its
  own criterion ("Y does work"): without it nobody can tell a refusal from a broken
  measurement.
- Do not modify the template's script and CSS; the document must keep working standalone in a
  browser, with no server or dependencies.
- Expecting more than one review round on the criteria? Write a small in-repo generator script
  that produces the run document from the template plus a criteria list, instead of editing
  the HTML by hand — regenerating after each criteria change is cheaper and prevents
  hand-edit drift.
- Add a **non-goals card** at the end ("Deliberately not covered"): a single freeform `.card`
  — not criterion rows, these are not criteria — with one bullet per gap: what was not done,
  the residual risk, whether it is mitigated, and why it is accepted and by whom. Leaving a
  risk deliberately uncovered is fine — residual risk is not failure — as long as it is
  recorded here with a named acceptor; only silent gaps are. This is where "silence that reads
  as coverage" gets its explicit place.
- After generating the run document, invoke the `html-annotator` skill (if available in your
  environment) to embed its feedback snippet and start its bridge — the reviewer can then
  comment on selections directly in the page.

#### The overview columns (Test / Falsifier / Reviewer)

The template renders each section as a table: a header row per group, and every criterion row
shows three status columns next to its title. These derive automatically — no manual upkeep:

- **Test**: from the evidence text — the *exact* strings `resultaat: PASS`/`resultaat: FAIL`
  or `exit code: 0` (with the space) mean a programmatic check; any other filled-in evidence
  (pasted output, uploads, `exitcode:` without the space) shows as **handmatig** so the reader
  can tell programmatic from human-supplied evidence at a glance. Do not hand-write these
  markers: `bin/bewijs.sh` emits them, and `bin/injecteer.py` warns before writing when a
  file would render as handmatig (this exact mismatch shipped once, on 29-08-2026).
- **Falsifier**: the bold verdict word (`VALID`/`REFUTED`) from the verdict field.
- **Reviewer**: the human judgment select (this is the row's status pill).

Per-row `data-` attributes refine this: `data-test="open"` forces the Test column to open when
the evidence field only holds an explanation rather than evidence, and
`data-test-note` / `data-fals-note` / `data-rev-note` add a short grey comment under the
status word.

**Note policy — a note earns its place only when it carries decision information the status
word alone does not:**

- what is *blocking* ("wacht op deploy token", "kan niet: geen toegang tot X");
- *timing* the reader would otherwise misread ("eerste nightly draait vanavond");
- a *caveat* on an otherwise green word ("oordeel gold de eerdere rode stand");
- something the reviewer and executor *agreed on that has since been processed*.

Never use notes for process history or technical detail the evidence already carries (commit
hashes, install dates, tool names). No note is the default; most rows should have none.

### 3. Fill in the evidence

Where the check is a script, **the script itself** writes its output into the record — evidence
created at the moment of the check beats anything assembled afterwards. Have every check script
print an environment fingerprint as its first lines: hostname, OS version, user, timestamp, and
the unique version identifier of what is being tested (commit SHA or image digest). That makes
it provable afterwards where and when the run happened and which version the evidence belongs
to.

Run every scripted check through the bundled runner instead of hand-rolling the output format:

```bash
<skill-dir>/bin/bewijs.sh A.1 -- pytest tests/ -k T1 -v            # groene run
<skill-dir>/bin/bewijs.sh A.1 --append --verwacht-rood -- pytest tests/ -k T1 -v  # mutatierun
```

It writes `evidence/<ID>.txt` with the fingerprint, the literal command, the literal output,
`exit code: N` and `resultaat: PASS/FAIL` — the exact contract the overview's Test column
parses. With `--verwacht-rood` a failing exit is the PASS (for mutation/counter-proof runs), so
red runs land in the same file without hand-edited verdict lines. Then place the files into the
document with the bundled injector:

```bash
<skill-dir>/bin/injecteer.py VERIFICATION.html              # droogloop: toont per ID of de
                                                            # Test-kolom het herkent
<skill-dir>/bin/injecteer.py VERIFICATION.html --toepassen  # schrijft echt
```

The injector touches only the evidence field of each matching row — falsifier verdicts, human
judgments and any annotator snippet survive re-injection — and its dry run flags every file
that would render as "handmatig", so a format mistake is caught before it reaches the
document. Keep the generated `evidence/` directory out of version control, and out of the
clean-tree check below.

Only for evidence that cannot come from a script do you dispatch a subagent with fresh
context, instructed to invoke the **`collect-evidence`** skill and given the path to the run
document, the criteria to fill, and the version identifier. Core rules, for yourself too:

- Paste literal output, including the command that produced it. Never shorten, rewrite, or
  summarize — a summary is a claim, not evidence.
- Evidence is a reference, not an assertion. "Tested and works" is not evidence; output, a
  file, or a log line is.
- If you cannot capture something yourself: leave the field empty and note what a human must
  supply. If a check fails to run: leave the field empty and note why. An empty field with an
  explanation is good; a filled-in assumption is fraud against your own document.
- One strong piece of evidence beats three weak ones. Evidence collection can itself become
  theater.
- Whoever filled in the evidence does not judge it. If the agent loop also builds the project:
  keep the verification script outside the building agent's write permissions, and treat any
  change to tests or baselines in the same change as a finding until the contrary is shown.

### 4. Have a falsifier attack the evidence

Dispatch a subagent with fresh context, instructed to invoke the **`falsify`** skill — the
generic falsifier. Pass it exactly four things: the claims (each criterion plus its expected
result, stated as something that can be false), the evidence per claim (or the path to the run
document), the version identifier, and what it may inspect. Never pass the reasoning or
transcript that produced the evidence — a falsifier that has read the maker's reasoning starts
confirming it. It writes VALID or REFUTED plus at most three sentences into each Falsifier
agent verdict field. Default is one falsifier round; for high stakes, multiple falsifiers from
different angles, or one on a different model family than whoever collected the evidence.

### 5. Human judgment and archiving

A human sets the final status (met / needs work / not met) and carries the residual risk; that
is about responsibility, not capability, so it keeps holding no matter how good models get.
Then click **Save as file**: CI systems purge artifacts after 30–90 days, so the run document
archives its own evidence, standalone, alongside the delivery.

One run document = one run, on one machine, by one executor. Rolling out to multiple machines
or environments: one run document per machine/environment, and the fingerprints in the output
then show different hostnames. The strongest close: have a fresh agent reproduce the run from a
clean checkout of the commit SHA.

## Row anatomy of the template

One criterion is one `<details class="row">` inside a `<div class="sep">` with a
`<div class="grp">` heading. Copy an existing row and adapt it:

```html
<details class="row"><summary><span class="chev">&#9654;</span><span class="ref">A.1</span>
<b>Title of the criterion</b><span class="pill open">Open</span></summary><div class="rb">
<p class="how">The concrete check. <b>The expected result.</b></p>
<div class="step"> ... stepnum 1: Evidence (evhint = recommended form, evtext + dropzone) ... </div>
<div class="step"> ... stepnum 2: Falsifier agent verdict ... </div>
<div class="step"> ... stepnum 3: Human judgment (select + jdnote) ... </div>
</div></details>
```

Keep the three steps intact in every row; adapt only `ref`, title, `how`, and the `evhint`. An
optional `<p class="ctx">Context ...</p>` after the how line explains why a criterion exists
(such as for a positive counter-check).

## Relation to other skills

- If the project runs **spec-driven-dev**: the RED→GREEN spec runs are exactly the "script
  output with exit code" this document wants as its strongest evidence. Reference the spec per
  criterion and paste the literal run output; do not write parallel checks.
- **review-my-work** reviews the *process* afterwards against the agentic-coding rubric. This
  document proves the *product* per criterion. The falsifier's test questions deliberately
  share the same source (rubric criteria C6 and C7).
