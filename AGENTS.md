# AGENTS.md

Everything in this repository is the agentic-coding product: three skills that
install together and the reference material they share, and nothing else.

It lives in two repositories with the same contents. The source is private and is
never pushed anywhere — its history carries fixtures that may not leave, and a
pre-push hook blocks it. The published copy is
**https://github.com/your-online/agentic-coding-skills**, default branch `main`,
which is what the clone URL in the README points at. Publishing is a copy of the
source root into the published root, so the trees line up file for file, apart from
a `.gitignore` the published copy keeps as its own. That copy is also the one moment
the two can drift: make a fix on either side and carry it to the other in the same
sitting.

Every sentence here has to be true in both, which is easy to get wrong — an earlier
version of this file opened by telling the published copy that it had no remote and
was never pushed.

Publishing, in the steps that have traps in them:

1. Clone the published repository, or `git fetch && git reset --hard origin/main` in
   an existing clone, so you are copying onto its current state and not onto a stale
   one.
2. Copy the five root files, then `rsync -a --delete` `skills/` and `evals/` with
   `--exclude __pycache__ --exclude .DS_Store --exclude .pytest_cache`. Without
   `--delete` a removed file lives on in the copy; without the excludes you publish
   caches. Nothing else goes: no `.git`, and nothing this root does not carry.
3. Run `uvx pytest evals/` **in the copy**, not in the source. That is what catches a
   bad copy, and it is the step worth not skipping.
4. One commit, then push.
5. Verify by reading it back — `gh api repos/your-online/agentic-coding-skills/contents/AGENTS.md --jq '.content' | base64 -d` — rather than assuming the push carried.

## The archived heavy reviewer

This product replaced a much heavier one: a 22-criterion reviewer with an
orchestrator, a scorer, falsification transport and an Excel workbook. For a while
both sat in the same source repository, which made every question about "the rubric"
start with working out which of the two was meant.

The heavy reviewer is archived, frozen at the last state it shipped in, and is not
developed further. It has never been published here, nothing in this product depends
on it, and no file here may reference it by path. It survives on a branch of the
private source repository, with its own `ARCHIVED.md` saying so; a change to it is
made there or nowhere. A third branch there, `slim-skill`, holds an obsolete copy of
this product from before it moved to the root, and is kept only as history.

## What is where

- `skills/references/` — material to read, not a skill. It deliberately carries no
  SKILL.md: a platform lists whatever has one, so as a skill it sat in the
  developer's skill list beside three routes they can start, and reading the rubric
  meant invoking a skill to be handed a path. The skills read these files by path.
- `skills/references/rubric.md` — the criteria; each one is a requirement, guidance
  and evaluation questions. It opens with the rules that hold for any judgement made
  against them: a judgement from outside, the strongest reasoning model of the
  platform, the rubric read whole.
- `skills/references/learning-materials.md` — the sources per criterion group, for
  developers who want to get better at one.
- `skills/references/example-formats/` — short worked examples of the artefacts a
  person has to read: three shapes of a criteria file, plus decisions, open questions
  and a pull request description. C8 points here for length and shape. They are examples, not a house
  format — that is for the people who own it to settle, and these exist to give them
  something concrete to react to. Keep them short: they are the only place where
  "this short" is shown rather than argued, and an example that grows stops being
  one.
- `skills/advise-me/SKILL.md` — a read of the running session against the rubric, in
  chat, while the work is going on. It answers from the working context and spawns
  the isolated judge in the background alongside. No file.
- `skills/review-my-work/SKILL.md` — the full review: transcript and diff, one
  isolated reviewer, one falsifier round, one revision, one Markdown report.
- `skills/log-feedback/SKILL.md` — what the developer thinks of the process, as one
  dated bullet in `docs/feedback.md` of the repository they work in. It judges
  nothing.
- `install.sh` — the installer the README calls: it detects which platforms are
  present (`~/.claude`, `~/.codex`) and installs everything in `skills/` into each —
  the three skills and the reference directory beside them.
  No flags, no options; it is the whole of step 2. It takes whatever `skills/` holds
  rather than a list of names, so a new skill cannot arrive here and silently stay
  home. It copies to `<target>.incoming` and moves that into place only once the copy
  succeeded, so a failed upgrade leaves the installed version standing; keep it that
  way. It also removes what it installed here before and no longer ships, reading a
  manifest it writes per platform at `~/<platform>/.agentic-coding-skills-manifest`,
  plus a `retired` line in the script for names dropped before that manifest existed —
  never a directory it did not put there, since `references` is a name anything could
  own. When you rename or drop a skill, add its old name to `retired` in the same
  commit. The detail the README no longer spells out, for whoever changes the script:
  it prints the path of every skill it installed; they all go in together, or the
  pointers between them point at nothing; and the install test covers a fresh
  machine, an upgrade over an existing installation, another working directory, a
  machine with only one of the two platforms, and a machine with neither.
- `evals/` — the regression suite. Run it from the repository root: `uvx pytest evals/`.
  It is not installed, so no SKILL.md may tell anyone to run it.
- `CHANGELOG.md` — one changelog for the package. The skills and the rubric no
  longer carry versions of their own.
- `CRITERIA.md` — what these skills themselves have to satisfy, with the test that
  guards each point.
- `README.md` — the public front page: the skills, install, structure. Its install
  section is two steps and two commands; the platform detection lives in
  `install.sh`, not in the instruction.

## Maintaining these skills

The practices this rubric measures apply to this product too.

1. Every meaningful change is an entry in `CHANGELOG.md`, under the release it ships
   in, naming the skill it changed. Never edit meaning in place without saying so
   there. No SKILL.md and no reference file carries a version or a changelog of its
   own — that bookkeeping lived in five files once and drifted.
2. The rubric lives once, in `skills/references/rubric.md`. So do the rules for
   judging against it. A skill that needs either points at that file by path and
   never copies a paragraph across — including the model names, which is how the
   duplication came back last time.
3. A rule that binds every judgement goes in the rubric's judging section; machinery
   that exists because of one route's shape — its bias, its output medium, its
   pipeline — goes in that route's SKILL.md and nowhere else. Both skills read the
   rubric whole and every judging subagent is handed it, so the rubric is the one
   shared home that costs no extra reading. A skill never invokes another skill:
   invocation drags the other route's triggers, answer format and background spawns
   into a context they were not written for, and costs a read rather than saving one.
4. Wherever the skills are listed together, `advise-me` comes before
   `review-my-work`: that is the order in which they are used.
5. The suite is green before installation, and green before a commit that claims it
   is. Read that from pytest's own exit status, not from what scrolled past: in
   `uvx pytest evals/ -q | tail -3 && git commit …` the `&&` sees `tail`'s status,
   so a red suite commits anyway. It did once here. Run pytest bare, or put
   `set -o pipefail` in front of the pipeline. Never weaken a test to make it pass.
6. Never install into the real `~/.claude` or `~/.codex` from a test. The install
   test runs against a throwaway home directory and must stay that way.
