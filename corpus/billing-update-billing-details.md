---
title: Updating billing contacts and invoice details
category: billing
---

# Updating billing contacts and invoice details

Billing > Business details controls everything printed on your invoices and everyone who receives
them. It is separate from the payment method and separate from the workspace Owner, which is why
invoices keep going to the wrong person long after the team has changed.

## The fields

| Field | Appears on invoice | Notes |
|---|---|---|
| Company name | Yes | Legal entity name, not the workspace name |
| Billing address | Yes | Determines tax treatment |
| Billing country | Yes | Card issuing country is ignored |
| VAT or GST number | Yes | Must validate to have any effect |
| Purchase order number | Yes | Free text, carried onto every future invoice |
| Billing email | No | Receives every invoice and every payment notice |
| Additional recipients | No | Up to five extra addresses |

## Changing them

1. Open Billing > Business details. Owner and Admin only - see account-roles-permissions.
2. Edit the fields you need.
3. Save. Changes apply to invoices issued from that moment onward.

Everything on this screen is forward-looking. Past invoices are never rewritten, for the reasons
set out in billing-tax-vat.

## The billing email

The billing email is the address that receives invoices, payment failure notices, renewal
warnings for annual plans, and the 80%-of-limit usage alerts. It does not need to be a member of
the workspace, is not billed, and does not get any access. Use a shared finance address rather
than a person - `accounts@` outlives whoever set the workspace up.

Add up to five additional recipients on the same screen if more than one team needs a copy.

## What this screen does not change

- **The payment method.** That is Billing > Payment method, and it is Owner only. See
  billing-payment-methods.
- **The workspace Owner.** Transferring ownership does not move the billing email, and changing
  the billing email does not change who can alter the plan. See account-transfer-ownership.
- **Past invoices.** See billing-invoice-access to re-send a copy of an old invoice to a new
  address - the copy carries the details that were correct at the time.
- **The workspace name.** That is Settings > General.

## Edge cases and gotchas

- Adding a VAT number here does not retroactively remove tax from the invoice you just received.
  Add it before the next renewal.
- A purchase order number added mid-period appears on the next invoice, not on any open one.
- If your finance system requires the PO number on the invoice you are about to be charged for,
  set it at least one full day before the renewal date in billing-cycle.
- Changing the billing country changes the tax treatment from the next invoice, and can change
  whether SEPA is available.
- Changes here are written to the audit log, so you can see who changed a billing address and
  when. See account-audit-logs.
- Deleting the workspace does not stop invoice archive access while anyone can still sign in, but
  after deletion the addresses on this screen receive nothing further.

## Troubleshooting

**Symptom: invoices still go to the previous Owner.**
The billing email was never changed. It does not follow ownership transfers.

**Symptom: nobody received the payment failure emails.**
Check the billing email and the additional recipients, then check spam. Payment notices go to the
Owner and the billing email; if those are the same absent person, nothing gets through. See
billing-payment-failed.

**Symptom: the company name on the invoice is the workspace name.**
No company name has been set, so we fall back to the workspace name. Set it explicitly.

**Symptom: saving fails with a validation error on the VAT number.**
The number is stored only if it parses. Include the country prefix; see billing-tax-vat.

**Symptom: ERR_2031 opening the screen.**
You are a Member or Viewer. Billing is Owner and Admin only.

## Related error codes

- ERR_2031 - insufficient permissions for billing screens.

## Related articles

- billing-tax-vat, billing-invoice-access, billing-payment-methods, billing-cycle,
  account-transfer-ownership, billing-invoice-dispute.

## If this did not help

Contact support with the workspace name, the field you need changed, and the value it should be.
If you need a past invoice re-sent to a new finance address, include the invoice IDs and we will
send them all at once.
