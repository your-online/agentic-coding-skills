*Example. Copy the shape, not the content. Each question says who decides and what
is blocked, so the reader can answer without reading the rest.*

# Open questions — payment webhooks

## 1. Does a webhook that never succeeds page someone at night?

**Marco decides.** Blocks nothing; the alert route is the last change.
What I found: no other failure in this service pages out of hours, and finance
reads the unpaid report at 09:00. So the cheap answer is no.

## 2. Should a rejected 4xx webhook be retried after a deploy?

**Anne decides.** Blocks criterion 2.
Two of the last three 4xx failures were our own validation bug, so a redelivery
would have worked. Retrying everything hides those bugs; retrying nothing means
manual replay. I have no view on which we want.

## 3. Which environment replays the stored webhooks?

**Answered — staging, 2026-08-14, Anne.** Production replay needs a key we do not
issue to jobs.
