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

Both rules hold for advise-me and review-my-work. log-feedback judges nothing
and spawns nothing, so neither applies to it.
"""

import unittest

from rubric_source import RUBRIC_SKILLS, flat, skill_text


class BothReviewingSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {name: flat(skill_text(name)) for name in RUBRIC_SKILLS}

    def in_every_skill(self, *fragments: str):
        for name, text in self.texts.items():
            for fragment in fragments:
                with self.subTest(skill=name, fragment=fragment):
                    self.assertIn(fragment, text)

    def in_no_skill(self, *fragments: str):
        for name, text in self.texts.items():
            for fragment in fragments:
                with self.subTest(skill=name, fragment=fragment):
                    self.assertNotIn(fragment, text)


class IsolationTests(BothReviewingSkills):
    def test_the_main_agent_never_judges_its_own_session(self):
        self.in_every_skill("Never judge your own work", "subagent with fresh context")

    def test_the_subagent_gets_raw_sources_and_no_expected_outcome(self):
        self.in_every_skill(
            "no expected outcome",
            "no earlier conclusion",
            "no summary you wrote yourself",
            "Hand the subagent the complete",
        )

    def test_missing_isolation_stops_the_run_instead_of_downgrading_it(self):
        self.in_every_skill(
            "If an isolated subagent cannot be spawned, say so and run nothing"
        )


class ModelTests(BothReviewingSkills):
    def test_every_reviewing_role_runs_on_the_strongest_model_of_its_platform(self):
        self.in_every_skill(
            "the reviewer, the falsifier, the feedback subagent",
            "runs on the strongest reasoning model the platform you are on offers",
        )

    def test_the_claude_models_are_an_example_and_not_the_whole_rule(self):
        """A named model is guidance for one platform. As a requirement it makes
        every other platform unable to comply — which is what shut Codex out."""
        self.in_every_skill(
            "In Claude Code that is Opus 5 (`claude-opus-5`)",
            "Opus 4.8 (`claude-opus-4-8`) when Opus 5 is out of reach",
            "on another platform it is that platform's own strongest reasoning model",
        )
        self.in_no_skill("There is no third option")

    def test_a_downgrade_is_never_silent(self):
        self.in_every_skill(
            "Never quietly fall back to a lighter or faster model",
            "say so explicitly instead of continuing in silence",
            "usage limits block it",
            "which model the",
        )


if __name__ == "__main__":
    unittest.main()
