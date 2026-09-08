---
title: Reassigning a seat to someone else
category: account
---

# Reassigning a seat to someone else

When somebody leaves and a replacement joins, you want the replacement to take over the empty
seat rather than push the workspace onto a bigger plan. There is no single "reassign" button:
a seat is freed by removing the previous holder and taken by the next person accepting an
invitation. Done in the right order it costs nothing extra. Done in the wrong order it can
trigger ERR_2044 or an unnecessary upgrade.

## The correct order

1. Open Settings > Team and confirm which seats are actually occupied. Deactivated people still
   hold a seat.
2. Remove the person who is leaving - overflow menu > Remove from workspace. The seat is freed
   immediately. See account-remove-member for what happens to their content and tokens.
3. Invite the replacement with the role they need. The seat is taken when they accept.
4. Add them to the same projects the previous person belonged to. Note these down before you
   remove, because the membership list disappears with the person.

If you invite first and remove second on a full plan, step 3 fails with ERR_2044 because no seat
is free at that moment.

## What it costs

The freed seat produces a credit for the unused days, and the new seat produces a prorated charge
for the remaining days. When both happen in the same period at the same price they very nearly
cancel out. You will still see two lines on the next invoice - a credit and a
`Plan change adjustment` - rather than nothing at all. billing-proration and
billing-seat-pricing describe both lines.

Same-day swaps usually net to a rounding difference of well under a dollar. Swaps across a
renewal boundary do not net at all: the credit lands on one invoice and the charge on the next.

## What does not transfer

A seat is a billing unit, not an identity. Nothing belonging to the old person moves to the new
one automatically:

- Content they created is reassigned to the Owner when they are removed, not to the replacement.
  An Owner can then reassign items individually.
- Project membership is not inherited. Add the replacement to projects explicitly.
- API tokens are revoked and cannot be handed over. The replacement creates their own - see
  tech-api-keys.
- Personal notification preferences are not copied. See onboarding-notifications.
- Integrations are owned by the workspace and keep working regardless, see
  onboarding-integrations.

## Alternatives worth knowing

- **Changing the email address instead.** If the same human is simply changing address, an Owner
  or Admin can edit the address on the existing row under Settings > Team rather than doing a
  remove-and-invite. Everything is preserved, and no billing event occurs. This does not work
  when SSO or SCIM drives identities.
- **Downgrading to Viewer.** On Business and Enterprise, moving someone to Viewer frees the
  billed seat while keeping their read access and history. See account-guest-viewer-access.
- **Deactivate rather than remove** if the person is on leave and coming back. They keep the
  seat and it stays billed.

## Edge cases and gotchas

- On Starter the cap is 3 members with no free Viewer tier, so a swap always needs the removal
  first.
- If SCIM is enabled, do the whole swap in your identity provider. Changes made here are
  overwritten at the next sync - see account-scim-provisioning.
- Removing someone with an open export job cancels the job. Re-run it as the new person.
- The replacement gets the Owner's accumulated reassignments only if the Owner hands them over
  deliberately.

## Troubleshooting

**Symptom: ERR_2044 when inviting the replacement.**
The seat was not actually freed. Check for deactivated rows, or for a pending invitation from an
earlier attempt that you assumed had lapsed.

**Symptom: the invoice went up even though headcount is unchanged.**
The credit and the charge landed in different periods. Compare the two invoices side by side in
Billing > Invoices; the total across both should be right.

**Symptom: the replacement cannot see anything.**
Project membership was not carried over. Add them under Settings > Team > the person > Projects.

**Symptom: you removed the wrong person.**
Re-invite them. Their content is with the Owner and can be reassigned back, but their seat starts
fresh and their tokens are gone for good.

## Related error codes

- ERR_2044 - seat limit reached because no seat was free.
- ERR_2031 - your role cannot manage seats.

## Related articles

- account-add-team-member, account-remove-member, account-guest-viewer-access.

## If this did not help

Contact support with the workspace name, who left, who is replacing them, and the date. If the
swap produced a charge you did not expect, include both invoice IDs and we will explain each
line or correct it.
