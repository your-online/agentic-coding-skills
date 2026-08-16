*Example. Copy the shape, not the content. What is open and what was settled sit in
front of the requirements. A requirement is checkable against the product, a decision
only against the conversation — so it carries a name and a date instead of a check,
and appears below as well when it has visible consequences.*

# Acceptance criteria — retry failed payment webhooks

## Open questions

**Does a webhook that never succeeds page someone at night?** *Marco decides. Blocks
nothing.* Nothing else here pages out of hours and finance reads the unpaid report at
09:00, so the cheap answer is no.

## Decisions

**Where do the retries live — in the handler or in the queue?** In the queue; the
handler has to answer Stripe within 10 seconds. *2026-08-14, Anne.* Nothing to test
on its own — B1 is what the outside sees.

**Do we retry a 4xx as well?** No — two of the last three 4xx failures were our own
validation bug, and retrying hides those. *2026-08-14, Anne.* Visible, so it is also
B2 below.

## Functional requirements

<details><summary><strong>B1 — A webhook that fails with a 5xx or a timeout is retried after 1, 5 and 25 minutes, then stops.</strong></summary>

*Source:* Anne, ticket PAY-780. *Expected behaviour:* force a 500 on staging; three
attempts at the stated intervals and no fourth.

*Evidence that it behaves that way:* `evidence/B1/` — queue log with timestamps.

</details>

<details><summary><strong>B2 — A webhook that fails with a 4xx is not retried and is recorded as rejected.</strong></summary>

*Expected behaviour:* send a malformed payload; one attempt, and the rejection is in
the log with its reason.

*Evidence:* `evidence/B2/` — the rejection log line.

</details>

## Technical requirements

<details><summary><strong>T1 — The same webhook id delivered twice leaves one order.</strong></summary>

*Expected behaviour:* replay a stored delivery; one order, and the second attempt is
logged as a duplicate.

*Evidence that it behaves that way:* `evidence/T1/` — replay log plus the order query.

</details>
