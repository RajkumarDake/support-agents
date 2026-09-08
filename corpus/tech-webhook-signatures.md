---
title: Verifying webhook signatures
category: technical
---

# Verifying webhook signatures

Every webhook we send carries a signature so you can prove it came from us and was not modified.
Verification is not optional in any sensible deployment: without it, anyone who learns your
endpoint URL can post whatever they like to it. This article covers the headers, the algorithm,
and the handful of mistakes that cause almost every verification failure.

## The headers

| Header | Contents |
|---|---|
| `X-Signature` | Hex-encoded HMAC-SHA256 of the request body |
| `X-Signature-Timestamp` | Unix seconds at the moment we signed |
| `X-Event-Id` | Unique event ID, use this to deduplicate |
| `X-Request-Id` | Delivery attempt ID, quote this to support |

## The signing secret

The secret is shown **once**, when you create the endpoint under Settings > Integrations >
Webhooks. Copy it then. If you lose it, rotate it from the endpoint's page - rotation issues a new
secret and the old one stops working immediately, so deploy the new one first if you can tolerate
a brief window, or accept a few failed deliveries that will be retried.

Store it as a secret, not in your repository. It is equivalent to a password for your endpoint.

## Verifying

1. Take the **raw request body exactly as received**. Do not parse it and re-serialise it.
2. Concatenate the timestamp, a dot, and the raw body: `{timestamp}.{body}`.
3. Compute HMAC-SHA256 over that string using the signing secret.
4. Hex-encode the result.
5. Compare against `X-Signature` using a **constant-time comparison**, not `==`.
6. Reject anything where `X-Signature-Timestamp` is more than five minutes old, to prevent replay.

## The four mistakes that cause every failure

1. **Re-serialising the body.** Most frameworks give you a parsed object. `JSON.stringify` of that
   object is not byte-identical to what we sent - key order, whitespace and unicode escaping all
   differ. Capture the raw body before any middleware parses it.
2. **Signing the body without the timestamp prefix.** The signed string is
   `{timestamp}.{body}`, not the body alone.
3. **Comparing with `==`.** It works, but it leaks timing information. Use your language's
   constant-time compare.
4. **Clock skew.** If your server's clock is more than five minutes off, every event looks like a
   replay. Sync with NTP. This is the same class of problem that causes ERR_1104 on SAML
   sign-in - see tech-sso-saml.

## Why this matters for ERR_6002

If your verification is broken you will reject valid events, return a non-2xx status, and after
six consecutive failures over roughly 24 hours the endpoint is marked unhealthy with ERR_6002 and
delivery is paused. From the outside this looks like an outage on our side. Before reporting one,
confirm your verification accepts our test event - Settings > Integrations > Webhooks > Send test
event. See tech-webhooks.

## Edge cases and gotchas

- The test event is signed identically to a real one, so it is a valid check of your verification
  code.
- Retries are re-signed with a new timestamp, so an event you rejected for staleness will arrive
  again with a fresh one.
- Body compression is not applied; you always receive the raw JSON.
- A load balancer or proxy that rewrites the body will break verification. Check for anything that
  normalises JSON in the path.
- Rotating the secret is written to the audit log, see account-audit-logs.
- The same signing scheme is used by Enterprise audit streaming, see account-audit-logs.

## Troubleshooting

**Symptom: every signature fails.**
The raw body. In Express use `express.raw`, in Flask use `request.get_data()`, in Rails use
`request.raw_post`. Verify before any JSON parsing.

**Symptom: signatures pass locally and fail in production.**
A proxy or WAF in front of the application is modifying the body, or the secret in the production
environment is stale after a rotation.

**Symptom: intermittent failures only on some events.**
Unicode. Re-serialisation differences show up only on payloads containing non-ASCII characters,
which is a strong hint that mistake 1 is the cause.

**Symptom: everything rejected as a replay.**
Server clock. Check NTP.

**Symptom: verification passes but the endpoint is still unhealthy.**
Something after verification is failing or exceeding the 5 second response budget. Acknowledge
first, process asynchronously.

## Related error codes

- ERR_6002 - endpoint marked unhealthy, frequently caused by broken verification.

## Related articles

- tech-webhooks, tech-api-keys, tech-integrations-troubleshooting, tech-sso-saml,
  account-audit-logs.

## If this did not help

Contact support with the endpoint URL and an `X-Request-Id` from a delivery that failed
verification. We can tell you the exact bytes we signed, which settles the raw-body question
immediately.
