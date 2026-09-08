---
title: How seats are counted and billed
category: billing
---

# How seats are counted and billed

You are billed per active seat. Understanding exactly when a seat becomes active, when it stops,
and which roles are free is enough to predict every invoice this product produces.

## Pricing

| Plan | Price | Seats included | Free Viewers |
|---|---|---|---|
| Starter | $29/month flat | 3 members total | No |
| Pro | $49 per seat/month | up to 25 | No |
| Business | $90 per seat/month | unlimited | Yes |
| Enterprise | Contract | unlimited | Yes |

Starter is a flat fee rather than per seat: three people cost the same as one. Pro and Business
multiply the per-seat price by the number of active seats each period.

## When a seat starts and stops

- A **pending invitation** does not consume a seat and is not billed. You can have twenty
  outstanding invitations on a three-seat plan.
- A seat becomes **active** the moment the invitation is accepted, and is charged prorated for
  the rest of the period.
- **Removing** a member frees the seat immediately, but the money comes back as a credit on the
  following invoice, not as a refund.
- **Deactivating** someone on Business or Enterprise does not free the seat. They are still
  billed. Remove them to stop paying - see account-remove-member.
- **Viewers** on Business and Enterprise are free and do not count toward the seat total. On
  Starter and Pro they are ordinary billed seats. See account-guest-viewer-access.
- **SCIM-provisioned** accounts consume a seat as soon as the directory creates them, before the
  person has ever signed in. See account-scim-provisioning.

## Where seats show up

- Settings > Plan and usage: seats used against seats included, live.
- Billing > Overview: the amount expected at the next renewal.
- Billing > Invoices: the recurring line, plus `Plan change adjustment` lines for mid-period seat
  changes, described as `Plan change adjustment - 2 seats` and similar.

## Worked example

A Business workspace with 18 seats at $90 renews at $1,620 per month. Adding two people 15 days
into a 30-day period adds $90 x 2 x 15/30 = $90 to the next invoice as an adjustment line, and
the following renewal is $1,800. Converting three of those people to Viewers frees three seats
and credits the unused days.

## Edge cases and gotchas

- The seat count on the invoice is the count at the moment of renewal. Changes during the period
  are handled by adjustment lines, so the recurring line alone will not match your headcount on
  any given day.
- Hitting the plan's cap blocks new invitations with ERR_2044 before any email is sent, so
  nothing is charged for a failed invite - see account-add-team-member.
- Starter's cap is a hard 3. There is no per-seat overage; you upgrade or you remove someone.
- Pro's cap of 25 is likewise hard. The 26th person needs Business.
- Removing someone on the last day of a period can round the credit to zero.
- Seats are per workspace. The same person in two workspaces is two seats.

## Troubleshooting

**Symptom: billed for more seats than you have people.**
Deactivated members hold seats. Check Settings > Team for rows marked Deactivated, and check for
SCIM-created accounts nobody ever used.

**Symptom: billed for a Viewer on Business.**
Their role is probably Member. Confirm in Settings > Team and change it; the credit appears next
invoice.

**Symptom: a seat you removed is still on the invoice.**
The recurring line was raised at renewal. Look for the offsetting credit line, or check
Billing > Credits.

**Symptom: ERR_2044 with an apparently free seat.**
A pending invitation from an earlier attempt is holding the slot in your mental model but not in
ours - check for a member who accepted and was forgotten.

**Symptom: the total does not equal seats x price.**
Proration and credits. billing-proration walks through each line type.

## Related error codes

- ERR_2044 - seat limit reached.
- ERR_2031 - your role cannot view billing.

## Related articles

- billing-proration, account-add-team-member, account-remove-member.

## If this did not help

Contact support with the workspace name and the invoice ID, and tell us the headcount you expect
to be paying for. We will reconcile the two line by line.
