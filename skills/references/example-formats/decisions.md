*Example. Copy the shape, not the content. One entry per decision, newest last;
undecided items go in open-questions.md, not here.*

# Decisions — payment webhooks

## Retries live in the queue, not in the handler

2026-08-14 · decided with Anne (payments) · replaces the in-handler `sleep` in the
first draft.

The handler must answer Stripe within 10 seconds, so it cannot wait between
attempts. The queue already has backoff and a dead-letter path.

Costs us: a failed webhook is now visible in two places, the queue and the order.

## Webhook id is the idempotency key

2026-08-14 · confirmed by Stripe docs, `event.id` is stable across redeliveries.

Was going to be order id plus amount, which collapses two legitimate payments for
the same amount on the same order.
