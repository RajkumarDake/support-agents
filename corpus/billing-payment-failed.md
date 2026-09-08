---
title: Failed payments and card declines
category: billing
---

# Failed payments and card declines

When a charge fails, nothing dramatic happens straight away. You get a fortnight to fix it, your
data is never at risk, and in most cases updating the card resolves everything in under a minute.
This article explains the retry schedule, what changes on each day, the common decline reasons,
and how to get out of a read-only workspace.

## The retry schedule

| Day | What happens | Workspace state |
|---|---|---|
| 0 | Charge fails, invoice moves to `open`, Owner emailed | Fully active |
| 1 | First automatic retry | Fully active |
| 3 | Second automatic retry, Owner and billing email notified | Fully active |
| 7 | Third and final automatic retry | Fully active |
| 14 | Final warning email | Fully active |
| 15 | Invoice moves to `failed` | Read-only |

Your workspace stays fully active for the whole 14-day grace period. On day 15 it moves to
read-only: everything is readable, exports still run, but you cannot create, edit or upload until
a payment succeeds. Nothing is deleted, and no data is lost at any point in this process.

## Fixing it

1. Open Billing > Payment method.
2. Add or update the card. Owner only - Admins can see invoices but not change how the workspace
   pays, see account-roles-permissions.
3. Saving a new payment method retries the outstanding invoice immediately. You do not need to
   wait for the next scheduled retry.
4. Confirm the invoice status has moved to `paid` under Billing > Invoices.

If the workspace was read-only, write access returns within a minute of the successful capture.

## Common decline reasons

- **Expired card.** By far the most common. Check the expiry on the card in Billing > Payment
  method against today's date.
- **Insufficient funds.** Retry after topping up; the day 3 or day 7 retry may catch it anyway.
- **Bank block on recurring international payments.** Very common for cards issued outside the
  US. The bank must allow the merchant; we cannot do this from our side.
- **3-D Secure challenge not completed.** Some issuers require an interactive confirmation that a
  background retry cannot satisfy. Update the card in the UI so the challenge can be shown.
- **Unsupported card type.** Prepaid cards are not accepted, and neither is PayPal - see
  billing-payment-methods. This surfaces as ERR_3112.

## Preventing the next one

Add a backup card under Billing > Payment method. If the primary declines we try the backup
before starting the retry schedule, so a single expired card never interrupts service. Also check
that the billing email in Billing > Business details reaches someone who will act - the Owner's
address alone is often a person on holiday.

## Edge cases and gotchas

- A failed payment does not move your renewal date. The next period's invoice is raised on
  schedule even while the previous one is open, so two open invoices can accumulate.
- Read-only mode does not free seats or stop the seat count. You are still billed for them.
- API tokens keep working in read-only mode for reads and return an error on writes.
- Plan changes are queued behind an outstanding invoice. Clear the invoice first, then upgrade or
  downgrade - see account-downgrade-plan.
- Filing a chargeback instead of updating the card suspends the workspace entirely for up to 90
  days, which is far worse than read-only. See billing-dispute-chargeback.
- SEPA direct debit failures behave the same way but take longer to report, because the bank's
  rejection can arrive days after the debit.

## Troubleshooting

**Symptom: ERR_3112 "payment method rejected" when saving the card.**
The card was declined at authorisation, or the type is not supported. Try another card, and ask
the bank whether recurring international payments are blocked.

**Symptom: the card is fine but the retry keeps failing.**
Remove the card and add it again rather than editing it. A stale token at the processor is
occasionally the cause.

**Symptom: paid but still read-only.**
Check that the invoice you paid is the outstanding one. If two invoices are open, both must be
settled. Reload after a minute.

**Symptom: no emails about any of this.**
They go to the Owner and the billing email. Check spam and confirm both addresses under Billing >
Business details.

**Symptom: you were charged after the workspace went read-only.**
That is the successful retry. Access should have returned; if it has not, contact support with
the invoice ID.

## Related error codes

- ERR_3112 - payment method rejected or unsupported.
- ERR_2031 - only the Owner can change the payment method.

## Related articles

- billing-payment-methods, billing-invoice-access, billing-cycle.

## If this did not help

Contact support with the workspace name, the invoice ID, and the decline message your bank gave
you if you have it. We can see the processor's decline code, which is usually more specific than
what the UI shows.
