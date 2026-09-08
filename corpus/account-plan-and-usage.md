---
title: Checking your plan and usage
category: account
---

# Checking your plan and usage

Settings > Plan and usage is the single screen that answers "what am I on, what have I used, and
when does it reset". Check it before raising a plan, before a large import, and whenever a limit
error appears.

## What the screen shows

- The current plan and the renewal date.
- Seats used against seats included.
- API calls made this period against the period allowance.
- Storage consumed against the storage limit.
- Any account credit waiting to be applied.

Everything except storage is counted per billing period and resets at the start of the next one.
Storage is a standing total: it goes down only when you delete things.

## Limits by plan

| | Starter | Pro | Business | Enterprise |
|---|---|---|---|---|
| Members | 3 | 25 | unlimited | unlimited |
| Free Viewers | no | no | yes | yes |
| Workspace storage | 10 GB | 250 GB | 1 TB | custom, typically 5 TB |
| Per-file upload | 100 MB | 2 GB | 2 GB | 10 GB |
| API calls per period | 60,000 | 600,000 | 2,000,000 | 20,000,000 or contract |
| API requests per minute | 60 | 600 | 600 | negotiated |
| SSO and SAML | no | no | yes | yes |
| Audit log export | no | no | yes | yes |
| Price | $29/month | $49/seat/month | $90/seat/month | contract |

## What happens as you approach a limit

At 80% of any limit we email the Owner. At 100% the affected feature is soft-capped rather than
cut off: existing data stays readable and the rest of the product keeps working, but the specific
thing you exhausted stops accepting new work.

- API calls at 100%: further calls return HTTP 429 with ERR_4029 until the period rolls over or
  the plan is raised. See tech-api-rate-limits.
- Storage at 100%: new uploads and new attachments are rejected with ERR_5140. See
  tech-storage-quota.
- Seats at 100%: new invitations fail with ERR_2044. See account-add-team-member.

Note that the per-minute rate limit and the per-period API allowance are different things, and
both return ERR_4029. A tight loop can trip the per-minute limit on day one of a period with the
allowance almost untouched.

## Raising or lowering the plan

Upgrade from Settings > Plan > Change plan. Upgrades take effect immediately and are prorated -
billing-proration explains the arithmetic and where the line item appears. Downgrades take effect
at the end of the current period and issue credit rather than a refund; see
account-downgrade-plan before you commit, because some features stop working at the moment the
downgrade lands.

## Edge cases and gotchas

- Usage figures update within a few minutes, not instantly. Do not judge a burst of API traffic
  by this screen in real time; use the response headers described in tech-api-rate-limits.
- Deleted files still count toward storage until the trash is emptied.
- Only Owners and Admins see this screen. Members and Viewers get ERR_2031.
- Changing plan mid-period does not reset the usage counters. The period boundary does.
- Seats used counts accepted members only. Pending invitations are not counted.

## Troubleshooting

**Symptom: seats used is higher than the number of people you recognise.**
Deactivated members still hold a seat. Check Settings > Team for rows marked Deactivated and
remove the ones who are not coming back - see account-remove-member.

**Symptom: storage is near the limit but you deleted a lot of files.**
Empty the trash. Until then the space is still allocated.

**Symptom: API calls jumped without a code change.**
A webhook retry storm or a polling integration is the usual cause. Check Settings >
Integrations > Webhooks for an endpoint marked unhealthy, see tech-webhooks.

**Symptom: the renewal date on this screen does not match the invoice date.**
Invoices are dated when the charge is captured, which can be a few hours after the renewal
boundary in your time zone. billing-cycle covers this.

## Related error codes

- ERR_4029 - rate limit or period allowance exhausted.
- ERR_5140 - storage quota exhausted.
- ERR_2044 - seat limit reached.
- ERR_2031 - your role cannot view plan and usage.

## Related articles

- billing-proration, account-downgrade-plan, tech-storage-quota.

## If this did not help

Send support the workspace name and a screenshot of Settings > Plan and usage, plus the limit you
believe is wrong. We can see the raw counters and the exact time each one last reset.
