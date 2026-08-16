*Example. Copy the shape, not the content. Replace what is here rather than adding to it.*

# Retry failed payment webhooks

Stripe drops a webhook roughly once a week and the order stays unpaid.

## Criteria

1. A webhook that fails with a 5xx or a timeout is retried after 1, 5 and 25
   minutes, then stops.
2. A webhook that fails with a 4xx is not retried and is recorded as rejected.
3. The same webhook id delivered twice leaves one order, whichever arrives first.
4. After the last retry fails, the order carries `payment_unconfirmed` and appears
   in the daily unpaid report.

## Out of scope

Refunds and subscription webhooks. Both go through a different handler.

## Open

One question, open-questions #1. It changes an alert, so keep building.
