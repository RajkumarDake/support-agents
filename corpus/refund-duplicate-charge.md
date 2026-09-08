---
title: Refunds for duplicate charges
category: refunds
---

# Refunds for duplicate charges

A duplicate charge is refunded in full and is not subject to the 14-day window in refund-policy.
There is no judgement call to make: if two payments settled where one should have, one comes back.
The only work is confirming that two payments genuinely settled.

## Confirm it is a duplicate first

Open Billing > Invoices and look at the invoices, not at your bank statement.

- **Two invoices, identical amount, same date, both `paid`.** A real duplicate. Proceed.
- **One invoice, two lines on the statement.** A pending authorisation that never settled. Your
  bank releases it in 3-5 business days and there is nothing for us to refund, because we only
  received one payment.
- **Two invoices with different amounts.** Not a duplicate. The smaller is almost always a
  `Plan change adjustment` from proration - see billing-proration.

billing-duplicate-charge walks through the same decision in more detail with the statement-side
symptoms.

## Requesting the refund

Send support **both invoice IDs**, in the form `INV-NNNN`. We need both because that is how we
distinguish two settled payments from one payment plus a pending authorisation - the bank
statement alone cannot tell those apart.

You do not need to explain anything else. The message can be one line.

## What happens

1. We confirm both payments settled against the processor.
2. The duplicate is refunded in full, including any tax that was charged on it.
3. The refunded invoice moves to status `refunded` and a credit note is issued.
4. The money leaves us the same day and takes 5-7 business days to appear on a card, up to 10
   with some banks, 3-5 for SEPA. See refund-timeline.

Expect a decision within one business day. Duplicates are the fastest category we handle because
there is nothing to weigh up.

## The 2026-09-02 batch

A retry in the payment processor captured a small batch of monthly invoices twice on 2026-09-02.
This is incident INC-2285, now resolved. Affected customers have two identical `paid` invoices
dated 2026-09-02.

Refunds for this batch are being issued on request, case by case, by the billing team - there is
no automatic sweep, so you do need to write in. Contact support with both invoice IDs and the
duplicate is refunded in full. See tech-service-status for the incident record and how to check
whether an incident is behind what you are seeing.

## Edge cases and gotchas

- Both invoices show as `paid`, so neither looks like the "wrong" one. We refund the later
  capture and keep the earlier; the effect is identical.
- Refunding a duplicate does not affect your plan, your seats, or your renewal date. Nothing about
  the subscription changes.
- If the duplicate spanned a currency conversion, the amounts on your statement may differ by a
  few cents. We refund the invoice amount exactly.
- Do not file a chargeback. It suspends the workspace for up to 90 days, blocks us from refunding
  at all while the case is open, and takes far longer. See billing-dispute-chargeback.
- Two charges for two different workspaces on the same card are not duplicates. Check the
  workspace name printed on each invoice.

## Troubleshooting

**Symptom: only one invoice exists but the bank shows two settled charges.**
Send support the statement line: descriptor, date, amount and last four digits. We can search the
processor by that.

**Symptom: the second charge disappeared before you wrote in.**
It was a pending authorisation. Nothing further to do.

**Symptom: refunded amount looks short.**
Currency conversion on your side, or you are comparing against the statement rather than the
invoice.

**Symptom: it happened again the next month.**
That is not a duplicate pattern, it is a configuration problem - two subscriptions on one card,
or two workspaces. Send both invoice IDs and we will identify which is which.

## Related articles

- billing-duplicate-charge, refund-policy, refund-timeline.

## If this did not help

Contact support with both invoice IDs. If you only have one, send the date, amount and last four
digits of the card and we will find the other.
