# What these skills themselves have to satisfy

Eleven points, in ordinary language, each with the test that guards it. These are
about the skills, not about the work they review — the rubric criteria live in
`skills/references/rubric.md`.

Run the guards with `uvx pytest evals/` from this directory.

1. **A criterion is a requirement, guidance and evaluation questions — in that
   order, each present once, with two to four questions.**
   Guarded by `evals/test_rubric_shape.py::test_every_criterion_has_the_three_parts_exactly_once_and_in_order`
   and `::test_each_criterion_asks_two_to_five_evaluation_questions`.

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

5. **The three skills you run stay three skills.** `advise-me` answers in chat,
   writes no file, reads transcript and diff itself, and works before any code
   exists; `review-my-work` writes one Markdown report, runs a falsifier and allows
   exactly one revision; `log-feedback` only ever appends one dated bullet in the
   developer's own words and borrows none of the reviewing machinery. What the
   skills read from — `skills/references/` — is not a fourth skill and carries no
   SKILL.md, so no platform offers it as a route.
   `advise-me` also sends an isolated judge to the background every time it answers,
   and may close by offering — never starting — a falsifier over its own advice.
   Guarded by `evals/test_skills.py::AdviseMeTests`, `::ReviewMyWorkTests`,
   `::LogFeedbackTests`,
   `::SelfTriggerTests::test_the_reference_is_not_a_skill_at_all` and
   `evals/test_isolation_and_model.py::AdviceIsAccompaniedTests`.

6. **The descriptions are disjunct, from each other and from the review skill
   already in the field.** A description is a trigger, not a summary: near-identical
   trigger sentences give the platform two candidates for one request. Every
   distinguishing marker belongs to exactly one skill, the two reviewing skills name
   what the other is for, and none of them borrows the neighbouring skill's
   vocabulary.
   Guarded by `evals/test_descriptions.py`.

7. **No skill decides on its own that a review is due, and none is ever
   self-judged.** The developer asks — in their own words or by name, which is a
   trigger and not a summons — and an isolated subagent does the judging; if
   isolation is impossible, nothing runs. Forward-looking advice is the one route
   that runs in the working context, because the wait for a spawned round lands
   exactly where the advice has to be usable and because the rubric is worth more
   in the session that continues; the boundary that keeps this from hollowing out
   the rule is that this route returns no verdict.
   Guarded by `evals/test_skills.py::SelfTriggerTests::test_no_skill_ever_triggers_itself`
   and `evals/test_isolation_and_model.py::IsolationTests`.

8. **The reviewing roles run on the strongest reasoning model of the platform they
   are on, a downgrade is never silent, and where the platform allows no model
   choice at all the run names the model that actually ran.** Two named Claude
   models as the whole rule made the Codex install impossible to obey; a Codex fork
   with the full history inherits the session's model and takes no override, so
   claiming the requirement was met there would be the same silent downgrade; and a
   silent downgrade is the one failure a review cannot report about itself.
   Guarded by `evals/test_isolation_and_model.py::ModelTests`.

9. **Both install steps in the README are the ones that were executed, and what
   arrives is the whole package.** Step 1 runs with the clone URL swapped for a local
   repository — the network is not this repository's to test, so
   `::test_step_one_names_a_real_repository_url` stands in for it by refusing a
   placeholder. Step 2 is one command, `./install.sh`, and the script behind it has
   to work on a machine without a skills directory, on a machine that already has an
   older installation — where a bare `cp -R` silently nests the new version inside
   the old one and leaves the old `SKILL.md` loading — from any working directory,
   and on a machine that has only one of the two platforms; with neither platform
   present it has to fail loudly. Every installed file is compared byte for byte,
   because an installer that drops the rubric leaves a skill that points at a
   reference with nothing in it, while every SKILL.md looks perfectly installed.
   The script installs whatever `skills/` holds rather than a list of names, so a new
   skill cannot stay behind. And an upgrade that fails leaves
   the working version standing: the copy goes beside the target and is moved into
   place only once it succeeded.
   Guarded by `evals/test_install_instructions.py`, which extracts the commands from
   the README and runs them against a throwaway home directory, with
   `::test_the_old_instruction_still_nests` and
   `::test_the_old_instruction_installs_nothing_on_a_fresh_machine` as its red tests
   and `::test_a_source_that_cannot_be_copied_leaves_the_installation_it_had` for the
   half-finished upgrade.

10. **The rubric exists once, and so do the rules for judging against it.** Both
    reviewing skills used to carry a copy of the rubric and a copy of the isolation
    and model rules, kept identical by a test — because a skill had to be installable
    on its own. They install together, so the copies are gone: the material lives in
    `skills/references/` and the skills read it by path. It was briefly a skill of
    its own, which cost a round trip to be handed a path and put a reference in the
    developer's skill list; it carries no SKILL.md now. A second `rubric.md` beside a
    skill that judges with it, or a rule restated in one, is the drift coming back.
    Guarded by `evals/test_skills.py::PackageLayoutTests` and
    `evals/test_isolation_and_model.py::OneWordingTests`.

11. **The report says which diff basis it used, and the bookkeeping lives in one
    place.** The developer is the only one who knows where the task really began, so
    the range is theirs to correct. Versions and changelogs used to sit in five
    files at once and drifted; there is one `CHANGELOG.md` for the package now, and
    nothing that ships carries a number of its own. A skill also names nothing that
    does not travel with it when it is installed.
    Guarded by
    `evals/test_isolation_and_model.py::SharedOutputRules::test_the_basis_compared_against_is_derived_and_named`,
    `evals/test_changelog.py` and
    `evals/test_install_instructions.py::test_nothing_installed_points_outside_the_package_that_ships_it`.
