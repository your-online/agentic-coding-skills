#!/usr/bin/env python3
"""The install instruction in the README, executed.

An instruction is a claim about what happens when you run it, so it is tested by
running it: the shell blocks are extracted from the README and executed against a
throwaway HOME.

Step 1 clones over the network, which a test may not depend on: it would be slow,
it would fail on a machine without a route to GitHub, and it would prove something
about the remote rather than about the instruction. So the clone is run for real
with exactly one substitution — the URL is swapped for a throwaway git repository
built from this directory. Everything else about step 1 stays as written, and
step 2 runs unmodified against the resulting clone. What that leaves untested is
the one thing this repository does not control: whether the URL in the README
resolves. `test_step_one_names_a_real_repository_url` is the stand-in for that —
it refuses a placeholder, and holds the repository name in the URL against the
directory step 1 stands in, so a name left behind by a rename fails here.

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
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from rubric_source import (
    LEARNING,
    README,
    REFERENCE_FILES,
    ROOT,
    RUBRIC,
    INSTALLED_DIRS,
    REFERENCE_DIR,
    RUNNABLE_SKILLS,
)

STEP_BLOCK = re.compile(r"^### Step (\d+) — [^\n]*\n\n```sh\n(.*?)```", re.MULTILINE | re.DOTALL)
CLONE_URL = re.compile(r"git clone (\S+)")

PLATFORM_ROOT = {"Claude Code": ".claude", "Codex": ".codex"}


def install_steps() -> "dict[str, str]":
    text = README.read_text(encoding="utf-8").split("## Install", 1)[1]
    return {m.group(1): m.group(2) for m in STEP_BLOCK.finditer(text)}


def local_origin(where: Path) -> Path:
    """A git repository holding what this directory holds, to clone from instead
    of over the network."""
    origin = where / "origin"
    shutil.copytree(
        ROOT, origin, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache")
    )
    git = ["git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval"]
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "origin"]):
        subprocess.run(git + args, cwd=origin, check=True, capture_output=True)
    return origin


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

    def test_step_one_names_a_real_repository_url(self):
        """A README that ships inside the repository it tells you to clone can
        name it. `<repository-url>` was a blank the reader had to fill in from
        somewhere this page never said, and a URL left over from a rename is that
        same blank with a plausible face: GitHub redirects it, so nothing
        complains, and the name the reader walks away with is the wrong one.
        Refusing a placeholder does not catch that. The directory the rest of
        step 1 stands in does — it is named after the repository, so the two have
        to agree."""
        url = CLONE_URL.search(self.steps["1"])
        self.assertIsNotNone(url, "step 1 has no git clone")
        self.assertRegex(url.group(1), r"^(https://|git@)\S+\.git$")
        self.assertNotIn("<", url.group(1))

        repository = url.group(1).rsplit("/", 1)[-1].removesuffix(".git")
        directory = re.search(r"^cd (\S+)", self.steps["1"], re.MULTILINE)
        self.assertIsNotNone(directory, "step 1 has no cd")
        self.assertEqual(
            directory.group(1),
            repository,
            f"step 1 clones {repository} and then stands in {directory.group(1)}",
        )

    def test_step_one_and_step_two_together_install_from_a_clone(self):
        """Both steps, in order, with the URL swapped for a local repository — the
        one substitution the docstring explains."""
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as work:
            home = Path(tmp)
            (home / ".claude").mkdir()
            origin = local_origin(Path(work))

            url = CLONE_URL.search(self.steps["1"]).group(1)
            script = self.steps["1"].replace(url, str(origin)) + self.install

            result = run(script, home, cwd=Path(work))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_installed(home, "Claude Code")

    def test_nothing_installed_points_outside_the_package_that_ships_it(self):
        """What arrives on a machine is `skills/`, never the repository around
        it. A file that names `evals/` or a path above itself is telling the
        reader to look somewhere the installer never put anything."""
        for path in [ROOT / "skills" / name / "SKILL.md" for name in RUNNABLE_SKILLS] + [
            RUBRIC,
            LEARNING,
        ]:
            with self.subTest(file=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                for stale in ("evaluate-acbp", "../../", "slim/", "evals/", "uvx pytest"):
                    self.assertNotIn(stale, text)

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
        """A skill is its SKILL.md *and* what that file points at.

        Checking only SKILL.md passes an installer that drops the rubric, and the
        damage is invisible until someone follows the pointer in `advise-me` or
        `review-my-work` to `references/rubric.md` and finds an empty directory.
        So the whole payload is compared byte for byte, the reference directory
        has to arrive with both reference files and without a SKILL.md of its own
        — that is what keeps it out of the developer's skill list — and no skill
        may carry a rubric, which is how the second copy would come back.
        """
        for skill in INSTALLED_DIRS:
            source = ROOT / "skills" / skill
            target = self.target_dir(home, platform, skill)
            with self.subTest(directory=skill):
                self.assertFalse((target / skill).exists(), f"{target} is nested")
                expected = sorted(p.relative_to(source) for p in source.rglob("*") if p.is_file())
                if skill == REFERENCE_DIR:
                    self.assertNotIn(Path("SKILL.md"), expected, f"{source} is a skill again")
                    for ref in REFERENCE_FILES:
                        self.assertIn(Path(ref), expected, f"{source} lost {ref}")
                else:
                    self.assertIn(Path("SKILL.md"), expected, f"{source} has no SKILL.md")
                    for ref in REFERENCE_FILES:
                        self.assertFalse(
                            (target / ref).exists(),
                            f"{target} carries a {ref} only {REFERENCE_DIR} should have",
                        )
                for relative in expected:
                    self.assertEqual(
                        (target / relative).read_bytes()
                        if (target / relative).is_file()
                        else None,
                        (source / relative).read_bytes(),
                        f"{target / relative} is missing or is not the version in this repository",
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
                for skill in INSTALLED_DIRS:
                    self.assertIn(str(self.target_dir(home, platform, skill)), result.stdout)

    def test_an_upgrade_replaces_the_old_version_instead_of_nesting_it(self):
        """Case b: the target already exists — the old instruction was a silent no-op."""
        for platform in PLATFORM_ROOT:
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                for skill in INSTALLED_DIRS:
                    target = self.target_dir(home, platform, skill)
                    target.mkdir(parents=True)
                    (target / "SKILL.md").write_text("stale version 1.0\n", encoding="utf-8")
                    (target / "leftover.md").write_text("dropped in 2.0\n", encoding="utf-8")

                result = run(self.install, home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed(home, platform)
                for skill in INSTALLED_DIRS:
                    leftover = self.target_dir(home, platform, skill) / "leftover.md"
                    self.assertFalse(leftover.exists(), f"{leftover} survived the upgrade")

    def test_a_source_that_cannot_be_copied_leaves_the_installation_it_had(self):
        """Case f: the upgrade fails halfway — an incomplete clone here, a full
        disk or an interrupt in the field.

        The installer used to remove the target before copying, so a copy that
        never happened took a working skill with it: the installed skill was gone
        and the script exited 1. An upgrade that fails has to leave you where you
        were, not worse off.

        The break is a source file the copy cannot read, which is what a broken
        source looks like to `cp`. Deleting a skill from the source would no
        longer do it: the installer takes whatever `skills/` holds, so a skill
        that is not there is not a failed copy, it is a skill that does not exist.
        """
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as work:
            home = Path(tmp)
            (home / ".claude").mkdir()
            self.assertEqual(run(self.install, home).returncode, 0)
            installed = self.target_dir(home, "Claude Code", "log-feedback")
            (installed / "marker.md").write_text("the installation that was here\n")

            broken = Path(work) / "broken"
            shutil.copytree(
                ROOT, broken, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache")
            )
            unreadable = broken / "skills" / "log-feedback" / "SKILL.md"
            unreadable.chmod(0o000)
            try:
                result = run(f"{broken}/install.sh", home)
            finally:
                unreadable.chmod(0o644)

            self.assertNotEqual(result.returncode, 0, "an unreadable source installed silently")
            self.assertTrue(
                (installed / "marker.md").is_file(),
                f"{installed} was removed before the copy that then failed",
            )
            self.assertTrue((installed / "SKILL.md").is_file(), f"{installed} lost its SKILL.md")
            leftovers = sorted(installed.parent.glob("*.incoming"))
            self.assertEqual([], leftovers, "a half-finished copy was left behind")

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
