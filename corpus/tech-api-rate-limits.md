---
title: API rate limits
category: technical
---

# API rate limits

Two separate limits govern API use: how many requests you may make per minute, and how many calls
your plan includes per billing period. Both return HTTP 429 with ERR_4029, which is why people
often fix the wrong one. Read the headers to tell them apart.

## The limits

| Plan | Requests per minute | Calls per billing period |
|---|---|---|
| Starter | 60 | 60,000 |
| Pro | 600 | 600,000 |
| Business | 600 | 2,000,000 |
| Enterprise | negotiated | 20,000,000 or contract |

The per-minute limit is a throughput cap and resets continuously. The per-period allowance resets
at the start of each billing period, at the same moment the renewal charge is raised - see
billing-cycle. Storage does not work this way; it is a standing total, see tech-storage-quota.

## Burst smoothing

Bursts are smoothed over a **10 second window**. The practical effect is that a tight loop trips
the limit even when your per-minute average is well under it: 60 requests fired in two seconds on
Starter exceeds the smoothed rate, and the 61st through 600th fail, even though you made only 60
requests that minute.

Spread requests evenly rather than firing them in a batch. A 100 ms delay between calls on
Starter, or 10 ms on Pro and Business, keeps you comfortably inside.

## Response headers

Every API response carries:

- `X-RateLimit-Limit` - your per-minute limit.
- `X-RateLimit-Remaining` - requests left in the current window.
- `X-RateLimit-Reset` - seconds until the window resets.
- `X-Quota-Remaining` - calls left in the billing period.
- `Retry-After` - on a 429 only, seconds to wait.

If `X-RateLimit-Remaining` is 0 you hit the per-minute limit and it clears in seconds. If
`X-Quota-Remaining` is 0 you have spent the period's allowance and it clears at the renewal date,
or when you raise the plan.

## Handling 429 properly

1. **Honour `Retry-After`** instead of retrying immediately. Retrying at once makes it worse and,
   with enough clients, keeps you permanently limited.
2. **Add exponential backoff with jitter.** Doubling the delay each attempt, with a random
   component, stops a fleet of workers retrying in lockstep.
3. **Batch reads where the API supports it.** One request for 100 records beats 100 requests.
4. **Cache** anything that does not change every minute.
5. **Raise the plan** if sustained throughput is genuinely needed rather than engineering around a
   limit that is simply too low.

## Edge cases and gotchas

- Limits are per workspace, not per token. Ten tokens share one budget, so a new integration can
  starve an existing one.
- Integration traffic counts. A chatty Jira or Slack sync consumes the same allowance as your own
  code, see onboarding-integrations.
- Webhook deliveries we send to you do not count against your limit. Your responses to them are
  not API calls.
- Hitting 100% of the period allowance soft-caps the API only. The web application keeps working
  normally, see account-plan-and-usage.
- A downgrade drops both limits at the moment it lands, which can break a working integration -
  see account-downgrade-plan.
- 429 responses themselves do not consume period allowance.

## Troubleshooting

**Symptom: ERR_4029 immediately at the start of a job.**
Burst smoothing. Your loop is too tight regardless of the per-minute average. Add a delay.

**Symptom: ERR_4029 that does not clear after a minute.**
The period allowance is spent, not the rate limit. Check `X-Quota-Remaining` and
Settings > Plan and usage. It clears at the renewal date.

**Symptom: ERR_4029 with no code change on your side.**
Something else is consuming the budget - a new integration, a webhook retry storm, or a colleague's
script. Check Settings > Integrations and the audit log for new tokens, see tech-api-keys.

**Symptom: limits look lower than the table.**
Confirm the plan under Settings > Plan and usage. Check that a scheduled downgrade has not landed.

**Symptom: 429 with `Retry-After: 0`.**
Retry once immediately, then back off. That value means the window is about to roll.

**Symptom: 401 rather than 429.**
That is the token, not the limit. See tech-api-keys.

## Related error codes

- ERR_4029 - rate limit exceeded or period allowance exhausted.

## Related articles

- tech-api-keys, account-plan-and-usage, tech-webhooks, onboarding-integrations,
  account-downgrade-plan, billing-cycle.

## If this did not help

Contact support with the workspace name, a request ID from `X-Request-Id` on a 429 response, and
the timestamp. If you need a higher limit, tell us your target sustained rate and why - Enterprise
limits are negotiated rather than fixed.
