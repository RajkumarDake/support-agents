---
title: Service credits for outages
category: refunds
---

# Service credits for outages

If we fail to keep the service available, Business and Enterprise customers can claim a service
credit against the affected month. This is a defined, quantified entitlement rather than a
goodwill gesture, which is why it is the route to use before asking for a discretionary refund.

## The thresholds

| Availability in a calendar month | Credit |
|---|---|
| 99.9% or above | none |
| below 99.9% | 10% of the monthly fee |
| below 99.0% | 25% of the monthly fee |
| below 95.0% | 50% of the monthly fee |

The percentages are of the monthly fee for the affected month. On an annual plan, the monthly fee
is one twelfth of the annual amount.

Starter and Pro workspaces are not covered by the service credit scheme. A prolonged outage on
those plans can still be raised under refund-policy, where exceptions are decided case by case by
a support lead.

## How to claim

1. Find the incident on the status page and note its ID, in the form `INC-NNNN`. See
   tech-service-status.
2. Contact support within **30 days of the incident**. Claims outside that window are not
   accepted.
3. Include the workspace name, the incident ID, the calendar month, and briefly how it affected
   you.
4. We confirm the availability figure for that month and apply the credit.

## What you get

The credit is applied to your **next invoice** as account credit. It is not paid out to a card,
and it is not redeemable for cash. It follows all the ordinary credit rules in
refund-downgrade-credit, including being forfeited if the workspace is closed.

A credit note is issued when the credit is applied, so your finance team has a document.

## What counts as unavailable

Availability is measured against the core service: the web application and the API returning
successful responses. Some things people expect to count do not:

- **Degraded but working.** Slow exports, delayed webhooks and stale mobile data are not
  downtime. The delayed webhook delivery in INC-2288 delivered every event once the backlog
  drained, so no availability was lost.
- **Partial regional issues.** An elevated error rate affecting a fraction of requests in one
  region, such as the upload failures in INC-2291, is counted proportionally rather than as full
  downtime.
- **Scheduled maintenance** announced in advance on the status page.
- **Problems on your side** - an identity provider outage causing ERR_1104, a webhook endpoint
  you took offline causing ERR_6002, or a rate limit you exhausted causing ERR_4029.

## Edge cases and gotchas

- Credits are per calendar month. An incident spanning midnight on the last day of a month
  affects both months' figures, and each is assessed separately.
- Only one credit applies per month; the thresholds are not cumulative.
- Claiming a service credit does not preclude a separate refund for a billing error - those are
  different processes, see billing-invoice-dispute.
- A workspace that is read-only because of a failed payment is not "unavailable" for these
  purposes.
- Enterprise contracts may define different thresholds or a different measurement window. The
  contract wins.
- Service credits do not stack with a discretionary refund for the same month.

## Troubleshooting

**Symptom: you cannot find an incident ID.**
Check the status page history for the month, see tech-service-status. If you experienced a
problem with no matching incident, tell us the date, time and what failed - if we missed it, that
matters more than the credit.

**Symptom: the 30 days have passed.**
Ask anyway with the incident ID, but expect the window to be applied. It exists so availability
figures are settled rather than reopened indefinitely.

**Symptom: told your plan is not eligible.**
Service credits are Business and Enterprise. On Starter or Pro, raise it as a refund request with
the dates and impact, see refund-how-to-request.

**Symptom: the credit did not appear on the next invoice.**
Check Billing > Credits for the balance. On annual plans it waits until the renewal.

## Related articles

- tech-service-status, refund-downgrade-credit, refund-policy.

## If this did not help

Contact support with the workspace name, the incident ID and the month. If the impact was
materially worse than the availability figure suggests - a failed launch, a missed deadline - say
so, and it goes to a support lead rather than through the standard calculation.
