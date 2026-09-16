# Evidence rules

Distilled from the sources of the
[acceptatiecriteria-en-bewijs-template](https://github.com/your-online/acceptatiecriteria-en-bewijs-template)
(SOC 2 audit practice, AWS continuous-auditing anti-patterns, Trail of Bits mutation testing,
LLM-as-judge research, SpecBench reward hacking, Playwright/asciinema evidence practice, and the
agentic-coding-skills rubric C6/C7). Whoever fills in or judges evidence reads this first.

## The one test question

**If the claim were false, would this evidence still look exactly the same?** If yes, it proves
nothing. A green run without output, an HTTP 200 without payload, "tests pass" without a
transcript, a check that cannot turn red: all of those survive a false claim. Everything below
is an elaboration of this one question.

## Hard requirements — not trade-offs, just do them

1. **Evidence is created at the moment of the check.** Evidence assembled afterwards (a later
   screenshot, a retold outcome) is structurally weaker and a recognized anti-pattern in audit
   practice. Have the check write its own evidence.
2. **Every script output starts with an environment fingerprint**: hostname, OS version, user,
   timestamp, and the commit SHA or image digest of what is being tested. Evidence without a
   time reference and origin is almost always rejected in audits; the machine and the moment
   must be visible in the output itself, not in a claim next to it.
3. **Version binding.** Evidence must demonstrably belong to the exact version being delivered.
   Yesterday's evidence does not cover today's code; without a commit/digest in the output,
   staleness cannot be ruled out. Collect on a clean, committed tree — and keep the generated
   evidence files themselves out of the dirty check (gitignore them, check with
   `git status --porcelain -uno`), otherwise the collection run pollutes the very version
   binding it must prove.
4. **Literal output, including the command.** Show what was executed, not only the outcome —
   that enables replay and makes gaming visible. Never shorten, rewrite, or summarize.
5. **Positive and negative assertion.** "X is refused" needs "Y does work" as its own
   criterion; otherwise a refusal cannot be told apart from a broken measurement. And the
   negative test proves a restriction *works*, not merely that it exists.
6. **Evidence binds directly to one criterion.** An artifact that "says something about it" is
   insufficient; it must carry exactly *this* criterion. No reusing one screenshot for five
   criteria.
7. **Recurring or multi-instance checks: no single snapshot.** One run document per run,
   machine, or environment; the fingerprints then show different hostnames. A single artifact
   is rarely enough for something that must work cyclically.
8. **Archive with the delivery.** CI keeps artifacts for 30–90 days and overwrites reports per
   run; the run document must be standalone with everything inside it (Save as file).
9. **Separation of roles.** Whoever filled in the evidence does not judge it. The falsifier has
   fresh context and no stake in the outcome. The human signs and carries the residual risk.
10. **Run binding — and it is not the same as version binding.** Evidence must demonstrably come
    from *one* collection run that *finished*. Two artifacts agreeing on a fingerprint only proves
    they saw the same state, not that one run produced both: two independent processes reading the
    same database write the same hash by construction. So give every artifact a run identifier that
    the collector generates once per run, require the artifacts to carry the *same* one, and have
    the collector write a closing result line only into the artifacts whose phase actually ran in
    that run. Watch the last part: a loop that stamps every artifact it can find, guarded by a file
    existence check, hands a completion marker to files this run never touched — it reads as proof
    of a finished run and is not. Both failures are silent and both survive a false claim, which is
    exactly what requirement 1's question is for.
11. **Collection must be resumable without breaking the binding.** A long chain that can only run
    whole restarts entirely on an unrelated hiccup — a container name clash, a flaky runtime — and
    each restart is another chance to hit the next one. Split it into phases and let a later phase
    be skipped, but only when the evidence itself says skipping is allowed: recompute the
    fingerprint over the live state and refuse on mismatch. Add a staleness bound and *derive* it
    from the data rather than picking a number — clock-relative seed data keeps its fingerprint
    while its meaning drifts, so find the tightest margin in the fixture and stay well inside it.

## Strength of evidence forms, strongest to weakest

Pick the strongest form that fits each criterion; one strong beats three weak.

1. **Config dump plus diff against a recorded baseline.** Machine-readable and diffable.
2. **Positive and negative assertion with exit code.**
3. **Evidence bundle per criterion**: commands, stdout/stderr, exit code, timestamp, and
   environment fingerprint as one unit.
4. **Independent anchor**: CI run with permalink, or append-only log with hash chain; traceable
   outside the agent.
5. **Hash or checksum** of an image, lockfile, or policy file. Proves identity, not behavior.
6. **Terminal recording (asciinema, .cast).** Textual, small (~8% of video), searchable,
   replayable at any speed; always above a screenshot or video of a terminal.
7. **UI trace (Playwright).** DOM snapshots, network, and console in one recording; answers
   "why", not just "what", and is hard to fake. Archive it yourself — CI purges it.
8. **Screenshot.** Proves only the state at that moment. Only for criteria where a graphical
   interface genuinely must be in view. Requirements: timestamp visible, system/environment
   recognizable in the image (platform name, navigation path), not cropped so far the context
   is gone. Confusing production and test environments makes the evidence worthless.
9. **Short screen recording, preferably gif.** Only for behavior that can exclusively be seen
   in motion. Video is heavy, shares poorly, and never gets watched; recording slows the run.
10. **Golden-set run for probabilistic (LLM-judged) criteria.** For behavior judged by a
    model rather than an assertion: a fixed golden set with hard subsets that must score 100%
    (e.g. every injection attempt caught), plus a deliberately dumb baseline that must fail
    (a regex stand-in scoring well would prove the set measures keywords, not judgment), plus
    a stop rule against tuning on the set itself — a score that keeps shifting while you tune
    on a handful of cases is overfit, not evidence.
11. **An agent's verdict (agent findings).** Weaker than programmatic evidence, but valid
    within the conditions below. Never when a programmatic form is possible.

## Conditions for an agent verdict as evidence

- **A current flagship model.** The often-cited false-positive research was measured on models
  that are now far surpassed; the requirement is the strength of the judge.
- **Fresh context with no stake in the outcome.** An agent that just did the work or wrote the
  evidence confirms its own work (self-preference). For high stakes: a different model family
  than the maker, or multiple judges — a single LLM verdict is manipulable and
  non-deterministic.
- **Every claim points at something inspectable**: a file line, a log line, or a screenshot.
  "No evidence found" is a valid result. Without source material, a judge rewards confident
  hallucinations.
- **Binary verdict** (VALID/REFUTED, met/not met) over a numeric scale: less variance, no false
  precision. Never reward length or confidence.
- **The outcome is evidence, not the final verdict.** For decisions about access or security, a
  human signs.

## Pitfalls

**Reward hacking.** Agents get to green by modifying the test or the verifier itself, by
memorizing outcomes (lookup tables that recognize validation tests), or by serving exactly the
visible tests while coherent behavior is missing — frontier models saturate visible tests
(~100%) and fall far back on held-out compositional tests. Countermeasures: keep the
verification script outside the building agent's write permissions; evidence shows the executed
commands, not only the outcome; a change to test or baseline files in the same change is a
finding until the contrary is shown; test compositions and end-to-end behavior, not only
isolated features.

**Mutant drift.** Mutation checks that patch literal code strings silently stop applying
after a refactor: the mutant reports "not applied", the tally quietly shrinks, and the suite
still looks green. A mutant that no longer applies is a red result, not a skipped one — fix
the mutant or the claim. Run mutation evidence (and its falsifier round) against the frozen
commit SHA of the delivery, never against a moving tree.

**Coverage theater.** Coverage measures execution, not verification: code that runs without
anything being asserted about it still counts. A test only proves something if it fails on
wrong behavior — show it red (test before the fix, temporarily break the behavior, or mutation
testing focused on the diff). When fixing such a mutation: first establish whether the mutated
behavior was a real requirement or an implementation accident, otherwise the test freezes an
accident.

**Evidence theater.** More artifacts is not more certainty. Three weak screenshots create the
impression of substantiation without making a single claim solid; the collection itself becomes
the goal. One form that survives the test question is enough.

**Silence that reads as coverage.** Explicitly name what was *not* checked and which paths to
the same result stayed untested. A list without gaps suggests a completeness that is not there;
the reader must be able to tell "checked and good" from "not checked".
