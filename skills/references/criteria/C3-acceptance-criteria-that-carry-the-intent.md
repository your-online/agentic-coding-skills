## C3 — Acceptance criteria that carry the intent

**Requirement.** There is a set of acceptance criteria that is concrete, observable
and testable, that covers the normal, the awkward and the failing paths, and that
traces back to confirmed intent rather than to what happened to get built. Missing
criteria are asked for, not invented.

**Guidance.** Having the agent [interview you before it writes
anything](https://code.claude.com/docs/en/best-practices#let-claude-interview-you)
tends to surface more than writing criteria yourself; so does letting it [grill the
criteria](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md#L22)
afterwards for the scenario you did not name. Corrections you make mid-conversation
are criteria too — they are the ones most often lost. Writing criteria down before
implementation is what makes the difference visible between criteria that shaped the
build and criteria reverse-engineered from it afterwards. Before implementation means
before the slice you are about to build, not before the whole project: you cannot
know everything at the start, so you settle what would finish this slice and how you
would show it, build that, and let what it teaches you sharpen, adjust or drop
criteria for the next one. Criteria that move that way are the work going well; the
ones that only appear once the code exists are what this asks about.
[Non-goals](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md#L67-L69)
are worth as much as goals. Criteria repay the attack C7 describes as much as claims
do: give them to someone who did not write them and ask what an implementation could
do that satisfies every one of them and is still the wrong thing. A useful form of
that attack asks for one or more concrete, plausible implementations. Each one
satisfies the criteria literally while producing a wrong, unsafe or useless outcome.
For each one, the attacker points to the wording that admits it, says why the proposed
verification would accept it, and offers the smallest change to the wording plus a
check seen fail on that implementation before the tightened criterion is trusted.
It also looks for criteria that overlap or prescribe machinery where an observable
outcome would do; merging or removing those keeps the plan smaller without reopening
the loophole. The attacker follows the C7 pattern: fresh context, raw sources, no
earlier conclusion to inherit.

**Evaluation questions.**

1. Can each criterion be read as an observable outcome, or does it need
   interpretation before anyone can tell whether it holds?
2. Which confirmed intent and which mid-conversation corrections made it into the
   criteria, and which quietly did not?
3. Do the criteria reach beyond the happy path to the edge and failure behaviour
   that matters here?
4. Were the criteria for a slice written before that slice was built, or fitted to it
   afterwards?
5. What concrete wrong, unsafe or useless implementation satisfies the criteria
   literally, why would the proposed verification accept it, and which smallest
   tightening plus check seen fail closes that opening?
