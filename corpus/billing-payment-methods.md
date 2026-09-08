---
title: Supported payment methods
category: billing
---

# Supported payment methods

This article lists what we accept, what we do not, how to change the card on file, and the rules
that decide which methods are available to your plan and region.

## What we accept

| Method | Available on | Notes |
|---|---|---|
| Visa | All plans | Credit and debit |
| Mastercard | All plans | Credit and debit |
| American Express | All plans | Credit and debit |
| SEPA direct debit | EU customers, annual plans only | Mandate signed at setup |
| ACH | Enterprise contracts over $12,000/year | Invoice terms, net 30 |
| Wire transfer | Enterprise contracts over $12,000/year | Invoice terms, net 30 |

## What we do not accept

PayPal, prepaid and gift cards, virtual single-use cards that expire before the next renewal,
cryptocurrency, and cheques. Attempting to save one of these returns ERR_3112. Prepaid cards in
particular often authorise once and then fail on renewal, which is why they are blocked at the
point of entry rather than at the first charge.

## Adding or changing a card

1. Open Billing > Payment method. Owner only - see account-roles-permissions.
2. Click Add payment method, or Replace on the existing card.
3. Enter the card details. Your bank may show a 3-D Secure challenge; complete it in the window.
4. Save. If an invoice is outstanding, it is retried immediately.

The card details never touch our servers. They are tokenised by the payment processor, and we
store only the brand, the last four digits and the expiry so we can show them back to you.

## Primary and backup

Only one method can be primary. Add a second card as backup and we try it automatically if the
primary declines, before the retry schedule in billing-payment-failed starts. This is the single
most effective thing you can do to avoid an interruption, and it costs nothing.

To swap them, use the overflow menu on the card you want and choose Make primary.

## Region and currency

Invoices are issued in USD by default. EU customers with a valid VAT number on file are invoiced
without VAT where reverse charge applies - see billing-tax-vat. Your bank may apply its own
conversion and a foreign transaction fee, which is why the amount on your statement can differ
slightly from the invoice total; the invoice amount is the authoritative one.

## Edge cases and gotchas

- SEPA is annual-only. Switching from annual to monthly means moving to a card first.
- ACH and wire are set up by our billing team as part of an Enterprise contract, not self-serve.
  Ask your account contact.
- Removing the only payment method is blocked while a subscription is active. Add the replacement
  first, then remove the old one.
- Changing the card does not change the billing email, the company name, or the VAT number. Those
  live in Billing > Business details, see billing-update-billing-details.
- Transferring workspace ownership does not change the card on file. The old Owner's personal
  card keeps being charged until someone replaces it, see account-transfer-ownership.
- Payment method changes are written to the audit log, see account-audit-logs.

## Troubleshooting

**Symptom: ERR_3112 when saving a card.**
Either the card was declined at the zero-amount authorisation, or the type is not on the accepted
list. Try a different card. Ask your bank whether recurring international payments are blocked -
that block is invisible to us and reads as a generic decline.

**Symptom: the 3-D Secure window does not appear.**
A popup blocker. Allow popups for our domain and retry, or use an incognito window - see
tech-browser-support.

**Symptom: the card saves but the invoice stays `open`.**
Wait a minute and reload. If it is still open, the retry hit a second decline; check
billing-payment-failed.

**Symptom: you want to pay one invoice with a different card than the subscription uses.**
Not supported self-serve. Change the primary card, let the invoice retry, then change it back.

**Symptom: SEPA is not offered.**
The plan is monthly, or the billing country on file is outside the SEPA area. Both must be right.

## Related error codes

- ERR_3112 - payment method rejected or unsupported.

## Related articles

- billing-payment-failed, billing-cycle, billing-tax-vat, billing-update-billing-details,
  billing-dispute-chargeback.

## If this did not help

Contact support with the workspace name, the last four digits of the card, and the exact message
shown when you tried to save it. If you need ACH or wire terms, say what your annual spend is so
we can tell you immediately whether you qualify.
