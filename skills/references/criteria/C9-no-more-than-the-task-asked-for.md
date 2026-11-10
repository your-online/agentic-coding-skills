## C9 — No more than the task asked for

**Requirement.** The solution is the simplest one that satisfies the criteria, and
the change touches only what the task requires — which covers what the run does to
the world as well as what it does to the code. A push, a merge, a branch moved under
someone else's feet, a deploy, a write to a live system or a schedule that starts
running, where nobody asked for it, is more than the task asked for however well it
was executed. Simplest is counted in what a
maintainer has to hold in their head — parts, layers, special cases — not in lines.
Every changed line traces back to the request, or to cleaning up what this change
itself made redundant. No speculative
abstractions, no unrequested features, no drive-by refactors of code that was not
broken.

**Guidance.** This is the failure mode agents are worst at. Andrej Karpathy, writing
about [two months of agent
coding](https://x.com/karpathy/status/2015883857489522876), put it plainly: they
"really like to overcomplicate code and APIs, they bloat abstractions, they don't
clean up dead code after themselves". He describes the same agent producing a bloated
construction over a thousand lines, being asked "couldn't you just do this instead?",
and cutting it to a hundred without protest — so asking is cheap and usually works.
He notes the second half too: agents "change/remove comments and code they don't
sufficiently understand as side effects, even if orthogonal to the task". (The
[widely shared CLAUDE.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md)
that followed his post was written by others from his observations, not by him.)

Matt Pocock offers two questions that turn this into something you can check.
[The deletion
test](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md#L63):
imagine deleting the module — if complexity vanishes, it was a pass-through; if
complexity reappears across its callers, it was earning its keep. And on seams: [one
adapter means a hypothetical seam, two adapters means a real
one](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md#L65)
— so do not introduce a seam unless something actually varies across it. He files
[speculative generality, the middle man and shotgun
surgery](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md#L51-L55)
as smells worth naming when you see them.

Lasting actions deserve the cheaper of the two habits: agree what the run may touch
before it starts — which branch, which environment, what is a dry run — rather than
judging each write while it happens. What was agreed is then something the developer
can check the run against afterwards.

One way to get there, offered as an example and not as a step to follow: get robust
acceptance criteria and tests in place for the slice you are on, then minimise the
lines of code
iteratively against the green suite — simplify or delete, re-run, and when the suite
goes red you went too far, so take a small piece back. What survives is what was
needed, with the suite as the boundary. On Claude Code,
[`/simplify`](https://code.claude.com/docs/en/commands) does a pass of this over the
current diff; elsewhere the loop above is the same move by hand. It only works if the suite is trustworthy
first, which is C5 and C6, and it is one route among several.

**Evaluation questions.**

1. Does every changed line, and every lasting action outside the working tree, trace
   to the request or to cleaning up what this change itself orphaned?
2. Which abstraction, parameter or layer exists for a need the criteria do not have —
   and what happens to complexity if you delete it?
3. Was adjacent code, formatting or commentary changed without being asked?
4. Was code that was already dead, or a comment that was already stale, removed as a
   side trip rather than as its own agreed change?
5. Could a smaller version of this solution satisfy the same criteria, and what would
   break if you tried?
