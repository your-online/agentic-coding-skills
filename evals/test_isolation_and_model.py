#!/usr/bin/env python3
"""Who judges, and on what.

Both rules protect the same thing: a review that is worth less than it looks.
An agent grading the session it worked in has every prior conclusion in context
and will confirm itself; a reviewer quietly demoted to a lighter model returns
thinner challenges and softer findings, and the report reads exactly the same
either way. Neither failure announces itself, so a judgement from outside is the
requirement and a model downgrade has to be said out loud.

The model rule used to name two Claude models and allow nothing else. That made
the Codex install impossible to obey: Codex runs GPT models and cannot spawn
`claude-opus-5`, so by its own rule the skill could never produce anything
there. The intent underneath was never "these two names" but "the strongest
reasoning model this platform has, and never a silent downgrade", so that is
what is written down and what is checked — with the two Claude names kept as the
Claude Code example rather than as the whole rule.

That still assumed the model can be chosen. On Codex it often cannot: a fork with
the full history, which is what a reviewer that reads the whole transcript needs,
inherits the model of the session and takes no override. The requirement stays what
it was, but where the platform decides, the skill names the model that actually ran
instead of reporting a requirement it did not meet.

Both rules hold for advise-me and review-my-work, and both used to be written out
in full in each of them — the same duplication the rubric itself had. They live
once now, in `references/rubric.md`, which both skills read, so this file reads
them there. `OneWordingTests` is what keeps them from growing back: the two skills
point at the rules and do not restate them. log-feedback judges nothing and
spawns nothing, so none of this applies to it.

advise-me went through both extremes. It spawned a judge for advice, which took
roughly twice the wall-clock with the wait falling exactly where the advice is
supposed to be usable, mid-work; then it spawned nothing at all and was forbidden
to return a verdict, which bought speed by refusing to answer the question that was
asked — in practice it opened by explaining what it would not do. It now does both
at once and pays for neither: it answers immediately from the sources in the working
context, and the isolated judge runs in the background rather than in front of the
answer. The boundary that keeps the isolation rule from being hollowed out is no
longer "no verdict" but "not the verdict": the session's own read never stands alone
or last, which is what `AdviceIsAccompaniedTests` holds down.
"""

import unittest

from rubric_source import REVIEWING_SKILLS, RUBRIC, flat, skill_text


class SharedRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = flat(RUBRIC.read_text(encoding="utf-8"))
        cls.reviewing = {name: flat(skill_text(name)) for name in REVIEWING_SKILLS}

    def in_the_rules(self, *fragments: str):
        for fragment in fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.rules)

    def in_no_reviewing_skill(self, *fragments: str):
        for name, text in self.reviewing.items():
            for fragment in fragments:
                with self.subTest(skill=name, fragment=fragment):
                    self.assertNotIn(fragment, text)


class IsolationTests(SharedRules):
    def test_the_judgement_that_counts_comes_from_outside_the_session(self):
        self.in_the_rules(
            "A judgement from outside is what counts",
            "subagent with fresh context",
        )

    def test_the_subagent_gets_raw_sources_and_no_expected_outcome(self):
        self.in_the_rules(
            "no expected outcome",
            "no earlier conclusion",
            "no summary written for it",
            "Hand the judging subagent the complete rubric",
        )

    def test_a_missing_isolated_judge_is_said_instead_of_hidden(self):
        """Nothing in a self-judgement looks different from a judged one, so the
        one thing that must never happen quietly is it standing in for one."""
        self.in_the_rules(
            "If an isolated judge cannot be spawned at all, say so where the answer lands",
            "rather than letting a self-judgement stand as if it came from outside",
        )


class AdviceIsAccompaniedTests(SharedRules):
    """The working context may read its own work — it is the only context that can
    do so while the work is still going on. What it may not do is be the only one
    that did. These assertions are the price of that permission: a judge goes out
    every time, and the session's own read never gets the last word."""

    def test_the_rules_allow_a_self_read_only_alongside_an_isolated_one(self):
        self.in_the_rules(
            "A session may read its own work against these criteria",
            "alongside an isolated judgement, never instead of one",
            "never presents its own read as the verdict",
        )

    def test_advise_me_spawns_the_judge_in_the_background_before_answering(self):
        advice = self.reviewing["advise-me"]
        self.assertIn("Spawn one judging subagent, in the background", advice)
        self.assertIn("Send it off before you write your own answer", advice)
        self.assertNotIn("Spawn nothing", advice)

    def test_advise_me_reports_the_judge_and_keeps_the_disagreement(self):
        advice = self.reviewing["advise-me"]
        self.assertIn("Report the subagent's judgement when it lands", advice)
        self.assertIn("where it contradicts yours", advice)
        self.assertIn("Do not smooth the two into one voice", advice)

    def test_advise_me_opens_with_substance_and_not_with_its_own_limits(self):
        """The route used to open by explaining what it was not allowed to do.
        That paragraph was the whole answer's first impression and told the
        developer nothing about their work."""
        advice = self.reviewing["advise-me"]
        self.assertIn("Open with the substance", advice)
        self.assertIn("no note that the rubric has been loaded", advice)
        self.assertIn("no disclaimer about judging your own work", advice)


