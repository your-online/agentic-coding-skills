*Example. Copy the shape, not the content. The criterion is the summary line;
source, expected behaviour and evidence live inside it, so the list reads as
criteria until you open one. Evidence is a path, not a promise.*

# Acceptance criteria — retry failed payment webhooks

## Decisions

**Where do the retries live — in the handler or in the queue?** In the queue. The
handler has to answer Stripe within 10 seconds, so it cannot wait between
attempts. Costs us: a failed webhook is visible in two places. *2026-08-14, Anne.*

**Do we retry a 4xx as well?** No, rejected on the first attempt. Two of the last
three 4xx failures were our own validation bug, and retrying hides those.
*2026-08-14, Anne.*

## Functional requirements

<details><summary><strong>B1 — A webhook that fails with a 5xx or a timeout is retried after 1, 5 and 25 minutes, then stops.</strong></summary>

*Source:* Anne, ticket PAY-780. Roughly one drop a week.

*Expected behaviour:* force a 500 on staging; the three attempts appear in the
queue log at the stated intervals and the fourth does not.

*Evidence that it behaves that way:* `evidence/B1/` — queue log with timestamps.

</details>

<details><summary><strong>[dropped]</strong> <s>B2 — A failing refund webhook is retried on the same schedule.</s> — refunds go through a different handler.</summary>

*Source:* finance, 2026-08-12.

*Evidence that it behaves that way:* `evidence/B2/` — not collected.

</details>

## Technical requirements

<details><summary><strong>T1 — The same webhook id delivered twice leaves one order.</strong></summary>

*Expected behaviour:* replay a stored delivery; one order, and the second attempt
is logged as a duplicate rather than silently dropped.

*Failure case:* two orders, or a second attempt that leaves no trace.

*Evidence that it behaves that way:* `evidence/T1/` — replay log plus the order
query before and after.

</details>
