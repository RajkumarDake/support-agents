---
title: Cancelling a subscription
category: refunds
---

# Cancelling a subscription

To cancel a subscription, go to Settings > Plan and click Cancel subscription. Cancelling stops
the next charge. It does not delete anything, it does not take effect immediately, and it is fully
reversible. If you want the data gone as well, that is a separate and much more serious action -
see account-close-workspace.

## Steps

1. Open Settings > Plan.
2. Click Cancel subscription. Owner only - Admins can read the plan screen but not change it, see
   account-roles-permissions.
3. Tell us why if you want to. It is optional and it is read by a person.
4. Confirm. The confirmation names the exact date access changes.

A banner shows the pending cancellation until the date arrives. You can undo it at any point
before then from the same screen.

## What happens and when

- **Immediately:** the next renewal is cancelled. Nothing else changes. You keep full access,
  every feature of your plan, and every seat.
- **At the end of the current period:** the workspace becomes read-only. Everyone can sign in and
  read, exports still run, but nobody can create, edit or upload.
- **Ongoing:** your data stays. There is no purge timer attached to cancellation. Invoices remain
  downloadable, see billing-invoice-access.
- **If you resubscribe:** full access returns immediately and a new billing cycle starts from
  that day, see billing-cycle.

## Money

You are not refunded the period you have already paid for. The plan runs to the end of it, which
is why you keep full access until then. This is set out in refund-policy.

The exception, and it is absolute: **if you were charged after cancelling, that charge is
refunded in full.** Send us the invoice ID. There is no time limit on this one and no judgement
involved.

Annual plans cancelled mid-term are not refunded pro rata by default. The term runs to the
anniversary date. Cancel before the renewal notice, which we send seven days out, to avoid the
next year entirely.

## Before you cancel, consider

- **Downgrading instead.** Dropping to a cheaper tier keeps the workspace writable. See
  account-downgrade-plan.
- **Removing unused seats.** If cost is the problem and headcount is the cause, this often solves
  it - see billing-seat-pricing.
- **Exporting first.** A read-only workspace can still export, but do it while everything is
  fresh in mind. See tech-data-export.

## Edge cases and gotchas

- Cancelling does not free seats or stop the seat count for the remaining period. You are paying
  for them either way.
- Cancelling does not remove members. They keep access until the period ends.
- API tokens keep working for reads after the period ends and return errors on writes. See
  tech-api-keys.
- Webhooks stop delivering when the workspace becomes read-only, and endpoints eventually go
  unhealthy - see tech-webhooks.
- Account credit remaining at cancellation stays on the account and is applied if you
  resubscribe. It is forfeited only if the workspace is deleted, see refund-downgrade-credit.
- An open invoice must still be paid. Cancelling does not write off what you already owe, see
  billing-payment-failed.
- Cancelling while a chargeback is open is blocked until the case closes, see
  billing-dispute-chargeback.

## Troubleshooting

**Symptom: no Cancel subscription button.**
You are an Admin, not the Owner. Ask the Owner or transfer ownership, see
account-transfer-ownership.

**Symptom: charged after cancelling.**
Send support the invoice ID. Refunded in full, no argument.

**Symptom: the workspace went read-only earlier than you expected.**
Check whether the cause was cancellation or a failed payment - the latter happens on day 15 of
the grace period and looks identical. See billing-payment-failed.

**Symptom: you cancelled the wrong workspace.**
Undo it from the banner on Settings > Plan before the period ends. After that, resubscribe.

**Symptom: you want the data deleted too.**
Cancellation does not do that. See account-close-workspace, and export first.

## Related articles

- refund-policy, refund-how-to-request, account-downgrade-plan.

## If this did not help

Contact support with the workspace name and the date you cancelled. If you were charged after
cancelling, include the invoice ID and we will refund it without further questions.
