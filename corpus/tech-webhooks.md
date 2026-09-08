---
title: Webhook delivery and retries
category: technical
---

# Webhook delivery and retries
Webhooks are delivered at least once. We retry a failed delivery six times with exponential
backoff over roughly 24 hours, then mark the endpoint unhealthy and email the workspace owner.

Your endpoint must answer within 5 seconds with a 2xx status. Verify the `X-Signature` header
against your signing secret and make handlers idempotent, because retries can duplicate an
event.
