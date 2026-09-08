---
title: Transferring workspace ownership
category: account
---

# Transferring workspace ownership

Every workspace has exactly one Owner, and the Owner is the only person who can change the plan,
change the payment method, delete the workspace, or configure SSO. When that person changes role
or leaves the company, transfer ownership before they lose access rather than after.

## Before you start

- The person receiving ownership must already be a member of the workspace with the Admin role.
  Raise them to Admin first under Settings > Team, see account-roles-permissions.
- The current Owner must be able to sign in. If they cannot, skip to the recovery section below.
- Have the billing email address to hand; it does not change automatically.

## Steps

1. The current Owner opens Settings > Team.
2. Click the overflow menu next to the Admin who will take over.
3. Choose Transfer ownership.
4. Read the confirmation, which lists what moves, and type the workspace name to confirm.
5. Confirm the second factor if 2FA is enabled on the Owner account.

The transfer is immediate. In the same action the previous Owner is downgraded to Admin - there
is never a moment with two Owners or none.

## What moves and what does not

**Moves to the new Owner:** billing responsibility, the ability to change plan and payment
method, workspace deletion rights, SSO and SCIM configuration, and the 80%-of-limit warning
emails described in account-plan-and-usage.

**Does not move:** the payment method on file, the billing email address, the company name and
VAT number on invoices, existing API tokens, and content ownership. The card that was charged
before is still the card that is charged after. If the old Owner's personal card is on file,
update it under Billing > Payment method - see billing-payment-methods.

## Edge cases and gotchas

- Ownership cannot be transferred to a Member, a Viewer, or someone with a pending invitation.
- Ownership cannot be transferred to an account outside the workspace. Invite them, wait for the
  invitation to be accepted, raise them to Admin, then transfer.
- Transferring does not change who receives invoice emails. Update the billing email under
  Billing > Business details, see billing-update-billing-details.
- If the workspace is past due, transfer still works, but the new Owner inherits the open invoice
  and the grace period already running. See billing-payment-failed.
- The transfer is written to the audit log with both names. See account-audit-logs.
- On Enterprise contracts the named signatory is a contractual matter separate from the product
  role. Changing the Owner in the product does not amend the contract.

## When the Owner has left and cannot sign in

This is the common case and it is handled by support, not self-serve. We will not transfer
ownership on the word of whoever emails first.

1. An existing Admin contacts support from an address on the workspace's verified domain.
2. We verify with the billing contact on file - the person or address that receives invoices.
3. We may ask for confirmation from the domain's administrative contact.
4. Once verified we transfer ownership to the named Admin.

Expect one business day once the verification reply is in. If the workspace has no other Admin
and no reachable billing contact, verification takes longer and may require proof of domain
control.

## Troubleshooting

**Symptom: Transfer ownership does not appear in the menu.**
You are not the Owner, or the person you clicked is not an Admin. Both must be true.

**Symptom: ERR_2031 when calling the transfer endpoint.**
Only an Owner token can transfer. Admin tokens are rejected.

**Symptom: the new Owner cannot see Billing.**
They are looking at a cached page. Reload. If Billing is still missing, confirm in Settings >
Team that their role now reads Owner.

**Symptom: invoices still go to the old Owner.**
Expected - the billing email is separate. Change it under Billing > Business details.

## Related error codes

- ERR_2031 - insufficient permissions; only the Owner can transfer.

## Related articles

- account-roles-permissions, account-remove-member, billing-payment-methods.

## If this did not help

Contact support with the workspace name, the email address of the current Owner, the email
address of the intended new Owner, and whether the current Owner can still sign in. That last
detail decides which of the two paths above applies.
