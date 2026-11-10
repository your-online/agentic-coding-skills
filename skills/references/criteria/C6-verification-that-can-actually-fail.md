## C6 — Verification that can actually fail

**Requirement.** The checks that support the important claims are able to fail, and
it has been shown that they do — a check that cannot go red proves nothing. Material
findings from review or from production become a lasting check where that is
practical.

**Guidance.** [Seeing a test red before the implementation makes it
green](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L36)
is the cheapest demonstration there is. Where that moment has passed, breaking the
behaviour on purpose and watching the check catch it does the same job; so does
[mutating the
implementation](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf),
or feeding the checker a known-bad input and confirming it rejects it. The question
worth asking of any test is: if this test claims to protect X, how would I show that
it does not — a question someone other than its author answers better, which is the
move C7 describes for the claims themselves. A test that was changed, narrowed or removed is a finding until someone
shows otherwise, and the showing falls to whoever changed it: that the requirement
itself moved or the test was demonstrably wrong, that the check standing in its place
was seen red before it went green, and that the coverage which survives is equal or
better and named rather than asserted. Short of all three, what you are looking at is
a test weakened to get past a failure, which is the thing this criterion exists to
catch. A repair made in the same movement as the fix hides exactly that, so it is
made visible on its own — its own commit, its own line in the handover — where a
reader can still see which came first.

**Evaluation questions.**

1. For the important claims, what shows that the supporting check can go red?
2. Is there a check whose logic makes failure impossible — [an assertion that
   repeats the implementation](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md#L31),
   a mock of the very integration under test?
3. Was any test changed, narrowed or removed — and for each one, what shows that the
   requirement moved or the test was wrong, that its replacement went red first, and
   which coverage took its place?
4. Did the findings that came out of review or from a bug leave a lasting check
   behind?
