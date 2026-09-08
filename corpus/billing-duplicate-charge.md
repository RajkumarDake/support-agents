---
title: Duplicate or double charges
category: billing
---

# Duplicate or double charges

Seeing the same amount twice on a statement is alarming and usually harmless. Three different
things look identical from the bank's side, and only one of them is a real double charge. Work
through them in order before contacting anyone.

## The three causes

**1. A retried authorisation.** Our processor retries a card authorisation that timed out. Your
bank shows both the abandoned authorisation and the successful capture. The abandoned one is
never settled and drops off your statement within 3-5 business days on its own. In your invoice
list there is only one invoice. There is nothing for us to refund, because we only ever received
one payment.

**2. A real double charge.** Two settled invoices, same amount, same date, both with status
`paid` in Billing > Invoices. Money genuinely left your account twice and one must be refunded.

**3. A plan change.** A mid-cycle upgrade or seat addition bills a prorated
`Plan change adjustment` that can be close to a full plan amount and lands days after the
recurring charge. Two charges, both correct. See billing-proration.

## How to tell them apart in 60 seconds

1. Open Billing > Invoices.
2. Count the invoices with status `paid` for the date in question.
3. **One invoice** and two lines on the statement: cause 1. Wait 3-5 business days.
4. **Two invoices, identical amount and date, both `paid`**: cause 2. Contact support with both
   invoice IDs.
5. **Two invoices, one recurring and one `Plan change adjustment`**: cause 3. Correct as charged.

## Getting a real duplicate refunded

Contact support with both invoice IDs, in the form `INV-NNNN`. We confirm from our side that two
payments settled rather than one payment plus a pending authorisation, then refund the duplicate
in full.

- Duplicate charges are refunded in full and are not subject to the 14-day refund window.
- The refund leaves us the same day it is approved and takes 5-7 business days to appear on a
  card, up to 10 with some banks, and 3-5 for SEPA. See refund-timeline.
- You receive a credit note when the refund is issued. The invoice status changes to `refunded`.
- refund-duplicate-charge covers the refund side in more detail.

## Known incident: 2026-09-02

A retry in the payment processor captured a small batch of monthly invoices twice on
2026-09-02 (incident INC-2285, now resolved). Affected customers have two identical `paid`
invoices dated 2026-09-02. If that describes what you are seeing, contact support with both
invoice IDs and the duplicate is refunded in full - this is being handled case by case by the
billing team, so there is no automatic sweep. See tech-service-status for the incident record.

## Edge cases and gotchas

- An unrecognised company name on the statement is not a duplicate. Check the statement
  descriptor before counting charges.
- Two workspaces on the same card produce two charges of similar size on similar dates. Confirm
  the workspace name on each invoice.
- Currency conversion means the two statement amounts may differ by a few cents even for a true
  duplicate. Compare the invoice amounts, not the statement amounts.
- A failed payment that later succeeded is one charge, not two, even though you were emailed
  twice - see billing-payment-failed.
- Do not file a chargeback for a suspected duplicate. It suspends the workspace for up to 90 days
  and takes far longer than asking us. See billing-dispute-chargeback.

## Troubleshooting

**Symptom: two pending charges, no second invoice.**
Cause 1. The pending authorisation is released by your bank in 3-5 business days.

**Symptom: two `paid` invoices but different amounts.**
Not a duplicate. The smaller one is proration; open it and read the line description.

**Symptom: two `paid` invoices, identical, and you are on annual billing.**
Still a duplicate and still refundable in full. Send both IDs.

**Symptom: the bank insists it is two settled charges but you only see one invoice.**
Send support the statement line with the descriptor, date, amount and last four digits. We can
search by that.

## Related articles

- refund-duplicate-charge, billing-proration, billing-invoice-access.

## If this did not help

Contact support with both invoice IDs, or with a screenshot of the statement lines if you cannot
find two invoices. Say which of the three causes above you have already ruled out - it saves a
round trip.
