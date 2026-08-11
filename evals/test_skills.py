#!/usr/bin/env python3
"""Three skills that must stay three skills.

The cheap failure here is convergence: advise-me grows a report file, or
review-my-work loses its falsifier because one pass looked good enough, or
log-feedback starts summarising and reshaping the developer's words. They answer
different questions — what should I do next, what did I build, what did I think
of the process — and the differences that carry that split are the file, the
falsifier, and who the feedback is about. The diff basis is checked separately:
a review of the wrong range is worse than no review, and only the developer can
spot that, which they can only do if the report says which range it used.
"""

import unittest

from rubric_source import (
    README,
    REFERENCE_FILES,
    RUBRIC_SKILL,
    RUNNABLE_SKILLS,
    SKILLS_DIR,
    SKILL_NAMES,
    flat,
    skill_text,
)


class SelfTriggerTests(unittest.TestCase):
    def test_no_skill_ever_triggers_itself(self):
        for name in RUNNABLE_SKILLS:
            with self.subTest(skill=name):
                text = flat(skill_text(name))
                self.assertIn("only when the developer asks for it by name", text)
                self.assertIn("Never start it on your own initiative", text)

    def test_the_reference_skill_starts_nothing_at_all(self):
        """It is material to read, so it has nothing to trigger. Saying it runs
        only on request would make it sound like a fourth route."""
        text = flat(skill_text(RUBRIC_SKILL))
        self.assertIn("A reference to consult, not a session to run", text)
        self.assertIn("nothing here starts anything", text)


class PackageLayoutTests(unittest.TestCase):
    """One rubric, in one place.

    Both reviewing skills used to carry their own copy, kept identical by a
    test, because a skill has to be installable on its own. They install
    together now, so the copy is gone and the rubric lives once. What is worth
    guarding is that it stays that way: a second `rubric.md` appearing next to a
    skill that judges with it is the old drift coming back.
    """

    def test_the_package_holds_exactly_these_skills(self):
        self.assertEqual(sorted(p.name for p in SKILLS_DIR.iterdir()), sorted(SKILL_NAMES))

    def test_only_the_reference_skill_carries_the_rubric(self):
        for name in SKILL_NAMES:
            present = sorted(p.name for p in (SKILLS_DIR / name).rglob("*") if p.is_file())
            with self.subTest(skill=name):
                if name == RUBRIC_SKILL:
                    self.assertEqual(present, sorted(("SKILL.md",) + REFERENCE_FILES))
                else:
                    self.assertEqual(present, ["SKILL.md"])


class AdviseMeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(skill_text("advise-me"))

    def test_it_writes_no_file_and_answers_in_chat(self):
        self.assertIn("Write no file", self.text)
        self.assertIn("in chat only", self.text)
        self.assertNotIn("Markdown file", self.text)

    def test_it_runs_no_falsifier_and_no_revision_round(self):
        self.assertIn("No falsifier, no revision round", self.text)

    def test_the_diff_is_optional(self):
        self.assertIn("The diff is optional", self.text)
        self.assertIn("this route is also used before any code exists", self.text)

    def test_it_looks_forward_instead_of_judging(self):
        self.assertIn("forward-looking", self.text)
        self.assertIn("Not a verdict on what has happened", self.text)

    def test_it_points_at_the_review_skill_for_the_other_job(self):
        self.assertIn("review-my-work", self.text)


class ReviewMyWorkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(skill_text("review-my-work"))

    def test_it_writes_one_markdown_report_and_never_overwrites(self):
        self.assertIn("One Markdown file", self.text)
        self.assertIn("docs/reviews/agentic-coding-review-", self.text)
        self.assertIn("Never overwrite an existing report", self.text)
        self.assertIn("The developer chooses where it goes", self.text)

    def test_it_runs_a_falsifier_and_exactly_one_revision(self):
        self.assertIn("Spawn one falsifier", self.text)
        self.assertIn("exactly one revision", self.text)

    def test_the_diff_is_a_source_and_not_optional(self):
        self.assertIn("as a diff", self.text)
        self.assertNotIn("The diff is optional", self.text)

    def test_the_diff_basis_is_derived_and_always_reported(self):
        self.assertIn("Is there uncommitted work? Then diff against `HEAD`", self.text)
        self.assertIn("the commit this session or task started from", self.text)
        self.assertIn("`HEAD~n`", self.text)
        self.assertIn("State the basis in the report, always", self.text)
        self.assertIn("Diff basis: <ref> (<why>)", self.text)

    def test_the_report_stays_free_form_and_unlabelled(self):
        self.assertIn("The form is free", self.text)
        self.assertIn("Do not attach a label to each criterion", self.text)
        self.assertIn("do not put a percentage anywhere", self.text)
        self.assertIn("what is good, what is weak, what is missing", self.text)

    def test_the_stripped_machinery_stays_stripped(self):
        self.assertIn(
            "There is no orchestrator layer, no scorer, no validator and no snapshot ceremony.",
            self.text,
        )

    def test_it_points_at_the_advice_skill_for_the_other_job(self):
        self.assertIn("advise-me", self.text)


class LogFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(skill_text("log-feedback"))

    def test_it_records_the_developers_feedback_and_never_gives_any(self):
        self.assertIn("It never says anything about their work", self.text)
        self.assertIn("nothing here reviews or advises", self.text)

    def test_it_appends_one_dated_bullet_to_the_repository_it_is_run_in(self):
        self.assertIn("`docs/feedback.md`, in the repository the developer is working in",
                      self.text)
        self.assertIn("Create the `docs/` directory and the file when they do not exist",
                      self.text)
        self.assertIn("One bullet, in the developer's own words, shortened to a single sentence",
                      self.text)
        self.assertIn("`YYYY-MM-DD`", self.text)

    def test_it_only_ever_appends(self):
        self.assertIn("Only ever append", self.text)
        self.assertIn("Never rewrite, reorder, reword or remove a line", self.text)
        self.assertIn("New entries go at the end of the file", self.text)

    def test_it_stays_a_bullet_instead_of_a_template(self):
        self.assertIn("No heading per entry, no template", self.text)
        self.assertIn("no metadata block of any kind", self.text)
        self.assertIn("Only when the remark genuinely does not fit in one sentence", self.text)

    def test_the_line_is_confirmed_before_it_is_written(self):
        self.assertIn("Show them the exact line and ask whether it says what they meant",
                      self.text)
        self.assertIn("Only after they confirm does anything get written", self.text)

    def test_it_borrows_no_machinery_from_the_reviewing_skills(self):
        """It has no judgement to make, so it needs no rubric, no subagent and no
        diff. Every one of those appearing here means the split has started to
        blur back together."""
        for stranger in ("rubric.md", "agentic-coding-rubric", "Spawn", "subagent", "Diff basis"):
            with self.subTest(fragment=stranger):
                self.assertNotIn(stranger, self.text)


class OrderTests(unittest.TestCase):
    """Advice comes while you work, the review comes after. Every place the two
    are listed together says them in that order, because a reader takes the
    first one named as the default entry point."""

    def order_holds(self, text: str, where: str):
        advise, review = text.index("advise-me"), text.index("review-my-work")
        self.assertLess(advise, review, f"{where} names the full review before the advice")

    def test_the_readme_names_the_advice_route_first(self):
        self.order_holds(README.read_text(encoding="utf-8").split("## The skills", 1)[1],
                         "README")

    def test_the_structure_listing_keeps_the_same_order(self):
        listing = README.read_text(encoding="utf-8").split("## Structure", 1)[1]
        self.order_holds(listing, "the README structure listing")

    def test_the_install_loop_keeps_the_same_order(self):
        install = README.read_text(encoding="utf-8").split("## Install", 1)[1]
        self.order_holds(install, "the install command")


if __name__ == "__main__":
    unittest.main()
