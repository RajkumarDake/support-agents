---
title: Service status and incident policy
category: technical
---

# Service status and incident policy

When something is broken, the status page is the fastest way to find out whether it is us. It
lists current incidents, their status, and the history for the last 12 months. Every incident has
an ID in the form `INC-NNNN`, which is what you quote when claiming a service credit.

## Reading the status page

Incidents move through four statuses:

| Status | Meaning |
|---|---|
| investigating | We know something is wrong and are working out what |
| identified | We know the cause and are fixing it |
| monitoring | The fix is deployed and we are watching it hold |
| resolved | Closed, with a final summary |

Each entry names the affected components, the error codes it produces, a summary, and a workaround
where one exists. Subscribe to updates from the status page itself so you hear about an incident
before your team reports it to you.

## Current and recent incidents

**INC-2291 - Elevated upload failures in eu-west-1.** Status monitoring, started 2026-09-07. A
storage node in eu-west-1 is returning intermittent rejections on uploads over 50 MB. Roughly 3%
of uploads in that region are affected and produce ERR_5012. Retrying usually succeeds. Files
under 50 MB are unaffected. Workaround: retry the upload from a fresh page load. See
tech-err-5012-upload.

**INC-2274 - Mobile app stale data on Android 15.** Status investigating, started 2026-09-05.
Background refresh is being suspended aggressively by the OS on some Android 15 devices, leaving
the app showing data up to a day old. Workaround: pull to refresh, or sign out and back in to
force a full resync. See tech-mobile-sync.

**INC-2288 - Delayed webhook delivery.** Status resolved, started 2026-09-04, resolved the same
day at 11:20 UTC. A backlog in the delivery queue delayed webhooks by up to 40 minutes. No events
were lost; all were delivered after the backlog drained. See tech-webhooks.

**INC-2285 - Duplicate charge batch on 2026-09-02.** Status resolved, started 2026-09-02. A retry
in the payment processor captured a small batch of monthly invoices twice. Affected customers have
two identical `paid` invoices dated 2026-09-02. Refunds are issued on request and case by case by
the billing team. Workaround: contact support with both invoice IDs and the duplicate is refunded
in full. See billing-duplicate-charge and refund-duplicate-charge.

**INC-2279 - SSO sign-in failures for Okta tenants.** Status resolved, started 2026-08-29. A
certificate rotation on our side invalidated cached IdP metadata for some Okta tenants, producing
ERR_1104 on sign-in. Workaround: re-upload the metadata XML under Settings > Security > SSO. See
tech-sso-saml.

## Is it us or is it you?

Before assuming an incident, check the error code. Several codes are almost always local
configuration rather than a service problem:

- **ERR_1104** - your identity provider's clock or attributes, unless an SSO incident is open.
- **ERR_6002** - your webhook endpoint failing or rejecting valid signatures, see
  tech-webhook-signatures.
- **ERR_6015** - a token revoked on the third-party side, see tech-integrations-troubleshooting.
- **ERR_4029** - your own request rate or a spent allowance, see tech-api-rate-limits.
- **ERR_2031** and **ERR_2044** - roles and seats, never an incident.

A problem affecting exactly one person is essentially never an incident. A problem that started for
everyone at the same minute usually is.

## Incident policy

- We open a public incident when a problem affects more than a small fraction of requests, or any
  amount of a critical path such as sign-in or billing.
- We post an initial note within 30 minutes of confirming, and update at least hourly while the
  status is investigating or identified.
- We publish a summary when an incident resolves, and a fuller write-up for anything that lasted
  over an hour or lost data.
- Scheduled maintenance is announced in advance on the status page and does not count against
  availability.

## Service credits

If a calendar month falls below 99.9% availability, Business and Enterprise customers can request
a service credit: 10% of the monthly fee under 99.9%, 25% under 99.0%, 50% under 95.0%. Requests
must be made **within 30 days** of the incident and must reference the incident ID. Credits are
applied to the next invoice. Full detail in refund-outage-credit.

Degraded-but-working conditions - delayed webhooks, slow exports, stale mobile data - are not
counted as downtime.

## Related articles

- refund-outage-credit, tech-error-codes-overview, tech-err-5012-upload.

## If this did not help

If you are seeing a problem with no matching incident, tell support the time, the error code and
what failed. An unreported incident matters more to us than an individual ticket, so those
messages are read quickly.
