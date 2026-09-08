---
title: Finding and downloading invoices
category: billing
---

# Finding and downloading invoices

Every charge produces an invoice, and every invoice is available as a PDF for as long as you need
it. This article covers where they live, who can see them, what each status means, and how to get
one to your finance team without giving them access to the workspace.

## Where invoices live

Billing > Invoices lists every invoice for the workspace, newest first. Each row shows:

- The invoice ID, in the form `INV-NNNN`. Quote this when you contact support about anything
  billing related.
- The date the charge was captured.
- The period the invoice covers.
- The amount and currency.
- The payment method used, shown as the type and last four digits.
- The status.

Click a row to open the invoice, and use Download PDF for a copy. Download all as CSV at the top
of the list exports the whole history for your accounting system.

## Invoice statuses

| Status | Meaning | What to do |
|---|---|---|
| `paid` | Captured successfully | Nothing |
| `open` | Raised, not yet paid, retries in progress | Check the card, see billing-payment-failed |
| `failed` | All retries exhausted | Update the payment method; the invoice retries at once |
| `refunded` | Money returned to the original method | See refund-timeline |

A credit note is issued alongside a refund and appears as its own document on the same row.

## Who can see them

Owners and Admins only. Members and Viewers do not see Billing at all and an API call for the
invoice list from their token returns ERR_2031. This is deliberate and cannot be changed per
person - see account-roles-permissions.

To get invoices to someone without workspace access, set the billing email under Billing >
Business details. Every invoice is emailed there automatically, and you can re-send any past
invoice to it from the invoice's own page. That address does not need to be a member and is not
billed.

## Getting the details right

The company name, address and VAT or GST number printed on the invoice come from Billing >
Business details. Fix them before your next renewal: we cannot reissue a past invoice with a VAT
number added retroactively. See billing-tax-vat and billing-update-billing-details.

A purchase order number can be added to the same screen and appears on subsequent invoices.

## Edge cases and gotchas

- Invoices are retained for seven years and remain downloadable after cancellation, provided
  someone can still sign in. Export them before deleting the workspace - see
  account-close-workspace.
- The invoice date is the capture date, which can differ from the renewal date by a few hours
  across a time zone boundary. See billing-cycle.
- A `Plan change adjustment` line is proration from an upgrade or a seat change, not a second
  charge. See billing-proration.
- Account credit is applied automatically and shows as a negative line, so a small invoice after a
  downgrade is normal - see refund-downgrade-credit.
- Two `paid` invoices for the same amount on the same date is a real duplicate, not a display
  problem. See billing-duplicate-charge.
- Enterprise customers invoiced by wire see the invoice here with status `open` until the
  transfer clears, which can take several days.

## Troubleshooting

**Symptom: Billing is missing from the menu.**
You are a Member or Viewer. Ask an Owner or Admin, or have your role raised.

**Symptom: ERR_2031 downloading an invoice through the API.**
Same cause. Invoices are Owner and Admin only.

**Symptom: the PDF will not open.**
Check whether the browser downloaded an HTML error page instead, which happens when the session
expired mid-download. Sign in again and retry - see account-session-timeout.

**Symptom: an invoice is missing from the list.**
Confirm you are in the right workspace; the list is workspace-scoped. If the charge is on your
statement but no invoice exists here, send support the statement descriptor and amount.

**Symptom: the charge on the bank statement does not match any invoice amount.**
Currency conversion by your bank, or two invoices settled together. Compare the total for the
day.

## Related error codes

- ERR_2031 - insufficient permissions; invoices are Owner and Admin only.

## Related articles

- billing-cycle, billing-tax-vat, billing-update-billing-details.

## If this did not help

Contact support with the workspace name and the invoice ID, or with the date and amount if you
cannot find the invoice at all. We can re-send any invoice to any address you nominate.