class SharedOutputRules(SharedRules):
    """Two rules moved into the rubric because both skills carried them in
    different words: which range a judgement compared against, and that a
    judgement is prose rather than marks. Moving them left only the negative
    half behind — `OneWordingTests` checks the skills no longer restate them —
    and a negative half alone is satisfied by the rules existing nowhere at all.
    Delete both paragraphs from the rubric and the skills would still point,
    still greenly, at nothing. These are the positive half."""

    def test_the_basis_compared_against_is_derived_and_named(self):
        self.in_the_rules(
            "Name the basis you compared against",
            "Uncommitted work is compared against `HEAD`",
            "the commit the session or task started from",
            "`HEAD~n` when nothing better identifies it",
            "Diff basis: <ref> (<why>)",
        )

    def test_a_judgement_is_prose_and_never_a_mark_beside_a_criterion(self):
        self.in_the_rules(
            "No labels, no table, no number standing in for a judgement",
            "Do not attach a label to each criterion",
            "do not put a percentage anywhere",
        )


class ModelTests(SharedRules):
    def test_every_reviewing_role_runs_on_the_strongest_model_of_its_platform(self):
        self.in_the_rules(
            "reviewer, falsifier, adviser",
            "runs on the strongest reasoning model the platform offers",
        )

    def test_the_claude_models_are_an_example_and_not_the_whole_rule(self):
        """A named model is guidance for one platform. As a requirement it makes
        every other platform unable to comply — which is what shut Codex out."""
        self.in_the_rules(
            "In Claude Code that is Opus 5 (`claude-opus-5`)",
            "Opus 4.8 (`claude-opus-4-8`) when Opus 5 is out of reach",
            "on another platform it is that platform's own strongest reasoning model",
        )
        self.assertNotIn("There is no third option", self.rules)

    def test_a_platform_without_a_model_choice_is_said_out_loud(self):
        """The rule assumed you can always pick the model. A Codex fork that
        carries the full history inherits the session's model and accepts no
        override — which is exactly the fork a reviewer needs. Pretending the
        requirement was met there is the same silent downgrade it forbids
        everywhere else, so what actually ran gets named — in whichever form the
        skill that ran it answers, since the rule now covers both."""
        self.in_the_rules(
            "Where the platform does not let you choose",
            "a Codex fork inherits the session's model and takes no override",
            "the run happens on the session's model, and that is said where the answer lands "
            "instead of claiming the requirement was met",
        )

    def test_a_downgrade_is_never_silent(self):
        self.in_the_rules(
            "Never quietly fall back to a lighter or faster model",
            "say which model did run",
            "usage limits block it",
        )


class RemedyTests(SharedRules):
    """A judgement used to be allowed to stop at "your verification is weak".
    The rubric's guidance is full of mechanisms — the falsifier round under C7,
    the ways under C6 to show a check can go red, the deletion test under C9 —
    and none of them reached the developer as advice, because "Suggestions and
    patterns, never demands" reads, to an agent that has to advise, as a reason
    to stay abstract. Those are two different acts: the rubric as a standard
    demands no method of anyone, advice to this developer about this work names
    one. The full wording of that rule lives in the rubric's judging rules; each
    reviewing skill asks it of its own output by pointing there, and advise-me
    asks it of the judge it sends out too. These assertions hold both halves
    down: the rule stays in the rubric, and the pointers stay in the skills."""

    def test_the_rules_ask_a_remedy_of_every_point_raised(self):
        self.in_the_rules(
            "A finding names its remedy",
            "which mechanism, over which claim or file, which check",
            "The guidance under each criterion is the first place to look",
            "a better fit that is not in the guidance is equally welcome, as long as it is named",
        )

    def test_the_standard_and_the_advice_are_told_apart(self):
        """Without this distinction the vagueness comes back: the next reader of
        "never demands" re-derives the caution and plays it safe again."""
        self.in_the_rules(
            "a rule about the standard, not about the advice",
            "advice to this developer, about this work, right now",
        )

    def test_each_reviewing_skill_asks_the_remedy_of_its_own_output(self):
        for name, text in self.reviewing.items():
            with self.subTest(skill=name):
                self.assertIn(
                    "carries its remedy, the way the rubric's judging rules ask", text
                )

    def test_advise_me_asks_the_same_of_its_background_judge(self):
        self.assertIn(
            "every point carrying its remedy", self.reviewing["advise-me"]
        )

    def test_the_full_wording_stays_in_the_rubric(self):
        self.in_no_reviewing_skill(
            "A finding names its remedy",
            "which mechanism, over which claim or file, which check",
        )


class OneWordingTests(SharedRules):
    """Pointing at the rules is what replaced the copy in each skill. Restating
    them is how that copy comes back, one paragraph at a time."""

    def test_both_reviewing_skills_send_the_reader_to_the_rubric_file(self):
        for name, text in self.reviewing.items():
            with self.subTest(skill=name):
                self.assertIn("`references/rubric.md`", text)
                self.assertIn("material to read, not a skill", text)
                self.assertIn("before you start", text)

    def test_neither_reviewing_skill_invokes_a_reference_skill(self):
        """The rubric stopped being a skill because invoking one to read a file
        is a round trip that returns a path. Nothing may send anyone back."""
        self.in_no_reviewing_skill(
            "/agentic-coding-rubric",
            "`agentic-coding-rubric` skill",
        )

    def test_neither_reviewing_skill_restates_the_rules(self):
        self.in_no_reviewing_skill(
            "A judgement from outside is what counts",
            "strongest reasoning model",
            "`claude-opus-5`",
            "Read this file whole",
        )


if __name__ == "__main__":
    unittest.main()
