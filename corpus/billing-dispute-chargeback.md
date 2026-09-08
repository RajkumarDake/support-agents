---
title: Chargebacks and disputes
category: billing
---

# Chargebacks and disputes

A chargeback is your bank reversing a payment on your behalf. It is a heavy instrument and it has
a consequence people rarely expect: filing one automatically suspends the workspace until the
bank closes the case, which can take up to 90 days, and we cannot lift that suspension while the
case is open. Please contact support first. Almost everything people file chargebacks for is
resolved by us in a few days.

## What happens when a chargeback is filed

1. The bank notifies our processor and pulls the funds back immediately.
2. The workspace is suspended automatically. Suspension is stricter than the read-only mode used
   for failed payments: nobody can sign in, the API returns 403, webhooks stop, and scheduled
   exports do not run.
3. We are given a window to submit evidence, which we always do.
4. The bank rules. This typically takes 30 to 90 days.
5. If the bank rules in your favour the charge stays reversed and the workspace stays suspended
   until the outstanding balance is settled. If it rules in ours, the charge stands and the
   workspace is restored once payment clears.

Your data is safe throughout. Nothing is deleted because of a chargeback.

## Why to contact us first

The two things we see most often behind a dispute are:

- **A duplicate charge.** Refunded in full, no time limit, usually within a few days of you
  sending both invoice IDs. See billing-duplicate-charge and refund-duplicate-charge.
- **An unrecognised company name on the statement.** Our statement descriptor does not always
  match the product name people remember. Compare it against Billing > Invoices before assuming
  fraud.

Both are faster and less disruptive to resolve through support than through a bank. A refund
takes 5-7 business days; a chargeback takes up to 90 and costs you the workspace in the meantime.

## Disputing a specific invoice without a chargeback

If you believe a particular invoice is wrong - the wrong seat count, a plan change you did not
authorise, tax applied that should not have been - raise it as an invoice dispute instead. That
process is described in billing-invoice-dispute and pauses collection on the disputed amount
while we look at it.

## If a chargeback has already been filed

1. Contact support with the workspace name and the invoice ID.
2. Tell us the reason code your bank gave you if you have it.
3. Withdraw the dispute with your bank if the underlying issue is one we can fix. Ask the bank
   for written confirmation of the withdrawal.
4. Send us that confirmation. We can then lift the suspension without waiting for the full case
   to close.

Only the bank can withdraw a dispute. We cannot do it for you, and neither can the processor.

## Edge cases and gotchas

- Suspension applies to the workspace, not to the person who filed. Your whole team is locked out
  by one person's phone call to their bank.
- A workspace under an open dispute cannot be deleted, downgraded or have its plan changed. See
  account-close-workspace.
- Repeated chargebacks can result in the account being refused card payment in future, leaving
  only invoice terms.
- Account credit is not touched by a chargeback and is not paid out.
- The dispute, the suspension and the resolution are all written to the audit log, see
  account-audit-logs.
- If the workspace is suspended and you need your data urgently, contact support - we can arrange
  a one-off export while the case is open.

## Troubleshooting

**Symptom: everyone is locked out with no warning.**
Check whether anyone with access to the card filed a dispute. This is the usual explanation for a
sudden full lockout as opposed to read-only mode.

**Symptom: read-only rather than locked out.**
That is a failed payment, not a chargeback. See billing-payment-failed - it is far easier to fix.

**Symptom: the bank says the case is closed but the workspace is still suspended.**
Send us the bank's written confirmation. We do not always receive the closure notice promptly
from the processor.

**Symptom: you filed by mistake.**
Call the bank the same day. Early withdrawals are much easier than late ones.

## Related articles

- billing-duplicate-charge, billing-invoice-dispute, billing-payment-failed.

## If this did not help

Contact support with the workspace name, the invoice ID, the date you filed, and your bank's
reason code. Mark the message urgent if your team is locked out - suspensions are handled ahead
of the normal queue.
