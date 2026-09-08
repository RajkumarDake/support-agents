---
title: Disputing an invoice
category: billing
---

# Disputing an invoice

If an invoice is wrong, you can dispute it directly with us rather than refusing the payment or
calling your bank. Disputing pauses collection on the amount in question while we investigate, so
the workspace does not slide into the failed-payment retry schedule while we talk. This is the
route to use for a billing disagreement; billing-dispute-chargeback covers what happens if you go
to the bank instead, and it is worse for everyone.

## Before you dispute: the four usual answers

Most invoices that look wrong are explained by one of these, and checking takes a minute:

1. **A `Plan change adjustment` line.** That is proration from an upgrade or a seat change, not a
   second charge. See billing-proration.
2. **More seats than you expected.** Deactivated members and SCIM-created accounts still hold
   billed seats. See billing-seat-pricing.
3. **Tax you did not expect.** No valid VAT or GST number was on file when the invoice was
   issued. See billing-tax-vat.
4. **Two identical charges.** That is a duplicate, handled by its own faster process. See
   billing-duplicate-charge.

## How to raise a dispute

1. Open Billing > Invoices and open the invoice.
2. Click Dispute this invoice.
3. Select the specific lines you are disputing. Disputing the whole invoice when only one line is
   wrong slows the review down.
4. Choose a reason: incorrect seat count, plan change not authorised, tax incorrect, service not
   delivered, duplicate, or other.
5. Add one or two sentences of detail, including any dates that matter.
6. Submit. You get a reference in the form `DSP-NNNN`.

Owner and Admin only, like everything under Billing - see account-roles-permissions.

## What happens next

- The disputed amount is placed on hold. Automatic retries stop for that amount, and the
  workspace does not move toward read-only because of it.
- Undisputed lines on the same invoice remain due and are collected normally.
- A human reviews it. We aim for a first response within one business day, and a decision within
  three for anything that does not need a plan history reconstruction.
- If we agree, we issue a corrected invoice and a credit note for the difference. If money has
  already moved, the difference is refunded to the original payment method within 5-7 business
  days - see refund-timeline.
- If we disagree, we explain the calculation with the underlying events from the audit log, and
  the hold is released with 7 days to pay.

## What we will ask you for

The invoice ID, which lines are wrong, and what you believe the correct amount is. For a seat
dispute, the headcount you expect to pay for. For an unauthorised plan change, the approximate
date you noticed. We can supply the actor and timestamp of every plan and seat change from the
audit log, which resolves most of these in one message - see account-audit-logs.

## Edge cases and gotchas

- Disputing does not pause the next period's invoice. If the same error will recur, fix the
  underlying setting too.
- You cannot dispute an invoice that has already been refunded, or one older than 12 months.
- Disputing while a chargeback is open on the same invoice is not possible; the bank's process
  takes precedence and must close first.
- A dispute upheld in your favour produces a credit note. Whether you get money back or account
  credit depends on the reason: an overcharge is refunded, a downgrade timing question is credit,
  see refund-downgrade-credit.
- On Enterprise contracts with net 30 terms, disputing before the due date avoids any late-payment
  consequence entirely.

## Troubleshooting

**Symptom: no Dispute this invoice button.**
You are a Member or Viewer, or the invoice is over 12 months old. Contact support directly in the
second case.

**Symptom: the workspace went read-only during a dispute.**
Only the disputed amount is held. An earlier undisputed invoice is probably still open - check
Billing > Invoices for anything with status `open` or `failed`, see billing-payment-failed.

**Symptom: you disputed the wrong invoice.**
Withdraw it from the same screen and raise the right one. Withdrawing releases the hold
immediately.

**Symptom: no response after a business day.**
Reply on the same thread with the `DSP-NNNN` reference rather than opening a second dispute -
duplicates go to the back of the queue.

## Related error codes

- ERR_2031 - your role cannot view or dispute invoices.

## Related articles

- billing-invoice-access, billing-proration, billing-seat-pricing, billing-tax-vat,
  billing-duplicate-charge, billing-dispute-chargeback, refund-how-to-request.

## If this did not help

Contact support with the invoice ID, the disputed lines, and the amount you believe is correct.
If the same error is about to repeat on the next renewal, say so - we will hold the next invoice
too rather than making you dispute it twice.
