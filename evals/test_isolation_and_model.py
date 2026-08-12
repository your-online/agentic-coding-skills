#!/usr/bin/env python3
"""Who judges, and on what.

Both rules protect the same thing: a review that is worth less than it looks.
An agent grading the session it worked in has every prior conclusion in context
and will confirm itself; a reviewer quietly demoted to a lighter model returns
thinner challenges and softer findings, and the report reads exactly the same
either way. Neither failure announces itself, so isolation is a hard stop and a
model downgrade has to be said out loud.

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
once now, in the reference skill both of those consult, so this file reads them
there. `OneWordingTests` is what keeps them from growing back: the two skills
point at the rules and do not restate them. log-feedback judges nothing and
spawns nothing, so none of this applies to it.

Isolation once covered advise-me too, by spawning a subagent for advice as well.
Measured against advice read straight into the working context, the spawned round
took roughly twice the wall-clock — the wait falling exactly where the advice is
supposed to be usable, mid-work — and it threw away the rubric context the session
still needed. The requirement moved rather than the test being weakened: advice runs
in the main context now, and what keeps the isolation rule from being hollowed out
is that the same route may not return a verdict. That boundary is what
`test_the_one_route_without_isolation_is_scoped_and_returns_no_verdict` holds down,
so the coverage the old assertion gave has a named replacement rather than a gap.
"""

import unittest

from rubric_source import REVIEWING_SKILLS, RUBRIC_SKILL, flat, skill_text


class SharedRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = flat(skill_text(RUBRIC_SKILL))
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
    def test_the_main_agent_never_judges_its_own_session(self):
        self.in_the_rules("Never judge your own work", "subagent with fresh context")

    def test_the_subagent_gets_raw_sources_and_no_expected_outcome(self):
        self.in_the_rules(
            "no expected outcome",
            "no earlier conclusion",
            "no summary you wrote yourself",
            "Hand the subagent the complete",
        )

    def test_missing_isolation_stops_the_run_instead_of_downgrading_it(self):
        self.in_the_rules("If an isolated subagent cannot be spawned, say so and run nothing")

    def test_the_one_route_without_isolation_is_scoped_and_returns_no_verdict(self):
        """Advice in the working context was measured at roughly half the wall-clock
        of a spawned round, and the rubric stays in the context that keeps working.
        What pays for it is the boundary: no isolated judge, so no verdict. Without
        that line the exception swallows the rule — the cheap route would answer the
        question the expensive one exists for."""
        self.in_the_rules(
            "Forward-looking advice about how to go on from here is",
            "not a judgement",
            "`advise-me` runs in the main context",
            "never returns a verdict",
        )
        advice = self.reviewing["advise-me"]
        self.assertIn("Spawn nothing", advice)
        self.assertIn("it never doubles as a verdict on what has been built", advice)
        self.assertNotIn("Spawn one isolated subagent", advice)


class ModelTests(SharedRules):
    def test_every_reviewing_role_runs_on_the_strongest_model_of_its_platform(self):
        self.in_the_rules(
            "the reviewer, the falsifier, the adviser",
            "runs on the strongest reasoning model the platform you are on offers",
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
            "Where the platform does not let you choose the model at all",
            "a Codex fork inherits the session's model and takes no override",
            "the run happens on the session's model, and you say that where the answer lands, "
            "in the report or in the chat answer, instead of claiming the requirement was met",
        )

    def test_a_downgrade_is_never_silent(self):
        self.in_the_rules(
            "Never quietly fall back to a lighter or faster model",
            "say so explicitly instead of continuing in silence",
            "usage limits block it",
            "tell the developer which model the run actually used",
        )


class OneWordingTests(SharedRules):
    """Pointing at the rules is what replaced the copy in each skill. Restating
    them is how that copy comes back, one paragraph at a time."""

    def test_both_reviewing_skills_send_the_reader_to_the_reference_skill(self):
        for name, text in self.reviewing.items():
            with self.subTest(skill=name):
                self.assertIn("use the `/agentic-coding-rubric` skill", text)
                self.assertIn("a reference to consult, not a session to run", text)
                self.assertIn("Read it before you start", text)

    def test_neither_reviewing_skill_restates_the_rules(self):
        self.in_no_reviewing_skill(
            "Never judge your own work",
            "Model requirement",
            "strongest reasoning model",
            "Read the rubric whole",
        )


if __name__ == "__main__":
    unittest.main()
