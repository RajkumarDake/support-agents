---
title: Requesting a refund
category: refunds
---

# Requesting a refund

There is no refund button in the product. Every refund is decided by a human, because almost
every request needs a judgement call about the plan, the period and how the workspace was used.
That sounds slower than it is: a decision is made within one business day.

## What to send

Contact support with:

1. **The invoice ID**, in the form `INV-NNNN`. Find it under Billing > Invoices, see
   billing-invoice-access. Without this we cannot start.
2. **One line on what happened.** "Charged after we cancelled on the 3rd", "two identical charges
   on 2026-09-02", "signed up, never used it, want to stop" are all perfectly good.
3. **For duplicates, both invoice IDs.** We need to confirm that two payments settled rather than
   one payment plus a pending authorisation - see billing-duplicate-charge.

That is genuinely all. You do not need to build a case; extra detail neither helps nor hurts.

## Who can request

Anyone can write to us, but we act on instructions from an Owner or Admin, or from the billing
email on file. If you are a Member, ask your Owner to send it or to confirm your message. See
account-roles-permissions.

## What happens

- A human reads it and decides within one business day. You get an answer either way, including
  a reason if the answer is no.
- If approved, the refund leaves us the same day.
- Card networks then take 5-7 business days, and some banks up to 10. SEPA reversals take 3-5.
  See refund-timeline.
- You receive an email confirmation and a credit note when the refund is issued, not when it
  lands.
- The invoice status changes to `refunded` under Billing > Invoices.

## Which route is actually yours

| Situation | Use |
|---|---|
| Two identical settled charges | refund-duplicate-charge |
| Charged after cancelling | refund-cancellation |
| Downgraded and expecting money back | refund-downgrade-credit - it is credit, not cash |
| An outage in a month you paid for | refund-outage-credit |
| One line on the invoice is wrong | billing-invoice-dispute |
| Signed up, never used it, within 14 days | this article |

Picking the right one first is the main thing that makes a refund fast.

## Edge cases and gotchas

- Refunds go to the original payment method only. We cannot pay to a different card or a bank
  account.
- Requesting a refund does not cancel your subscription. Cancel separately under Settings > Plan,
  see refund-cancellation.
- A refund on an invoice does not reverse the usage it paid for. If you refund a period, the
  workspace does not lose data.
- Do not file a chargeback while a refund request is open. It suspends the workspace for up to 90
  days and stops us refunding at all - see billing-dispute-chargeback.
- If the card that paid has since been closed, the refund still goes to it. The issuing bank
  forwards it to the replacement account, which adds a few days.
- For amounts on an Enterprise contract, refunds follow the contract terms and are handled by
  your account contact rather than the normal queue.

## Troubleshooting

**Symptom: no answer after a business day.**
Reply on the same thread rather than opening a second request. Duplicate threads split the
history and go to the back of the queue.

**Symptom: told the refund was issued but nothing has arrived.**
Check the date on the confirmation email and count business days: 5-7 typical, up to 10 for some
banks. See refund-timeline.

**Symptom: you cannot find the invoice ID.**
Send the date, the amount and the last four digits of the card instead, and we will find it.

**Symptom: refused.**
Read refund-policy for which category your charge fell into. If circumstances were unusual, say
so - exceptions for prolonged outages are decided by a support lead.

## Related articles

- refund-policy, refund-timeline, refund-cancellation.

## If this did not help

Contact support with the invoice ID and one sentence. If it is urgent because the amount is large
or the charge was unauthorised, say that in the first line and it is picked up ahead of the
queue.
