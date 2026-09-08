---
title: Credits from downgrades
category: refunds
---

# Credits from downgrades

Downgrading a plan, removing a seat, or converting someone to a free Viewer produces **account
credit**, not money back. This is the single most common expectation mismatch in billing, so it
is worth being precise about what credit is and how it behaves.

## What credit is

Credit is a balance held against your workspace that is applied automatically to the next invoice
before the card is charged. It is visible under Billing > Credits, which shows the balance, where
each amount came from, and when it was added.

On the invoice it appears as a negative line, which is why a bill after a downgrade can be small
or zero rather than simply lower. See billing-invoice-access.

## What produces credit

| Event | Result |
|---|---|
| Downgrading a plan | Credit for the difference, at the end of the period |
| Removing a member mid-period | Credit for the unused days, on the next invoice |
| Converting a Member to a free Viewer on Business | Credit for the unused days |
| A service credit for an outage | Credit, see refund-outage-credit |
| An upheld invoice dispute about timing | Credit, see billing-invoice-dispute |

What does not produce credit: duplicate charges and charges after cancellation, which are
refunded as money - see refund-duplicate-charge and refund-cancellation.

## The rules

- Credit is applied automatically. There is nothing to redeem and no code to enter.
- Credit **cannot be transferred between workspaces**, even workspaces you own and pay for on the
  same card.
- Credit is **not redeemable for cash**. We will not convert it to a refund on request.
- If a workspace is closed with credit remaining, the credit is **forfeited**. Spend it before
  deleting - see account-close-workspace.
- Credit does not expire while the workspace is active.
- Credit survives cancellation and is applied if you resubscribe later, see refund-cancellation.
- Tax is calculated after credit is applied, so a large credit reduces the tax too - see
  billing-tax-vat.

## Why downgrades are credit and upgrades are cash

Upgrades take effect immediately, so you receive the value immediately and pay for it prorated.
Downgrades take effect at the end of the period, so you keep the higher plan's features until
then and there is nothing to give back - the credit represents value you did not consume after
the boundary. billing-proration sets out the arithmetic; account-downgrade-plan lists what stops
working on the day.

## Worked example

A Business workspace at $90 per seat with 20 seats downgrades to Pro at $49 per seat with the same
20 seats, effective at the period end. The next period is billed at Pro rates. If two people were
also removed 10 days before the boundary, a credit of $90 x 2 x 10/30 = $60 appears and is applied
against that Pro invoice.

## Edge cases and gotchas

- On annual plans, credit sits in Billing > Credits until the anniversary renewal, which can be
  months away. It is not lost, just idle.
- Credit is not shown on Settings > Plan and usage in older sessions; reload if the balance looks
  stale.
- A credit balance larger than the next invoice carries forward. It is never paid out.
- Removing someone on the last day of a period can produce a credit that rounds to zero.
- Credit does not prevent a workspace going read-only if a card fails - the invoice still has to
  clear even if the amount due is small. See billing-payment-failed.

## Troubleshooting

**Symptom: you downgraded and expected a refund.**
Downgrades issue credit by design. refund-policy sets out which cases are refunded in money.

**Symptom: no credit appeared after removing a member.**
Credits land on the **following** invoice, not the current one. Check Billing > Credits for the
balance in the meantime.

**Symptom: the credit is smaller than expected.**
It is prorated by remaining days, not by the full period, and it is calculated on whole days in
UTC.

**Symptom: you want the credit moved to your other workspace.**
Not possible. Credit is workspace-scoped.

**Symptom: you are closing the workspace with credit on it.**
It is forfeited. If the amount is significant, contact support before you confirm the deletion.

## Related articles

- account-downgrade-plan, billing-proration, billing-seat-pricing, refund-policy,
  refund-outage-credit, refund-cancellation, account-close-workspace.

## If this did not help

Contact support with the workspace name and the amount you expected. If you believe the credit
was calculated wrongly, include the date of the change and we will show you the day count we
used.
