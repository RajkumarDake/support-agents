---
title: Fixing a broken integration
category: technical
---

# Fixing a broken integration

An integration that worked and then stopped has a short list of causes, and the error code tells
you which one applies. This article is the diagnosis path. For connecting an integration in the
first place, see onboarding-integrations.

## Start with the error code

| Code | Meaning | Where the fix is |
|---|---|---|
| ERR_6015 | Integration token revoked upstream | The other service |
| ERR_6002 | Webhook endpoint unhealthy | Your endpoint |
| ERR_4029 | Rate limit or allowance exhausted | Your request pattern or your plan |
| ERR_2031 | Insufficient permissions | Your role here |

Settings > Integrations shows the current state of each connection, and the last error with its
timestamp.

## ERR_6015: token revoked upstream

The OAuth token for the integration was revoked on the other side, usually because the account
that granted it lost access there - somebody left, their licence was removed, or an administrator
revoked third-party apps.

Fix:

1. Open Settings > Integrations.
2. Click Reconnect on the affected integration.
3. Complete the OAuth flow **with an account that will stay active** - a service account or a
   long-lived admin account, not whoever happens to be at the keyboard.
4. Confirm the scopes are granted in full. A reduced grant completes the flow and then fails
   silently on the first real call.

This is the most common integration failure we see, and re-granting with a personal account simply
schedules the same outage for whenever that person leaves.

## ERR_6002: webhook endpoint unhealthy

Six consecutive delivery attempts failed over roughly 24 hours, so the endpoint was marked
unhealthy and delivery was paused. Confirm the endpoint returns 2xx within 5 seconds, confirm your
signature verification is not rejecting valid events, then re-enable and replay. Full detail in
tech-webhooks and tech-webhook-signatures.

## ERR_4029: rate limits

Integration traffic counts against your workspace API allowance. A chatty sync on Starter, where
the limit is 60 requests per minute and 60,000 calls per period, can exhaust it and take your own
scripts down with it. Limits are per workspace, not per token. See tech-api-rate-limits and
account-plan-and-usage.

## Silent failures with no error at all

- **Nothing is subscribed.** A webhook endpoint with no events selected is silent by design.
- **The workspace is read-only** after an unpaid invoice, so no events are generated. See
  billing-payment-failed.
- **The integration is connected but not configured** - no Slack channel chosen, no Jira project
  mapped.
- **Scopes were reduced during approval**, so we can authenticate but not do the work. Disconnect
  and reconnect.
- **The other service changed something** - a renamed channel, an archived repository, a deleted
  Jira project.

## Edge cases and gotchas

- Integrations are owned by the workspace and survive the connector leaving the team - see
  onboarding-integrations and account-remove-member. What does not survive is the upstream account
  losing access.
- Reconnecting does not replay anything missed. Use webhook replay for events, which covers the
  last 7 days.
- Disconnecting and reconnecting resets configuration. Note your channel and project mappings
  first.
- Connection and disconnection are written to the audit log, so you can see exactly when an
  integration was last touched and by whom - see account-audit-logs.
- A plan downgrade does not disconnect integrations, but can starve them of API allowance.
- Duplicate posts usually mean the workspace is connected twice, not that we sent twice.

## Troubleshooting

**Symptom: worked for months, stopped overnight, ERR_6015.**
Someone was deprovisioned on the other side. Reconnect with a service account.

**Symptom: events stopped, endpoint shows unhealthy.**
ERR_6002. Fix the endpoint, re-enable, replay.

**Symptom: intermittent gaps, no errors.**
Check whether an incident explains the window - INC-2288 delayed webhook delivery by up to 40
minutes on 2026-09-04, for example. See tech-service-status.

**Symptom: ERR_2031 on the Integrations screen.**
You are a Member or Viewer. Integrations are Owner and Admin only.

**Symptom: the OAuth flow completes and nothing works.**
Reduced scopes. Disconnect, reconnect, approve everything requested.

**Symptom: one integration is fine and another is not.**
Then it is not a network or account-wide problem. Read that integration's last error on the
Integrations screen.

## Related error codes

- ERR_6015 - integration token revoked upstream.
- ERR_6002 - webhook endpoint unhealthy.
- ERR_4029 - rate limit or period allowance exhausted.
- ERR_2031 - insufficient permissions.

## Related articles

- onboarding-integrations, tech-webhooks, tech-webhook-signatures, tech-api-rate-limits,
  tech-api-keys, tech-service-status.

## If this did not help

Contact support with the workspace name, which integration, the error code, and the last time it
worked. If the token was revoked on the other side, the fix is over there and we will tell you
precisely what to ask their administrator to restore.
