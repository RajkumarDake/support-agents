---
title: Removing a member
category: account
---

# Removing a member

Removing someone ends their access to the workspace and frees the seat they were occupying. It is
the right action when a person leaves the company or moves to another team. It is not reversible
in the sense that matters for billing: re-adding the person later sends a fresh invitation and
starts a new seat.

## Steps

1. Open Settings > Team.
2. Find the person in the list.
3. Click the overflow menu (three dots) at the end of their row.
4. Choose Remove from workspace.
5. Confirm in the dialog. The dialog names the person and shows how many items will be
   reassigned.

Only Owners and Admins can remove. An Admin cannot remove the Owner, and nobody can remove
themselves if they are the Owner - transfer ownership first, see account-transfer-ownership.

## What happens immediately

- Their browser sessions end within a minute. They are signed out of web and mobile.
- Their personal API tokens are revoked immediately. Any script running under their token starts
  returning 401 on the next call.
- They disappear from every project member list in the workspace.
- Content they created stays in the workspace and is reassigned to the Owner. Comments and
  history keep their original author name so the audit trail stays readable.
- The removal is written to the audit log with your name as the actor. See account-audit-logs.

## What happens to the seat and the money

The seat is freed immediately, but you are not refunded in cash. The unused portion shows as a
credit on your following invoice. This is the same mechanic described in
refund-downgrade-credit: credit against future invoices, not money back to the card. If you
remove someone on the last day of a period the credit can round to zero.

If you are replacing the person rather than shrinking the team, remove them and invite the
replacement in the same session - see account-seat-reassignment for why the ordering matters.

## Deactivate versus remove

On Business and Enterprise the overflow menu also offers Deactivate. A deactivated person cannot
sign in, but keeps their project membership and their seat, and is still billed. Use it for
someone on extended leave who will come back. Use Remove when they are gone for good.

## Edge cases and gotchas

- Removing the person who connected an integration does not break the integration. Integrations
  are owned by the workspace. See onboarding-integrations.
- Removing a person does not delete files they uploaded, and does not free storage. If you are
  removing someone to get under a storage limit, that will not work - see tech-storage-quota.
- If SCIM provisioning is enabled, removing someone here is temporary: the next directory sync
  re-creates them. Deprovision in your identity provider instead. See
  account-scim-provisioning.
- Removing the last Admin leaves the workspace with only the Owner, which is allowed but means
  nobody can cover for them.
- Their pending mentions and assigned items are reassigned to the Owner, who will get a burst of
  notifications. Warn the Owner, or mute the digest for a day under Settings > Notifications.

## Troubleshooting

**Symptom: Remove is greyed out.**
You are an Admin trying to remove the Owner, or you are a Member. Check your role at the top of
Settings > Team.

**Symptom: ERR_2031 when removing via the API.**
The token belongs to a role without team management rights. Team management is Owner and Admin
only.

**Symptom: the person can still sign in ten minutes later.**
They are almost certainly hitting a cached page. Ask them to hard reload. If they genuinely
still have write access, check whether SCIM re-created the account, and send support the
timestamp.

**Symptom: the freed seat did not reduce the next invoice.**
Look for a credit line rather than a smaller total. Credits are applied against the following
invoice; on annual plans the credit sits in Billing > Credits until the renewal.

## Related error codes

- ERR_2031 - insufficient permissions to manage team members.

## Related articles

- account-add-team-member - inviting someone new.
- account-seat-reassignment - swapping one person for another cleanly.
- account-roles-permissions - what you are taking away.

## If this did not help

Contact support with the workspace name, the email address of the person, and what you expected
to happen. If this is an urgent offboarding and you need certainty that access is gone, say so -
we can confirm session and token revocation from our side.
