# Agentic Coding skills

Skills that help you do agentic coding well, and show that you did. They judge your
work against one shared rubric, make a delivery checkable per acceptance criterion,
and keep your repository clean.

The rubric says *what* has to be good (context, acceptance criteria, tests, evidence,
implementation), never *how* you get there. Any method counts if it holds up.

What changed: [CHANGELOG.md](CHANGELOG.md). Full details per skill, for agents and the
curious: [AGENTS.md](AGENTS.md).

## The skills

Say what you want in your own words, or type the slash command to be sure.

**Feedback on how you work**

- `advise-me` — feedback on your approach while you work. *"Give me feedback on my approach so far."*
- `review-my-work` — a full review with a score when you're done. *"Review this session against the rubric."*
- `log-feedback` — write down your feedback on this way of working, one line.

**Proof that the product works**

- `create-verification` — sets up a page that shows what each green check is based on.
- `collect-evidence` — runs the checks and records the literal output.
- `falsify` — tries to refute each claim; returns SURVIVED or REFUTED.

**Day to day**

- `next-steps` — where the open work stands, as one numbered list.
- `clickable-questions` — questions to you as a choice, not a paragraph.
- `repo-hygiene` — checks a push for files that don't belong in the repo.

The rubric itself is not a skill: it lives in `skills/references/rubric.md`, with one
file per criterion in `skills/references/criteria/`.

## Install

### Step 1 — get the repository

```sh
git clone https://github.com/your-online/agentic-coding-skills.git agentic-coding-skills
cd agentic-coding-skills
```

### Step 2 — install the skills

```sh
./install.sh
```

The script installs into every platform it finds, `~/.claude` and `~/.codex`, and the
same command upgrades. It fails if it finds neither.

## Structure

```
skills/references/rubric.md                      the criteria, and the rules for judging by them
skills/references/learning-materials.md          how to get better per criterion
skills/advise-me/SKILL.md                        feedback on your approach, in chat
skills/review-my-work/SKILL.md                   the full review, report and concise score
skills/review-my-work/scoring/score-contract.json one scale, weights and the C4 merge block
skills/review-my-work/scripts/calculate_score.py deterministic score calculation
skills/log-feedback/SKILL.md                     your feedback about the process, one bullet
skills/next-steps/SKILL.md                       where the open work stands, one numbered list
skills/clickable-questions/SKILL.md              questions as a choice, not a paragraph
skills/repo-hygiene/SKILL.md                     clutter check on a push, judged by a falsifier
skills/repo-hygiene/references/rules.md          what belongs in a repository, and the exceptions
install.sh                                       the installer: both platforms, everything in skills/
evals/                                           regression suite: uvx pytest evals/
CHANGELOG.md                                     what changed, per release
CRITERIA.md                                      what these skills themselves have to satisfy
AGENTS.md                                        pointer file for agents working here
```
