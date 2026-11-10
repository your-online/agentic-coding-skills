## C5 — Tests that cover what matters

**Requirement.** The material acceptance criteria have verification that was
actually built and actually runs, covering the scenarios that matter for each one.
Where a criterion has no automated check, that is a stated gap rather than a silence.

**Guidance.** Deciding per criterion how it will be shown to work, before building,
tends to produce a [thinner and better-aimed
suite](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L22)
than writing tests afterwards. That decision is taken per slice: writing all the
tests first and all the implementation after produces bulk tests of imagined
behaviour, which check the shape of things rather than what anyone does with them and
go numb to real change. Working in [vertical
slices](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L40)
instead — one criterion, the check that shows it, the code that satisfies it, then
the next — keeps each check aimed at behaviour someone asked for, and lets the slice
you just finished inform the criteria for the one after it. Coverage per criterion
says more than a test count: a
large generated suite can still miss the one scenario the feature exists for, and
[coverage and mutation figures over a generated
suite](https://arxiv.org/abs/2607.22880) stop being reliable indicators where the
code under test may itself be faulty. Which scenario a suite misses is the hardest
thing to see from inside it, so it repays the attack C7 describes: hand the criteria
and the verification to a fresh agent that built neither, and let it argue that the
one does not cover the other. Not everything needs a unit test — [an
inspection, a recorded run or a
demo](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work)
can be the right verification, as long as someone other than the author can repeat
it.

**Evaluation questions.**

1. Which criterion does each material test map to, and which criteria map to nothing?
2. Do the tests exercise the awkward inputs and the failure paths, or only the shape
   the feature was designed around?
3. Are there tests that skip themselves, run only under certain conditions, or were
   never executed on this version?
