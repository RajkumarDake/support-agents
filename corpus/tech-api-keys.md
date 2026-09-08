---
title: API keys and authentication
category: technical
---

# API keys and authentication

The API authenticates with a bearer token. There are two kinds - personal and workspace - and
choosing the wrong one is the most common reason a working integration dies overnight.

## Personal versus workspace tokens

| | Personal token | Workspace token |
|---|---|---|
| Created under | Settings > API > Personal tokens | Settings > API > Workspace tokens |
| Who can create | any Member or above | Owner and Admin |
| Permissions | inherits the creator's role | scoped explicitly at creation |
| Survives the creator leaving | no, revoked immediately | yes |
| Survives Sign out everywhere | no | yes |
| Best for | scripts you run yourself | anything in production |

**Use a workspace token for anything that must keep running.** A personal token is revoked the
moment its owner is removed from the workspace, and also when they use Sign out everywhere - see
account-remove-member and account-session-timeout.

## Creating a token

1. Open Settings > API.
2. Click New token and choose Personal or Workspace.
3. Name it after what it does. The name appears as the actor in the audit log, so
   `nightly-sync` is far more useful than `token 3`.
4. For a workspace token, select the scopes: `read`, `write`, `admin`. Grant the least you need.
5. Optionally set an expiry - 30, 90 or 365 days, or never.
6. Copy the token. It is shown **once**. If you lose it, revoke it and create another.

## Using it

Send it as a bearer token on every request:

```
Authorization: Bearer <token>
```

Responses carry `X-Request-Id`, which is the single most useful thing to quote to support, and
the rate limit headers described in tech-api-rate-limits.

## Revoking and rotating

Revoke from Settings > API with the Revoke button. Revocation is immediate - in-flight requests
complete, the next one returns 401.

Rotate on a schedule: create the new token, deploy it, confirm traffic has moved, then revoke the
old one. Doing it in the other order causes an outage. Tokens with an expiry send a reminder to
the creator seven days before they lapse.

## Permissions and plans

A token can never do more than the role behind it. A personal token created by a Member cannot
read invoices, and returns ERR_2031 if it tries - invoices and team management are Owner and
Admin only, see account-roles-permissions.

Rate limits are per workspace, not per token: 60 requests per minute on Starter, 600 on Pro and
Business, negotiated on Enterprise. Adding tokens does not add capacity.

## Edge cases and gotchas

- Lowering someone's role immediately narrows what their existing personal tokens can do. It does
  not revoke them.
- Tokens are not affected by two-factor authentication. 2FA gates interactive sign-in only - see
  account-two-factor.
- A workspace in read-only mode after an unpaid invoice allows token reads and rejects writes -
  see billing-payment-failed.
- A suspended workspace, following a chargeback, returns 403 to every token. See
  billing-dispute-chargeback.
- Token creation and revocation are written to the audit log, see account-audit-logs.
- Tokens are workspace-scoped. A token from one workspace never works against another.
- Never put a token in a client-side application. There is no browser-safe token type; use your
  own backend.

## Troubleshooting

**Symptom: 401 on every request, suddenly.**
The token was revoked. Common causes: the person who created it left the workspace, they used
Sign out everywhere, or the token expired. Create a workspace token instead.

**Symptom: 403 with ERR_2031.**
The role or the scope is insufficient. Check the token's scopes and the creator's role.

**Symptom: 403 on everything including reads.**
The workspace is suspended. Check billing.

**Symptom: 429 with ERR_4029.**
Rate limit or period allowance, not authentication. See tech-api-rate-limits.

**Symptom: the token works in curl and not in your application.**
Almost always a missing `Bearer ` prefix, or a trailing newline picked up from a file.

**Symptom: you lost the token value.**
There is no way to display it again. Revoke and create a new one.

## Related error codes

- ERR_2031 - the token's role or scope is insufficient.
- ERR_4029 - rate limited.

## Related articles

- tech-api-rate-limits, tech-webhooks, tech-webhook-signatures.

## If this did not help

Contact support with the workspace name, the token name (never the token itself), and an
`X-Request-Id` from a failing response. We can see why a specific request was rejected without
you sending us any credentials.
