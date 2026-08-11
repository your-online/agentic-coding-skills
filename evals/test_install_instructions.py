#!/usr/bin/env python3
"""The install instruction in the README, executed.

Three failures were reproduced with the instruction this replaces, and none of
them announced itself:

1. On a machine without `~/.claude/skills`, `cp -R` failed and installed nothing.
2. On a machine that already had the skill, `cp -R` copied the source directory
   *into* the target — `.../advise-me/advise-me/` — exited 0, and left the old
   SKILL.md as the one that loads. A silent no-op on exactly the upgrade path.
3. Nothing said you had to clone the repository and stand in it first.

An instruction is a claim about what happens when you run it, so it is tested by
running it: the shell blocks are extracted from the README and executed against a
throwaway HOME, once on an empty machine and once over an existing installation.
`test_the_old_instruction_still_nests` keeps the second case honest — it is the
red proof that the check can fail, run against the form that used to be there.

Nothing here may touch the real ~/.claude or ~/.codex: HOME is a tmpdir, and the
extracted block is refused if it mentions any absolute home path.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from rubric_source import README, ROOT, SKILL_NAMES

INSTALL_BLOCK = re.compile(
    r"^(Claude Code|Codex):\n\n```sh\n(.*?)```", re.MULTILINE | re.DOTALL
)


def install_blocks() -> "dict[str, str]":
    text = README.read_text(encoding="utf-8").split("## Install", 1)[1]
    return {m.group(1): m.group(2) for m in INSTALL_BLOCK.finditer(text)}


def run(script: str, home: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["sh", "-e", "-c", script],
        cwd=ROOT,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        capture_output=True,
        text=True,
    )


class InstallInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blocks = install_blocks()

    def test_the_readme_carries_one_block_per_platform(self):
        self.assertEqual(sorted(self.blocks), ["Claude Code", "Codex"])
        self.assertIn(".claude/skills", self.blocks["Claude Code"])
        self.assertIn(".codex/skills", self.blocks["Codex"])
        for name in SKILL_NAMES:
            for platform, block in self.blocks.items():
                with self.subTest(platform=platform, skill=name):
                    self.assertIn(name, block)

    def test_no_block_writes_outside_the_home_it_is_given(self):
        """A tilde follows HOME; an absolute /Users/... path would not."""
        for platform, block in self.blocks.items():
            with self.subTest(platform=platform):
                self.assertNotIn("/Users/", block)
                self.assertNotIn("/home/", block)
                self.assertNotIn("$HOME", block.replace('"$skill"', ""))

    def target_dir(self, home: Path, platform: str, skill: str) -> Path:
        root = ".claude" if platform == "Claude Code" else ".codex"
        return home / root / "skills" / skill

    def assert_installed(self, home: Path, platform: str):
        for skill in SKILL_NAMES:
            target = self.target_dir(home, platform, skill)
            with self.subTest(skill=skill):
                self.assertTrue((target / "SKILL.md").is_file(), f"{target} has no SKILL.md")
                self.assertFalse((target / skill).exists(), f"{target} is nested")
                self.assertEqual(
                    (target / "SKILL.md").read_text(encoding="utf-8"),
                    (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8"),
                    f"{target}/SKILL.md is not the version in this repository",
                )

    def test_a_fresh_machine_ends_up_with_all_three_skills(self):
        """Case 1: no skills directory at all — the old instruction installed nothing."""
        for platform, block in self.blocks.items():
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                result = run(block, home)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed(home, platform)

    def test_an_upgrade_replaces_the_old_version_instead_of_nesting_it(self):
        """Case 2: the target already exists — the old instruction was a silent no-op."""
        for platform, block in self.blocks.items():
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                for skill in SKILL_NAMES:
                    target = self.target_dir(home, platform, skill)
                    target.mkdir(parents=True)
                    (target / "SKILL.md").write_text("stale version 1.0\n", encoding="utf-8")
                    (target / "leftover.md").write_text("dropped in 2.0\n", encoding="utf-8")

                result = run(block, home)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed(home, platform)
                for skill in SKILL_NAMES:
                    leftover = self.target_dir(home, platform, skill) / "leftover.md"
                    self.assertFalse(leftover.exists(), f"{leftover} survived the upgrade")

    def test_the_old_instruction_still_nests(self):
        """The red proof: run the form the README used to carry, and watch it fail.

        Without this, a green upgrade test could mean the check is toothless
        rather than that the new instruction is right.
        """
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "skills" / "advise-me"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("stale version 1.0\n", encoding="utf-8")

            old = 'cp -R skills/advise-me ~/.claude/skills/advise-me'
            result = run(old, home)

            self.assertEqual(result.returncode, 0, "the old form failed loudly, it did not")
            self.assertTrue((target / "advise-me").is_dir(), "expected the nested directory")
            self.assertEqual(
                (target / "SKILL.md").read_text(encoding="utf-8"),
                "stale version 1.0\n",
                "expected the stale SKILL.md to still be the one that loads",
            )

    def test_the_old_instruction_installs_nothing_on_a_fresh_machine(self):
        """The other red proof: no skills directory, so the copy fails outright."""
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = run('cp -R skills/advise-me ~/.claude/skills/advise-me', home)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((home / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
