---
title: How long a refund takes
category: refunds
---

# How long a refund takes

Once a refund is approved it leaves us the same day. Everything after that is your bank's
timetable, not ours, and that is where the waiting happens. This article sets out realistic
numbers so you know when it is worth chasing.

## The timeline

| Stage | Who | Typical duration |
|---|---|---|
| Decision on the request | Us | 1 business day |
| Refund issued to the processor | Us | Same day as approval |
| Confirmation email and credit note | Us | Within minutes of issue |
| Card network settlement | Your bank | 5-7 business days |
| Slow issuers | Your bank | up to 10 business days |
| SEPA direct debit reversal | Your bank | 3-5 business days |
| ACH or wire reversal | Your bank | 5-10 business days |

Business days exclude weekends and bank holidays in the card issuer's country, which is why a
refund issued on a Friday before a long weekend can feel like it has vanished.

## The confirmation email

You get an email with the refund confirmation and a credit note **when the refund is issued**,
not when it lands in your account. This trips people up constantly: the email is our receipt for
sending the money, not your bank's receipt for receiving it. The invoice status in Billing >
Invoices changes to `refunded` at the same moment, again reflecting our side.

If you need proof for your finance team while you wait, the credit note is the document to use.
See billing-invoice-access for where to download it.

## What can make it slower

- **A closed card.** The refund still goes to the original card, and the issuing bank forwards it
  to the replacement account. Add several days.
- **Currency conversion.** The amount that lands may differ slightly from the invoice amount
  because your bank converts at a different rate on the refund date than on the charge date. We
  refund the exact amount charged in the invoice currency.
- **A bank that posts refunds only on statement cycles.** Some issuers batch. The money is with
  them before you can see it.
- **A pending authorisation being confused for a refund.** If the original charge never settled
  there is nothing to refund - the authorisation drops off in 3-5 business days on its own. See
  billing-duplicate-charge.

## Edge cases and gotchas

- Refunds always go to the original payment method. There is no alternative destination.
- Account credit is not a refund and does not follow this timeline at all. It is applied to your
  next invoice automatically - see refund-downgrade-credit.
- A refund does not cancel the subscription. Cancel separately, see refund-cancellation.
- Service credits from an outage are applied to the next invoice rather than paid out, so they do
  not appear on a card statement at all - see refund-outage-credit.
- Tax is refunded with the charge and appears in the same transaction, not separately.
- If a chargeback is open on the same invoice we cannot refund it; the bank's process must close
  first. See billing-dispute-chargeback.

## Troubleshooting

**Symptom: 10 business days have passed and nothing has arrived.**
Reply on the original thread with the refund confirmation email. We can supply an acquirer
reference number, sometimes called an ARN, which your bank can use to locate the transaction
directly.

**Symptom: the amount is slightly less than the charge.**
Currency conversion by your bank. Compare the invoice amounts rather than the statement amounts.

**Symptom: the invoice says `refunded` but the money is not there.**
That status is our side. Count business days from the confirmation email date.

**Symptom: you received a credit note but expected money.**
Check which mechanism applied. Downgrades and outage credits are account credit; only refunds
move money.

**Symptom: the bank says they have no record.**
Ask them to search by the ARN rather than by amount and date. Request it from us on the same
thread.

## Related articles

- refund-how-to-request, refund-policy, refund-duplicate-charge.

## If this did not help

Contact support with the invoice ID and the date on your refund confirmation email, and say
whether your bank has been asked to search. The acquirer reference number is the thing that
resolves the genuinely stuck ones.
