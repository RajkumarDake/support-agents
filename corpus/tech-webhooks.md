---
title: Webhook delivery and retries
category: technical
---

# Webhook delivery and retries

Webhooks push events to your endpoint as they happen, so you do not have to poll. This article
covers setting one up, the delivery guarantees, the retry schedule, and what to do when an
endpoint is marked unhealthy. Signature verification has its own article,
tech-webhook-signatures.

## Setting one up

1. Open Settings > Integrations > Webhooks. Owner and Admin only.
2. Click Add endpoint.
3. Enter the URL. It must be HTTPS; plain HTTP is refused at save time.
4. Select the events to subscribe to. Subscribing to everything and filtering on your side works,
   but wastes your rate budget and ours.
5. Save. We show the signing secret **once** - copy it now, see tech-webhook-signatures.
6. Click Send test event and confirm your endpoint returns 2xx.

## Delivery guarantees

Webhooks are delivered **at least once**. That is a deliberate choice: we would rather send an
event twice than lose it. The consequence is that your handler must be idempotent - key on the
event ID we send and ignore an ID you have already processed.

Order is not guaranteed either. Two events generated a second apart can arrive in either order,
particularly after a retry. Use the timestamp in the payload rather than arrival order.

## Requirements for your endpoint

- Answer within **5 seconds** with a 2xx status.
- Do the work asynchronously. Acknowledge first, process afterwards; a handler that does real work
  inline will eventually exceed 5 seconds under load.
- Accept POST with a JSON body.
- Do not require authentication we cannot provide. Verify our signature instead of putting the
  endpoint behind a login.

## The retry schedule

A failed delivery is retried **six times with exponential backoff over roughly 24 hours**. A
failure is any non-2xx response, a timeout, or a connection error.

After six consecutive failures the endpoint is marked **unhealthy**, delivery is paused, and we
email the workspace Owner. That state raises ERR_6002.

To recover:

1. Fix the endpoint and confirm it returns 2xx within 5 seconds.
2. Check that signature verification is not rejecting valid events - a bug there looks exactly
   like an outage.
3. Re-enable the endpoint under Settings > Integrations > Webhooks.
4. Replay the missed events from the same screen. Replay covers the last 7 days.

## Known incident: delayed delivery

A backlog in the delivery queue delayed webhooks by up to 40 minutes on 2026-09-04. This is
incident INC-2288, resolved the same day at 11:20 UTC. No events were lost; all were delivered
once the backlog drained. If you are diagnosing a gap around that date, that is the explanation
and no action is needed. See tech-service-status.

## Edge cases and gotchas

- Deliveries we send do not count against your API rate limit. Your own calls do, see
  tech-api-rate-limits.
- An endpoint that returns 200 with an error body is a success as far as we are concerned. Return
  a non-2xx status when you genuinely could not accept the event.
- Redirects are not followed. Point the endpoint at the final URL.
- Self-signed certificates are rejected. Use a certificate from a public authority.
- A workspace in read-only mode after an unpaid invoice stops generating events, so endpoints go
  quiet without going unhealthy, see billing-payment-failed.
- Endpoint changes are written to the audit log, see account-audit-logs.
- Enterprise audit streaming uses the same delivery, retry and signature rules, see
  account-audit-logs.

## Troubleshooting

**Symptom: ERR_6002 "webhook endpoint unhealthy".**
Six consecutive failures over roughly 24 hours. Fix the endpoint, re-enable it, replay the missed
events.

**Symptom: intermittent failures under load.**
Your handler is exceeding 5 seconds. Acknowledge immediately and queue the work.

**Symptom: duplicate events.**
Expected - delivery is at least once. Deduplicate on the event ID.

**Symptom: events arrive out of order.**
Also expected. Sort by the payload timestamp.

**Symptom: no events at all, no errors.**
Check the subscription list; an endpoint subscribed to no events is silent. Then check whether the
integration behind them lost its token with ERR_6015, see tech-integrations-troubleshooting.

**Symptom: signature verification fails on every event.**
See tech-webhook-signatures - this is almost always the raw body being re-serialised before
verification.

## Related error codes

- ERR_6002 - endpoint marked unhealthy after six consecutive failures.
- ERR_6015 - the integration's upstream token was revoked.

## Related articles

- tech-webhook-signatures, tech-integrations-troubleshooting, tech-api-keys,
  tech-api-rate-limits, onboarding-integrations, tech-service-status.

## If this did not help

Contact support with the workspace name, the endpoint URL, and the timestamp of a delivery you
expected. We keep delivery attempts with their response codes for 7 days and can tell you exactly
what your endpoint returned.
