#!/usr/bin/env python3
"""The install instruction in the README, executed.

An instruction is a claim about what happens when you run it, so it is tested by
running it: the shell block for step 2 is extracted from the README and executed
against a throwaway HOME. Step 1 is a clone, which cannot be run here, so its
block is only checked for shape.

The failures this guards against were all reproduced, and none of them announced
itself:

1. On a machine with `~/.claude` but no `skills/` underneath, `cp -R` failed and
   installed nothing.
2. On a machine that already had the skill, `cp -R` copied the source directory
   *into* the target — `.../advise-me/advise-me/` — exited 0, and left the old
   SKILL.md as the one that loads. A silent no-op on exactly the upgrade path.
3. Nothing said you had to clone the repository and stand in it first.

`test_the_old_instruction_still_nests` and
`test_the_old_instruction_installs_nothing_on_a_fresh_machine` keep the checks
honest: they run the naive form and prove the assertions bite, so a green
upgrade test means the installer is right rather than that the test is toothless.

Nothing here may touch the real ~/.claude or ~/.codex: HOME is a tmpdir, and the
extracted block is refused if it mentions any absolute home path.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from rubric_source import README, ROOT, SKILL_NAMES

STEP_BLOCK = re.compile(r"^### Step (\d+) — [^\n]*\n\n```sh\n(.*?)```", re.MULTILINE | re.DOTALL)

PLATFORM_ROOT = {"Claude Code": ".claude", "Codex": ".codex"}


def install_steps() -> "dict[str, str]":
    text = README.read_text(encoding="utf-8").split("## Install", 1)[1]
    return {m.group(1): m.group(2) for m in STEP_BLOCK.finditer(text)}


def run(script: str, home: Path, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["sh", "-e", "-c", script],
        cwd=cwd,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        capture_output=True,
        text=True,
    )


class InstallInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.steps = install_steps()
        cls.install = cls.steps["2"]

    def test_the_readme_carries_two_steps_and_one_install_command(self):
        """Clone and stand in it, then one command that does the rest."""
        self.assertEqual(sorted(self.steps), ["1", "2"])
        self.assertIn("git clone", self.steps["1"])
        self.assertIn("cd ", self.steps["1"])
        self.assertEqual(self.install.strip(), "./install.sh")

    def test_the_readme_holds_no_platform_specific_install_block(self):
        """The platform detection lives in the script, not in the instruction."""
        text = README.read_text(encoding="utf-8").split("## Install", 1)[1]
        self.assertNotRegex(text, r"^(Claude Code|Codex):\n\n```sh", re.MULTILINE)

    def test_no_block_writes_outside_the_home_it_is_given(self):
        """A tilde follows HOME; an absolute /Users/... path would not."""
        for step, block in self.steps.items():
            with self.subTest(step=step):
                self.assertNotIn("/Users/", block)
                self.assertNotIn("/home/", block)

    def target_dir(self, home: Path, platform: str, skill: str) -> Path:
        return home / PLATFORM_ROOT[platform] / "skills" / skill

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

    def test_a_platform_without_a_skills_directory_ends_up_with_all_three_skills(self):
        """Case a: the platform is installed, but has never held a skill."""
        for platform in PLATFORM_ROOT:
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                (home / PLATFORM_ROOT[platform]).mkdir()

                result = run(self.install, home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed(home, platform)
                for skill in SKILL_NAMES:
                    self.assertIn(str(self.target_dir(home, platform, skill)), result.stdout)

    def test_an_upgrade_replaces_the_old_version_instead_of_nesting_it(self):
        """Case b: the target already exists — the old instruction was a silent no-op."""
        for platform in PLATFORM_ROOT:
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                for skill in SKILL_NAMES:
                    target = self.target_dir(home, platform, skill)
                    target.mkdir(parents=True)
                    (target / "SKILL.md").write_text("stale version 1.0\n", encoding="utf-8")
                    (target / "leftover.md").write_text("dropped in 2.0\n", encoding="utf-8")

                result = run(self.install, home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed(home, platform)
                for skill in SKILL_NAMES:
                    leftover = self.target_dir(home, platform, skill) / "leftover.md"
                    self.assertFalse(leftover.exists(), f"{leftover} survived the upgrade")

    def test_the_script_works_from_any_working_directory(self):
        """Case c: the README says to stand in the clone, but the script may not
        depend on it. Only the path to the script changes, not what is run."""
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as elsewhere:
            home = Path(tmp)
            (home / ".claude").mkdir()

            script = self.install.strip().replace("./", f"{ROOT}/", 1)
            result = run(script, home, cwd=Path(elsewhere))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_installed(home, "Claude Code")
            self.assertEqual([], list(Path(elsewhere).iterdir()), "it wrote into the cwd")

    def test_only_the_platform_that_is_present_is_installed_into(self):
        """Case d: Codex but no Claude Code — nothing may appear in ~/.claude."""
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()

            result = run(self.install, home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_installed(home, "Codex")
            self.assertFalse((home / ".claude").exists(), "it created a platform that was absent")

    def test_neither_platform_present_fails_loudly_and_installs_nothing(self):
        """Case e: no home to install into is an error, not a silent success."""
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = run(self.install, home)

            self.assertNotEqual(result.returncode, 0, "it exited 0 with nothing installed")
            self.assertIn(".claude", result.stderr)
            self.assertIn(".codex", result.stderr)
            self.assertEqual([], list(home.iterdir()), f"{home} is not empty")

    def test_the_old_instruction_still_nests(self):
        """The red proof: run the form the README used to carry, and watch it fail.

        Without this, a green upgrade test could mean the check is toothless
        rather than that the installer is right.
        """
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "skills" / "advise-me"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("stale version 1.0\n", encoding="utf-8")

            old = "cp -R skills/advise-me ~/.claude/skills/advise-me"
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
            (home / ".claude").mkdir()

            result = run("cp -R skills/advise-me ~/.claude/skills/advise-me", home)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((home / ".claude" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
