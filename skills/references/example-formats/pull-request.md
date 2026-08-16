*Example. Copy the shape, not the content. The first sentence is what a reviewer
reads if they read nothing else.*

# Retry failed payment webhooks

A dropped Stripe webhook left the order unpaid with nothing to show for it; failed
deliveries are now retried three times and, if they still fail, land in the daily
unpaid report.

## What changed

- `WebhookQueue` retries 5xx and timeouts after 1, 5 and 25 minutes. 4xx is
  rejected on the first attempt — see decisions.md, we do not want to hide our own
  validation bugs.
- Delivery is keyed on Stripe's `event.id`, so a redelivery cannot create a second
  order.
- Orders that exhaust the retries get `payment_unconfirmed` and appear in the
  09:00 report finance already reads.

## How I know it works

- `test_webhook_retry.py` covers the three attempts, the 4xx path and the double
  delivery. The retry test fails if the backoff is set to zero, which is how I
  checked it can fail at all.
- Replayed 14 real dropped webhooks from last month on staging: 14 orders paid,
  no duplicates. Log: `staging-replay-2026-08-14.txt`.
- Not checked: behaviour when the queue itself is down. Same as before this change.

## Open

open-questions #1, with Marco. It changes an alert route, not this code.
