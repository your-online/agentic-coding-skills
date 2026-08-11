# AGENTS.md

Everything in this directory is the slim agentic-coding product: four skills that
install together and the rubric they share. It is self-contained: publication is a
copy of the contents of this directory into an empty repo, nothing else. Nothing
outside `slim/` belongs to this product, and no file here may reference a path
outside it.

## What is where

- `skills/agentic-coding-rubric/SKILL.md` — the reference skill. It starts nothing;
  it holds the two files below and the rules that hold for any judgement made
  against them: an isolated judge, the strongest reasoning model of the platform,
  the rubric read whole. The other skills point at it by its slash name.
- `skills/agentic-coding-rubric/rubric.md` — the criteria; each one is a
  requirement, guidance and evaluation questions.
- `skills/agentic-coding-rubric/learning-materials.md` — the sources per criterion
  group, for developers who want to get better at one.
- `skills/advise-me/SKILL.md` — feedback on the approach, in chat, while the work
  is going on. No file, no falsifier, no verdict.
- `skills/review-my-work/SKILL.md` — the full review: transcript and diff, one
  isolated reviewer, one falsifier round, one revision, one Markdown report.
- `skills/log-feedback/SKILL.md` — what the developer thinks of the process, as one
  dated bullet in `docs/feedback.md` of the repository they work in. It judges
  nothing.
- `install.sh` — the installer the README calls: it detects which platforms are
  present (`~/.claude`, `~/.codex`) and installs every skill in `skills/` into each.
  No flags, no options; it is the whole of step 2. It takes whatever `skills/` holds
  rather than a list of names, so a new skill cannot arrive here and silently stay
  home. It copies to `<target>.incoming` and moves that into place only once the copy
  succeeded, so a failed upgrade leaves the installed version standing; keep it that
  way. The detail the README no longer spells out, for whoever changes the script: it
  prints the path of every skill it installed; they all go in together, or the
  pointers between them point at nothing; and the install test covers a fresh
  machine, an upgrade over an existing installation, another working directory, a
  machine with only one of the two platforms, and a machine with neither.
- `evals/` — the regression suite. Run it from this directory: `uvx pytest evals/`.
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
2. The rubric lives once, in `skills/agentic-coding-rubric/`. So do the rules for
   judging against it. A skill that needs either points at the reference skill by its
   slash name; it never copies a paragraph across.
3. Wherever the skills are listed together, `advise-me` comes before
   `review-my-work`: that is the order in which they are used.
4. The suite is green before installation. Never weaken a test to make it pass.
5. Never install into the real `~/.claude` or `~/.codex` from a test. The install
   test runs against a throwaway home directory and must stay that way.
