#!/usr/bin/env python3
"""Frontmatter that a real YAML parser accepts.

Claude Code and Codex read the frontmatter tolerantly enough that a broken block
still works, so nothing in the suite noticed when a description carried a `: ` of
its own — `... look ahead: that is what ...` — and YAML started reading the rest
of the sentence as a nested mapping. GitHub is not tolerant: it refused to render
the skill and showed the parse error instead. The frontmatter is the first thing
anyone sees of a skill, so it has to be valid YAML, name the skill it sits in,
and say so here rather than on the file page of whoever opens it.
"""

import unittest

from rubric_source import (
    SKILL_NAMES,
    FrontmatterError,
    load_frontmatter,
    skill_frontmatter,
    yaml,
)

#: The description that broke GitHub, kept verbatim so the checker is measured
#: against the real defect and not against a tidied-up imitation of it.
BROKEN = (
    "---\n"
    "name: review-my-work\n"
    "description: Review the work. Not for a verdict-free look ahead: that is "
    "what the advise-me skill is for.\n"
    "---\n"
)


class FrontmatterTests(unittest.TestCase):
    def test_every_skill_has_frontmatter_a_yaml_parser_accepts(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                try:
                    loaded = skill_frontmatter(name)
                except FrontmatterError as error:
                    self.fail(f"{name} has invalid frontmatter: {error}")
                self.assertIsInstance(loaded, dict)

    def test_every_skill_declares_a_name_and_a_description_as_text(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                loaded = skill_frontmatter(name)
                for field in ("name", "description"):
                    self.assertIn(field, loaded, f"{name} declares no {field}")
                    self.assertIsInstance(loaded[field], str)
                    self.assertTrue(loaded[field].strip(), f"{name} has an empty {field}")

    def test_the_declared_name_is_the_directory_the_skill_is_installed_from(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                self.assertEqual(skill_frontmatter(name)["name"], name)

    def test_the_check_rejects_the_description_that_broke_github(self):
        """Whichever parser this environment has, it must still catch the bug
        this test was written for — a passing suite on a machine without pyyaml
        would otherwise mean nothing."""
        with self.assertRaises(FrontmatterError):
            load_frontmatter(BROKEN)

    def test_the_check_accepts_the_same_description_once_it_is_quoted(self):
        loaded = load_frontmatter(BROKEN.replace(
            "description: Review", "description: 'Review").replace(
            "is for.\n---", "is for.'\n---"))
        self.assertIn("look ahead: that is what", loaded["description"])

    def test_the_environment_reports_which_parser_ran(self):
        """Not an assertion about pyyaml being present — a record of which of the
        two paths the rest of this file exercised here."""
        print(f"\nfrontmatter parser: {'pyyaml' if yaml else 'built-in fallback'}")


if __name__ == "__main__":
    unittest.main()
