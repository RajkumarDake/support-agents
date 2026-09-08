---
title: How proration works on plan changes
category: billing
---

# How proration works on plan changes

Proration is how we charge for a change that happens in the middle of a billing period. The rule
is short: upgrades are immediate and prorated, downgrades wait for the end of the period and
produce credit rather than cash. Everything else in this article follows from those two
sentences.

## Upgrades

An upgrade takes effect the moment you confirm it. You pay the difference between the two plans
for the days remaining in the current period, and your renewal date does not move.

The calculation is daily. If you are 10 days into a 30-day period and move from Pro at $49 per
seat to Business at $90 per seat with 8 seats:

- Days remaining: 20 of 30.
- Difference per seat: $90 - $49 = $41.
- Prorated amount: $41 x 8 seats x 20/30 = $218.67.

That amount appears on your **next** invoice as a line called `Plan change adjustment`, not as a
separate charge on the day. It is one of the most common reasons someone thinks they have been
charged twice - see billing-duplicate-charge.

## Adding and removing seats

Seats prorate the same way. Adding a seat mid-period charges the per-seat price for the remaining
days; removing one credits the unused days. Both appear as `Plan change adjustment` lines, with
the seat count in the description. Invoice descriptions look like
`Plan change adjustment - 2 seats`.

A seat starts costing money when an invitation is accepted, not when it is sent - see
billing-seat-pricing.

## Downgrades

A downgrade takes effect at the end of the current period. You keep the higher plan's features
until then, and you are never refunded the difference in money. The saving becomes account
credit, applied automatically to the next invoice and visible under Billing > Credits. See
refund-downgrade-credit for how the credit behaves and account-downgrade-plan for what stops
working on the day it lands.

## Reading the invoice

A typical invoice after a mid-period upgrade has three kinds of line:

- The recurring plan charge for the new period.
- One or more `Plan change adjustment` lines, positive for additions and negative for removals.
- A credit line applying any balance from Billing > Credits.

The total is the sum. If the arithmetic does not work out, the usual culprit is a change that
happened after the invoice was generated and will appear on the following one instead.

## Edge cases and gotchas

- Proration is calculated on whole days in UTC. A change made late in your evening may count from
  the following day.
- Annual plans prorate against the remaining days of the year, so a mid-year upgrade can be a
  large single line. Check the amount on the confirmation screen before confirming.
- Switching monthly to annual is not an upgrade and does not prorate; it applies at the next
  renewal, see billing-cycle.
- A downgrade scheduled and then reversed before the period ends produces no lines at all.
- Removing and re-adding a person in the same period produces both a credit and a charge that
  nearly cancel - see account-seat-reassignment.
- Proration never changes the renewal date.

## Troubleshooting

**Symptom: an unexpected line called `Plan change adjustment`.**
That is proration, not a second charge. The description names the change and the seat count.

**Symptom: you upgraded but the invoice total looks like the old plan.**
The upgrade happened after the invoice was generated. The adjustment lands on the next one.

**Symptom: you downgraded and expected money back.**
Downgrades issue credit, not refunds. See refund-downgrade-credit.

**Symptom: the prorated amount seems too high.**
Check the seat count in the description. Proration multiplies by seats, and an upgrade often
coincides with adding people.

**Symptom: the credit from removing a seat never appeared.**
Credits land on the following invoice, not the current one. On annual plans they sit in
Billing > Credits until the renewal.

## Related articles

- billing-seat-pricing, billing-cycle, billing-invoice-access, refund-downgrade-credit,
  account-downgrade-plan, billing-duplicate-charge.

## If this did not help

Contact support with the invoice ID and the line you cannot account for. We will show you the
change that produced it, with the date and the person who made it from the audit log.
