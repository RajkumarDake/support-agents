---
title: Tax, VAT and business details
category: billing
---

# Tax, VAT and business details

Whether tax appears on your invoice depends on your billing country and whether a valid VAT or
GST number is on file at the moment the invoice is issued. The timing matters more than anything
else here: we cannot reissue a past invoice with a number added retroactively.

## Adding a VAT or GST number

1. Open Billing > Business details. Owner and Admin only.
2. Enter the company name, the billing address and the country.
3. Enter the VAT or GST number in full, including the country prefix - `DE123456789`, not
   `123456789`.
4. Save. We validate the number against the relevant registry, which usually takes a few seconds
   and occasionally a minute.
5. Confirm the field shows Validated. A number in the field that has not validated has no effect
   on tax.

Once a valid number is on file, future invoices are issued without VAT where the reverse charge
applies, and the invoice carries the note that the recipient accounts for the tax.

## The retroactive rule

We cannot reissue past invoices with a VAT number added afterwards. The tax treatment is fixed at
the moment the invoice is issued, and reissuing it would misstate a tax position for a period that
has already been reported.

Add your number **before** your next renewal. If you have just missed one, the next invoice will
be correct; the missed one stands. This is the single most common tax question we get, and the
answer does not change with escalation.

## What determines the tax treatment

| Situation | Treatment |
|---|---|
| EU business with a validated VAT number, outside our country of establishment | Reverse charge, no VAT added |
| EU business without a valid number | VAT added at the local rate |
| EU consumer | VAT added at the local rate |
| UK business with a validated VAT number | Reverse charge where applicable |
| US customer | Sales tax where we have nexus, based on the billing address |
| Other regions | GST or none, depending on the billing country |

The billing address, not the card's issuing country, determines the treatment. If the two
disagree, fix the address.

## Company name, address and PO numbers

The company name and address printed on the invoice come from the same screen and can be changed
at any time. A purchase order number can be added there too and appears on subsequent invoices.
Like the VAT number, all of these apply to future invoices, not past ones. See
billing-update-billing-details for the full set of fields and who can change them.

## Edge cases and gotchas

- A number that fails validation is stored but not applied. Check the field says Validated after
  saving.
- Some registries are intermittently unavailable. If validation fails repeatedly and you are sure
  the number is right, contact support with the number and we can validate manually.
- Changing the billing country mid-subscription changes the treatment from the next invoice. It
  does not trigger a correction of earlier ones.
- Tax is calculated on the total after credits. A large account credit can reduce the tax as well
  as the subtotal - see refund-downgrade-credit.
- Refunds are issued inclusive of any tax that was charged, and the credit note reflects that.
- Enterprise customers on wire or ACH terms are invoiced with the same rules; the payment method
  makes no difference to the tax.

## Troubleshooting

**Symptom: VAT was charged despite a number on file.**
Check the field shows Validated, and check the invoice date against the date you saved the
number. Invoices issued before validation carry tax.

**Symptom: the number will not validate.**
Include the country prefix and remove spaces and punctuation. Newly issued numbers can take days
to appear in the registry.

**Symptom: the invoice shows the wrong company name.**
Change it in Billing > Business details. Future invoices pick it up; past ones do not change.

**Symptom: you need a past invoice reissued for your accountant.**
We can re-send a copy of any invoice to any address, but the content is fixed. See
billing-invoice-access.

**Symptom: you were charged US sales tax you believe is exempt.**
Send us your exemption certificate through support. Once on file it applies to future invoices.

## Related articles

- billing-update-billing-details, billing-invoice-access, billing-invoice-dispute,
  billing-cycle, refund-downgrade-credit.

## If this did not help

Contact support with the workspace name, the VAT or GST number, and the invoice ID you are asking
about. If you are asking whether a past invoice can be corrected, expect the answer above - but
send it anyway, because the occasional case genuinely is a mistake on our side.
