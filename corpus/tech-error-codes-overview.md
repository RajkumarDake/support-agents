---
title: Reading our error codes
category: technical
---

# Reading our error codes

Every error surfaced in the product carries a code of the form `ERR_NNNN`. The code is stable,
searchable, and far more useful than the message next to it. Quote the full code and the
timestamp whenever you contact support.

## The families

The first digit tells you which subsystem raised it:

| Prefix | Family | Typical cause |
|---|---|---|
| 1xxx | authentication | sign-in, SSO, password reset |
| 2xxx | permissions | your role, or a plan limit on people |
| 3xxx | validation | something you submitted was malformed |
| 4xxx | rate limiting | too many requests, or a period allowance |
| 5xxx | storage and uploads | files, exports, quota |
| 6xxx | integrations and webhooks | third-party connections |

Knowing the family usually tells you whose problem it is. 1xxx and 6xxx are frequently
configuration on your side or your identity provider's; 2xxx is a role or a plan; 5xxx is a file
or a limit.

## The full list

**Authentication**
- `ERR_1077` - reset link expired. Valid for one hour, single use. See
  account-password-reset.
- `ERR_1104` - SSO assertion rejected. Missing `email` attribute, or clock skew over five
  minutes. See tech-sso-saml.

**Permissions**
- `ERR_2031` - insufficient permissions. Invoices and team management are Owner and Admin only.
  See account-roles-permissions.
- `ERR_2044` - seat limit reached. Every seat in the plan is in use. See
  account-add-team-member.

**Validation**
- `ERR_3007` - import validation failed, with a row number. Nothing was written. See
  onboarding-import-data.
- `ERR_3112` - payment method rejected. Declined, or an unsupported card type. See
  billing-payment-failed.

**Rate limiting**
- `ERR_4029` - rate limit exceeded, or the period allowance is spent. Honour `Retry-After`. See
  tech-api-rate-limits.

**Storage**
- `ERR_5012` - upload rejected: size, type, or an expired 15-minute upload token. See
  tech-err-5012-upload.
- `ERR_5108` - export archive exceeded the 10 GB per-job limit. See tech-export-slow.
- `ERR_5140` - storage quota exhausted. See tech-storage-quota.

**Integrations**
- `ERR_6002` - webhook endpoint unhealthy after six consecutive failures. See tech-webhooks.
- `ERR_6015` - integration token revoked upstream. See onboarding-integrations.

## Severity

Codes carry an internal severity that shapes how support triages them. `ERR_1104` and `ERR_5140`
are high - they stop people working. `ERR_4029`, `ERR_5012`, `ERR_5108`, `ERR_6002` and
`ERR_6015` are medium. `ERR_2031`, `ERR_2044`, `ERR_3007` and `ERR_1077` are low, because they
almost always have an immediate self-serve fix. `ERR_3112` is high because it leads to a workspace
going read-only if left.

## Where codes are recorded

Every error raised by an administrative action is written to the audit log with the actor, the
timestamp and the source IP. Owners and Admins on Business and Enterprise can read and export it -
see account-audit-logs. This is why we ask for a timestamp: with a code and a time we can find the
exact event rather than guessing.

API responses carry the code in the body and in the `X-Error-Code` header, alongside a request ID
in `X-Request-Id`. Include the request ID if you have it; it is the single most useful thing you
can send.

## Edge cases and gotchas

- The same code can have several causes - ERR_5012 has three. Read the article before concluding
  which one applies.
- A code that appears during a known incident may have nothing to do with your configuration.
  Check tech-service-status first when an error is new and intermittent.
- Codes are stable across releases. If you have written alerting against them, it will not break.
- Errors without a code are unexpected and worth reporting as-is; they mean something got past our
  handling.

## Troubleshooting

**Symptom: an error with no code at all.**
Send us a screenshot and the time. That is a gap in our handling, not something you can fix.

**Symptom: a code not on this list.**
Send it. The list above is the complete published set, so an unlisted code means either a typo or
something new.

**Symptom: the same code from two different actions.**
Normal. The family is the subsystem, not the action.

## Related articles

- tech-service-status, account-audit-logs, tech-api-rate-limits.

## If this did not help

Contact support with the full code, the timestamp including the time zone, the workspace name,
and the request ID if it came from the API. That set resolves most technical tickets in one
exchange.
