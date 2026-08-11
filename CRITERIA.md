# What these skills themselves have to satisfy

Eleven points, in ordinary language, each with the test that guards it. These are
about the skills, not about the work they review — the rubric criteria live in
`references/rubric.md`.

Run the guards with `uvx pytest evals/` from this directory.

1. **A criterion is a requirement, guidance and evaluation questions — in that
   order, each present once, with two to four questions.**
   Guarded by `evals/test_rubric_shape.py::test_every_criterion_has_the_three_parts_exactly_once_and_in_order`
   and `::test_each_criterion_asks_two_to_four_evaluation_questions`.

2. **The rubric stays compact: between eight and ten criteria, numbered in order.**
   It replaced a twenty-two criterion rubric and the pull back towards that is real.
   Guarded by `evals/test_rubric_shape.py::test_the_rubric_stays_compact`.

3. **The rubric uses no machine vocabulary.** No verdict labels, no criticality
   keywords, no gates, no percentages, no scores. The detector is proven to bite
   before it is trusted.
   Guarded by `evals/test_rubric_language.py::test_the_rubric_is_free_of_machine_vocabulary`,
   with `::test_the_detector_catches_planted_violations` as its own red test.

4. **Guidance suggests and never demands; the rubric prescribes no way of working.**
   Guarded by `evals/test_rubric_shape.py::test_guidance_is_offered_and_never_demanded`.

5. **The three skills stay three skills.** `advise-me` answers in chat, writes no
   file, runs no falsifier and works without a diff; `review-my-work` writes one
   Markdown report, runs a falsifier and allows exactly one revision;
   `log-feedback` only ever appends one dated bullet in the developer's own words
   and borrows none of the reviewing machinery.
   Guarded by `evals/test_skills.py::AdviseMeTests`, `::ReviewMyWorkTests` and
   `::LogFeedbackTests`.

6. **The three descriptions are disjunct, from each other and from the review skill
   already in the field.** A description is a trigger, not a summary: near-identical
   trigger sentences give the platform two candidates for one request. Every
   distinguishing marker belongs to exactly one skill, the two reviewing skills name
   what the other is for, and none of them borrows the neighbouring skill's
   vocabulary.
   Guarded by `evals/test_descriptions.py`.

7. **Nothing is ever self-triggered and never self-judged.** The developer invokes
   it; an isolated subagent performs the judging; if isolation is impossible, nothing
   runs.
   Guarded by `evals/test_skills.py::SelfTriggerTests::test_no_skill_ever_triggers_itself`
   and `evals/test_isolation_and_model.py::IsolationTests`.

8. **The reviewing roles run on the strongest reasoning model of the platform they
   are on, and a downgrade is never silent.** Two named Claude models as the whole
   rule made the Codex install impossible to obey; a silent downgrade is the one
   failure a review cannot report about itself.
   Guarded by `evals/test_isolation_and_model.py::ModelTests`.

9. **The install instruction in the README is the one that was executed.** It is one
   command, `./install.sh`, and the script behind it has to work on a machine without
   a skills directory, on a machine that already has an older installation — where a
   bare `cp -R` silently nests the new version inside the old one and leaves the old
   `SKILL.md` loading — from any working directory, and on a machine that has only
   one of the two platforms; with neither platform present it has to fail loudly.
   Guarded by `evals/test_install_instructions.py`, which extracts the command from
   the README and runs it against a throwaway home directory, with
   `::test_the_old_instruction_still_nests` and
   `::test_the_old_instruction_installs_nothing_on_a_fresh_machine` as its red tests.

10. **The rubric copies never drift from the source.** Two skills carry the rubric
    and a skill has to be installable on its own, so the copies are real files; one
    byte of difference is a red run. `log-feedback` carries no copy at all.
    Guarded by `evals/test_reference_sync.py`.

11. **The report says which diff basis it used, and the versions are stated
    consistently.** The developer is the only one who knows where the task really
    began, so the range is theirs to correct; and feedback is only comparable when
    you can tell which rubric produced it. A skill also names nothing that does not
    travel with it when it is installed.
    Guarded by `evals/test_skills.py::ReviewMyWorkTests::test_the_diff_basis_is_derived_and_always_reported`
    and `evals/test_versions.py` (one skill version across the three skills, the
    rubric version they name, a changelog line per version, and no dead reference in
    an installed file).
