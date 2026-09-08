---
title: Billing cycles and renewal dates
category: billing
---

# Billing cycles and renewal dates

Your billing cycle decides when you are charged and what a "period" means for every usage limit
in the product. Most questions about a surprising invoice date are answered by understanding two
things: when the cycle rolls over, and what happens when the day of the month does not exist.

## Where to look

Billing > Overview shows the current plan, the next renewal date, and the amount expected on that
date. Billing > Invoices shows what has actually been charged - see billing-invoice-access.
Settings > Plan and usage shows how much of the period's allowance you have used.

## Monthly plans

A monthly plan renews on the same day of the month you subscribed. Subscribe on the 14th and you
renew on the 14th of every month.

If the day does not exist in a shorter month, we charge on the last day of that month. A
subscription started on the 31st renews on 30 April, 28 February, or 29 February in a leap year,
and returns to the 31st in months that have one. The renewal date shown in Billing > Overview
always reflects the real next date, so trust it over the arithmetic.

## Annual plans

Annual plans are charged in full on the anniversary date. We email a renewal notice to the Owner
and to the billing email seven days before the charge, so there is time to change the card or
cancel. See billing-payment-methods and refund-cancellation.

Annual plans are the only ones eligible for SEPA direct debit in the EU.

## Switching between monthly and annual

Switching from monthly to annual applies at the next renewal, not immediately. You are not
charged a year on the day you click; you finish the current month and the annual charge lands on
the normal renewal date. Switching from annual to monthly likewise takes effect at the end of the
annual term.

Upgrading the tier is different and does apply immediately, prorated - see billing-proration.

## Periods and usage

Usage counters - API calls in particular - reset at the start of each billing period, at the same
moment the renewal charge is raised. Storage does not reset, because it is a standing total. This
is why an ERR_4029 that appears on the 13th disappears on its own on the 14th, and an ERR_5140
does not. See account-plan-and-usage.

For annual plans the API allowance is still counted monthly, on the monthly anniversary of the
annual start date. An annual plan is not a year's worth of calls to spend at once.

## Edge cases and gotchas

- Invoices are dated when the charge is captured, which can be a few hours after the renewal
  boundary in your local time zone. An invoice dated the day after the renewal date is normal.
- Time zone: renewals run in UTC. If you are in UTC+10 a renewal can look like it happened
  "tomorrow".
- A failed payment does not move the renewal date. Retries happen on day 1, 3 and 7 against the
  same invoice - see billing-payment-failed.
- A mid-cycle upgrade does not reset the cycle. Your renewal date stays where it was and the
  extra appears as a `Plan change adjustment` line.
- Cancelling does not change the renewal date either; it stops the charge that would have
  happened on it.
- Reactivating a cancelled subscription starts a new cycle from the reactivation day.

## Troubleshooting

**Symptom: charged a day early or a day late.**
Compare the invoice timestamp in UTC against your local time. A shift of a few hours across
midnight explains almost all of these.

**Symptom: two charges close together.**
Usually a monthly renewal plus a prorated `Plan change adjustment` from an upgrade. If both lines
are the identical plan amount on the same date, that is a real duplicate - see
billing-duplicate-charge.

**Symptom: the renewal notice never arrived.**
Renewal notices go to the Owner and to the billing email, which are often different addresses.
Check both, then update the billing email under Billing > Business details.

**Symptom: an annual renewal you wanted to stop.**
Cancel before the anniversary date. After it, annual terms are not refunded pro rata by default -
refund-policy explains the exceptions.

## Related articles

- billing-proration, billing-invoice-access, billing-payment-failed.

## If this did not help

Contact support with the workspace name and the invoice ID you are asking about. Include what
date you expected instead - most of these turn out to be a time zone or a proration line, and
both are quick to confirm.
