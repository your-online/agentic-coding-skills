# What belongs in a repository

You were handed this file as the rules for one claim type: "these files belong in this
repository". Your general instructions (`falsifier.md`) and the evidence rules still hold;
this file says what "belongs" means and where the exceptions are written down.

## The rule

A file belongs in the repository only if it is needed to **build, test, run or understand**
the software. Everything else is clutter, however useful it was to whoever made it.

Belongs, as a rule:

- code, and the configuration the build or the runtime reads;
- tests, with fixtures that are synthetic (made up for the test, not copied from a real
  system);
- README, ADRs, and docs that state what the software must do or how it is verified
  (`CONTRACT`, `VERIFY` and the like);
- deploy configuration, without secrets.

Clutter by default:

- build output and caches: `node_modules/`, `dist/`, `build/`, `.next/`, `__pycache__/`,
  `.venv/`, `.pytest_cache/`, `coverage/`, `*.pyc`;
- local data: `*.db`, `*.sqlite`, log files, `*.jsonl` run output;
- experiments, and eval **runs and results** (an eval script or eval definition may stay;
  what it produced may not);
- analyses, plans, notes, and mockup or prototype HTML that the software does not serve;
- screenshots, recordings and `evidence/` folders;
- temp and backup files: `*.bak`, `*.orig`, `*.tmp`, `*.swp`, `.DS_Store`, `*~`.

The list is a default, not the test. A file not on it is clutter when it fails the rule; a
file on it belongs when the build, a test or the running software demonstrably reads it.
Judge by what the file is and what reads it, not by its name alone: open it, and search the
code for what refers to it.

## Exceptions live in AGENTS.md, nowhere else

A file that fails the rule still belongs when an `AGENTS.md` says so. Read **every**
`AGENTS.md` on the way from the file's own folder up to the repository root, in the version
you were given (`git show <sha>:<folder>/AGENTS.md`), not in the working tree. The format:

```
## Hoort in de repo

experiments/ : vergelijking van drie promptvarianten, input voor ADR-0004
docs/mockups/checkout.html : referentie voor de UI-review
```

One line per entry: a path, ` : `, and the reason. The path is relative to the folder that
holds that `AGENTS.md`. A path ending in `/` covers everything below it. No globs. A file
covered by such a line is not clutter, and a clearly separated folder of experiments or
mockups is fine when it is listed this way.

Only `AGENTS.md` counts. An exception written in `CLAUDE.md`, a README, a code comment or a
commit message is not an exception: it binds one tool or nobody, and the rule must hold for
every developer and every agent that opens the repository.

An entry without a reason, or a reason that does not explain why the file is needed, is still
an entry: say so in your notes, but do not refute on it.

## The verdict, for this check

Per claim, SURVIVED or REFUTED as `falsifier.md` describes, with one deliberate exception to
its advice on file names: a REFUTED verdict lists **every offending path**, one per line,
each with a few words on why it fails the rule (for example `results/run-0412.jsonl : eval
output, not read by any code`). The developer decides per path what happens to it, so a
verdict without paths cannot be acted on. A folder that is clutter as a whole may be listed
once as the folder.

Do not refute a claim on files you were not given: the scope in your brief is the scope.
