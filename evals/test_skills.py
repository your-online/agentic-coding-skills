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
    INSTALLED_DIRS,
    README,
    REFERENCE_DIR,
    REFERENCE_FILES,
    RUNNABLE_SKILLS,
    SKILLS_DIR,
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

    def test_the_reference_is_not_a_skill_at_all(self):
        """It used to be one, and its SKILL.md existed to say where a file was.
        A platform lists whatever has a SKILL.md, so the developer's skill list
        offered a reference beside three routes — and reading the rubric meant
        invoking a skill to be handed a path. Having no SKILL.md is what makes
        that unrepeatable."""
        self.assertFalse((SKILLS_DIR / REFERENCE_DIR / "SKILL.md").exists())


class PackageLayoutTests(unittest.TestCase):
    """One rubric, in one place.

    Both reviewing skills used to carry their own copy, kept identical by a
    test, because a skill has to be installable on its own. They install
    together now, so the copy is gone and the rubric lives once. What is worth
    guarding is that it stays that way: a second `rubric.md` appearing next to a
    skill that judges with it is the old drift coming back.
    """

    def test_the_package_holds_exactly_these_directories(self):
        self.assertEqual(sorted(p.name for p in SKILLS_DIR.iterdir()), sorted(INSTALLED_DIRS))

    def test_only_the_reference_directory_carries_the_rubric(self):
        for name in INSTALLED_DIRS:
            present = sorted(p.name for p in (SKILLS_DIR / name).rglob("*") if p.is_file())
            with self.subTest(directory=name):
                if name == REFERENCE_DIR:
                    self.assertEqual(present, sorted(REFERENCE_FILES))
                else:
                    self.assertEqual(present, ["SKILL.md"])


class AdviseMeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(skill_text("advise-me"))

    def test_it_writes_no_file_and_answers_in_chat(self):
        self.assertIn("answers in chat, writes no file", self.text)
        self.assertNotIn("Markdown file", self.text)

    def test_it_reads_both_sources_itself(self):
        """It advised from what it remembered doing once, which is the one
        account of the work guaranteed to match the choices being judged."""
        self.assertIn("The whole transcript of this session", self.text)
        self.assertIn("The code produced so far, as a diff", self.text)
        self.assertIn("Do not advise from memory of what you did — read the diff", self.text)

    def test_it_still_works_before_any_code_exists(self):
        self.assertIn("Before any code exists there is no diff", self.text)
        self.assertIn("the transcript alone carries the answer", self.text)

    def test_it_judges_against_the_criteria_and_says_what_to_do_next(self):
        self.assertIn("Where does this work meet the criteria, where does it not", self.text)
        self.assertIn("what would you do differently from here", self.text)

    def test_it_takes_the_shape_the_shared_rules_ask_for(self):
        """The no-labels rule was written out here in one wording and in
        review-my-work in another — the same rule, two phrasings, which is where
        drift starts. It binds every judgement, so it moved to the rubric and
        this route points at it."""
        self.assertIn("takes the shape those same rules ask for", self.text)

    def test_it_points_at_the_review_skill_for_the_other_job(self):
        self.assertIn("review-my-work", self.text)

    def test_the_falsifier_over_the_advice_is_an_offer_and_never_automatic(self):
        """The background judge goes out every time; a falsifier over the advice
        itself does not. It exists only as a closing offer, one short line after
        both answers have landed, and nothing runs until the developer says yes
        — so an eager session cannot quietly turn the advice round into a
        review nobody asked for."""
        self.assertIn("Offer a falsifier over the advice — never start one", self.text)
        self.assertIn("a single short line", self.text)
        self.assertIn("asked to knock it down", self.text)
        self.assertIn("Nothing runs until the developer says yes", self.text)
        self.assertIn("Never spawn it on your own initiative", self.text)
        self.assertIn("never make it the default", self.text)

    def test_the_offer_is_recommended_and_says_why_it_is_worth_it(self):
        """Permission to offer is not an offer. Left at "you may", the line goes
        unsaid on exactly the answers that need it most — this route's advice is
        half-written by the session that made the choices, which is the half with
        a reason to be gentle. So it is recommended wherever something hangs on
        the answer, and skipped only where nothing does."""
        self.assertIn("Strongly recommended after every advice that anything hangs on", self.text)
        self.assertIn("the half most likely to be gentle", self.text)
        self.assertIn("Skip the offer when nothing much rests on the answer", self.text)

    def test_the_offer_is_phrased_for_someone_who_never_heard_of_a_falsifier(self):
        """The developer being advised is not the author of this rubric. An offer
        naming the machinery asks them to evaluate a word instead of a benefit."""
        self.assertIn("Say what it buys, not what it is called", self.text)
        self.assertIn("never heard the word falsifier", self.text)

    def test_the_offer_never_stands_in_front_of_the_advice(self):
        """An offer phrased as a question before the answer is a toll booth: the
        developer asked for advice and gets a decision to make instead."""
        self.assertIn(
            "never turn the offer into a question the developer has to answer "
            "before they get their advice",
            self.text,
        )


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

    def test_the_report_stays_free_form_and_takes_its_shape_from_the_rules(self):
        """Both routes carried the same no-labels rule in different words, and
        the review carried its own copy of the diff-basis procedure. Both bind
        every judgement, so both live in the rubric now and this file points."""
        self.assertIn("The form is free", self.text)
        self.assertIn("what is good, what is weak, what is missing", self.text)
        self.assertIn("the way the rubric's judging rules ask", self.text)
        self.assertIn("on the basis the rubric's judging rules derive", self.text)

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
