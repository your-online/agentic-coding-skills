# What this skill itself has to satisfy

Eight points, in ordinary language, each with the test that guards it. These are
about the skill, not about the work it reviews — the rubric criteria live in
`skills/agentic-coding/references/rubric.md`.

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

5. **The two routes stay different.** Route 1 writes one Markdown report, runs a
   falsifier and allows exactly one revision; route 2 answers in chat, writes no
   file, runs no falsifier, and works without a diff.
   Guarded by `evals/test_routes.py::test_only_the_full_review_writes_a_file`,
   `::test_only_the_full_review_runs_a_falsifier_and_exactly_one_revision`,
   `::test_the_diff_is_required_in_route_one_and_optional_in_route_two` and
   `::test_route_two_looks_forward_instead_of_judging`.

6. **The review is never self-triggered and never self-judged.** The developer
   invokes it; an isolated subagent performs it; if isolation is impossible, nothing
   runs.
   Guarded by `evals/test_routes.py::test_neither_route_ever_triggers_itself` and
   `evals/test_isolation_and_model.py::test_the_main_agent_never_reviews_its_own_session`,
   `::test_missing_isolation_stops_the_review_instead_of_downgrading_it`.

7. **The reviewing roles run on Opus 5 or Opus 4.8, or the review does not run at
   all.** A silent downgrade to a lighter model is the one failure a review cannot
   report about itself.
   Guarded by `evals/test_isolation_and_model.py::test_every_reviewing_role_is_pinned_to_one_of_two_named_models`
   and `::test_an_unavailable_or_limited_model_is_a_hard_visible_failure`.

8. **The report says which diff basis it used, and the version is stated
   consistently.** The developer is the only one who knows where the task really
   began, so the range is theirs to correct; and feedback is only comparable when
   you can tell which rubric produced it.
   Guarded by `evals/test_routes.py::test_the_diff_basis_is_derived_and_always_reported`
   and `evals/test_versions.py` (skill, rubric and README name the same versions, and
   the current rubric version has a changelog line).
