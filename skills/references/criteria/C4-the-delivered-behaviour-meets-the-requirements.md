## C4 — The delivered behaviour meets the requirements

**Requirement.** The thing that was built actually does what the criteria describe,
on the version that is being handed over — including the awkward paths, not only the
main one.

**Guidance.** Walking each criterion against an observation of the real behaviour is
usually enough; the gaps show up as criteria you cannot point at anything for.
[Judging the reached end
state](https://www.anthropic.com/engineering/multi-agent-research-system#appendix)
rather than whether the agent followed a particular route keeps this honest. Where
output is textual or user-facing, [checking it against the
source](https://www.anthropic.com/engineering/multi-agent-research-system#effective-evaluation-of-agents)
rather than against how convincing it reads catches invented entities and numbers.

**Evaluation questions.**

1. For each material criterion, what was observed that shows it holds on this
   version?
2. Which criteria are supported only by [the assertion that they
   hold](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work)?
3. Where behaviour is user-facing or semantic, was the real result inspected rather
   than a proxy for it?
