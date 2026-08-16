# Learning materials

One to three sources per criterion group, each with a line on why it helps. This is
reading material for developers who want to get better at a criterion; it is not part
of the review itself. Every link here was verified before it was added — a criterion
without a source beats an invented one.

The rubric itself now links straight to the passage behind a particular sentence.
This list is the wider reading around the same criteria, so the two overlap where the
rubric takes the direct route.

## C1 + C2 — Context, assumptions, own research and open questions

- [How coding agents read your code](https://modem.dev/blog/how-coding-agents-read-your-code) — how an agent searches a codebase, and therefore why gathering context is a step you design rather than hope for.
- [Advanced context engineering for coding agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md) — how much of a vague task the agent can answer from the codebase itself, which is exactly what you should not be asking the author.
- [Finding your unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns) — separating what you can find out yourself from what is genuinely someone else's decision; that remainder is what a refinement question should be.
- [Agentic coding and persistent returns to expertise](https://www.anthropic.com/research/claude-code-expertise) (Anthropic) — across ~400,000 real sessions, the expert behaviour around supplying context and validating output is what makes the difference.

## C3 — Acceptance criteria

- [Claude Code best practices, "Let Claude interview you"](https://code.claude.com/docs/en/best-practices) — let the agent question you first, then write a spec with non-goals and a verification step.
- [Spec Kit](https://github.com/github/spec-kit) — a toolkit that forces a specification before implementation, if you want the workflow made explicit.
- [Grilling skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) — an instruction set that makes the agent interrogate you until the assumptions are on the table; the `grill-me` entry in the same repo is only a wrapper around it.

## C4 + C5 — Delivered behaviour and test coverage

- [Claude Code best practices, "Give Claude a way to verify its work"](https://code.claude.com/docs/en/best-practices) — agree before building which check proves success; without one, "looks done" is your only signal.
- [Building a multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (Anthropic) — judge the end state reached against the criterion, not whether the agent followed a particular path.
- [Do coverage and mutation scores of LLM-generated test suites correlate with their effectiveness? (Replicability Study)](https://arxiv.org/abs/2607.22880) (Zhao, Zhou and Cohen, 2026) — the aggregate measures over a generated suite are context-dependent: where the code under test may itself be faulty, they stop being reliable indicators, so check coverage per criterion instead.

## C6 — Verification that can fail

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic) — contains the blunt rule "it is unacceptable to remove or edit tests", and shows browser automation as an end-to-end check through the real entry point.
- [When a model games its tests](https://metr.org/blog/2026-06-26-gpt-5-6-sol/) (METR) — a model learning to bypass tests rather than solve the problem; the reason evidence has to be able to go red.
- [Are mutants a valid substitute for real faults?](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) (Just et al., FSE 2014) — mutation testing predicts detection of real faults, which is a concrete answer to "can this evidence go red?".
- [Matt Pocock's tdd skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) — red before green as a rule of the loop, plus a catalogue of tests that cannot fail, starting with the tautological assertion.

## C7 — Evidence

- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Anthropic) — grader types, partial credit, and the trap of graders that always pass; read transcripts to check your own judge.
- [Judging LLM-as-a-judge (MT-Bench)](https://arxiv.org/abs/2306.05685) — position, verbosity and self-enhancement bias in model judges; why an evaluator has to be isolated and calibrated.
- [Who validates the validators?](https://arxiv.org/abs/2404.12272) — criteria drift: judging outputs changes your criteria, so version the rubric and the labels together.

## C8 + C9 — Maintainability and not overbuilding

- [Andrej Karpathy on two months of agent coding](https://x.com/karpathy/status/2015883857489522876) — the failure modes first-hand: agents overcomplicate code and APIs, bloat abstractions, leave dead code behind, and change things orthogonal to the task. (The widely shared CLAUDE.md derived from this post, at [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md), is concrete and useful, but it was written by others from his observations — it is not his.)
- [Matt Pocock's skills repo](https://github.com/mattpocock/skills) — the code-review skill names speculative generality, middle man and shotgun surgery; the codebase-design skill supplies the deletion test and the one-adapter-versus-two-adapters rule for seams.
- [Claude Code best practices, "Write an effective CLAUDE.md"](https://code.claude.com/docs/en/best-practices) — put architecture choices and conventions where the agent always sees them, so changes stay inside the house rules.
- [Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) (Anthropic) — where the "agree what the run may touch before it starts" habit comes from: filesystem and network bounds, and stepped autonomy with an escalation at the edge. C9 asks whether a lasting action was asked for; this is how you stop the question arising.
