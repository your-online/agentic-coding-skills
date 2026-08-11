---
name: log-feedback
description: Record something the developer says about this way of working or about these skills themselves — a gripe, a wish, a rough edge — as one dated bullet in docs/feedback.md of the repository they are working in. Use only when the developer wants their own remark written down for later — "log this", "note this as feedback", "schrijf dit op als feedback". This skill never produces feedback for the developer and never judges their work.
---

# Log feedback

Skill version 2.1.

This skill captures what the developer says **about** the process or the skills.
It never says anything about their work; nothing here reviews or advises.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from a complaint in passing that it should be logged.

## Where it goes

`docs/feedback.md`, in the repository the developer is working in. Create the
`docs/` directory and the file when they do not exist yet, with a single `#
Feedback` heading and nothing else.

Only ever append. Never rewrite, reorder, reword or remove a line that is already
there, not even one you added earlier in the same session — the log is a record of
what was said and when, and an edited record answers no question.

## The line

One bullet, in the developer's own words, shortened to a single sentence:

```
- 2026-08-11 — the falsifier round makes the review too slow for a small change
```

The date is today's, in `YYYY-MM-DD`. No heading per entry, no template, no author,
no tags, no status, no metadata block of any kind. New entries go at the end of the
file.

Only when the remark genuinely does not fit in one sentence does a second line go
underneath, indented, and that is the limit:

```
- 2026-08-11 — the review contradicted the advice from earlier in the session
  advice said to split the change, the review then criticised the extra commits
```

## Run it

1. Summarise what the developer said in one sentence, in their words. Do not
   improve their point, do not generalise it, and do not add a reason they did not
   give.
2. Show them the exact line and ask whether it says what they meant. Only after they
   confirm does anything get written.
3. Append it, and say which file you appended to.

## Maintaining this skill

Every change to this skill is a versioned change with a changelog line below. Never
edit meaning in place. The regression suite in the repository this skill was
installed from has to be green before anything is installed, and no test may be
weakened to make it pass.

## Changelog

- **2.1** — Installation is one command: `./install.sh` detects the platforms
  present and installs into each, replacing any existing version. No change to
  what this skill does.
- **2.0** — First version. Added alongside the split of `agentic-coding` into
  `advise-me` and `review-my-work`, and versioned with them so the three skills that
  ship together carry one number.
