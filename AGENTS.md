# AGENTS.md

Everything in this directory is the slim agentic-coding product: three skills that
install together and the reference material they share. It is self-contained: publication is a
copy of the contents of this directory into the root of the public repository,
nothing else. Nothing outside `slim/` belongs to this product, and no file here may
reference a path outside it.

The public repository is **https://github.com/your-online/agentic-coding-skills**,
default branch `main`. The repository around this directory has no remote and is
never pushed: what goes out is this directory's contents, copied to the root of that
public repo — so `slim/skills/` lands there as `skills/`, and the clone URL in the
README is that same repository. It carries a `.gitignore` that does not exist here;
leave it in place when copying. Publishing is the one moment the two can drift, so
when a fix is made on either side, carry it to the other in the same sitting.

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
5. The suite is green before installation. Never weaken a test to make it pass.
6. Never install into the real `~/.claude` or `~/.codex` from a test. The install
   test runs against a throwaway home directory and must stay that way.
