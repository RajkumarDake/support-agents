---
title: Your first week
category: onboarding
---

# Your first week

A workspace that is set up properly in the first week rarely needs support later. This is the
order we recommend, based on what actually goes wrong when people skip steps. Nothing here takes
more than an hour, and most of it takes minutes.

## Day 1 - the workspace and the people

1. Create the workspace and set its name under Settings > General. This name appears on invoices
   until you set a company name, so make it the real one.
2. Set Billing > Business details: company name, address, VAT or GST number and a shared billing
   email. Do this **before** your first renewal - a VAT number added later cannot be applied
   retroactively, see billing-tax-vat.
3. Invite your team from Settings > Team > Invite member. Add people to projects as you invite
   them so their first screen is not empty. See account-add-team-member.
4. If you use an identity provider, connect it now: Settings > Security > SSO. Doing it after
   people have passwords means two sign-in methods and confusion. See tech-sso-saml, and
   account-scim-provisioning if you also want automatic joiner and leaver handling.

## Day 2-3 - your data

Import existing data with the CSV importer under Settings > Import, or through the API. The
importer validates the whole file before writing anything, so a failed import changes nothing and
is safe to retry.

Most teams are productive right after the import step, so it is worth doing properly. If an
import stalls, it is nearly always a CSV with inconsistent columns - the importer reports the
offending row number and raises ERR_3007. See onboarding-import-data.

For large data sets, check the per-file limit for your plan first: 200 MB per import file, and
100 MB per attachment on Starter against 2 GB on Pro and Business. See tech-upload-limits.

## Day 4-5 - integrations and noise

1. Connect only the integrations you will actually use, from Settings > Integrations. Each one
   asks for the scopes it needs and can be revoked from the same screen. See
   onboarding-integrations.
2. Turn off the notifications you do not want, before your team decides the product is noisy. Set
   the workspace default under Settings > Notifications and let people adjust their own - see
   onboarding-notifications.
3. If you are building against the API, create a token now and read the rate limits before you
   write a polling loop. See tech-api-keys and tech-api-rate-limits.

## Day 6-7 - the boring, important bits

- Turn on two-factor authentication for yourself, and consider requiring it for the workspace on
  Business and Enterprise. Store the recovery codes somewhere outside the workspace - see
  account-two-factor.
- Confirm someone other than you is an Admin, so a single locked-out account does not stop the
  team. See account-roles-permissions.
- Run one export and check that the archive opens. Knowing the export works is worth more than
  hoping it does - see tech-data-export.
- Check Settings > Plan and usage so you know where your limits are before you hit one, see
  account-plan-and-usage.

## Common first-week mistakes

- Inviting everyone before creating any projects, so twenty people land on an empty screen.
- Adding the VAT number after the first invoice.
- Using a personal card that expires during the year, with no backup card - see
  billing-payment-methods.
- Setting the billing email to the founder rather than a shared finance address, so payment
  failure notices go unread until the workspace goes read-only, see billing-payment-failed.
- Inviting read-only stakeholders as Members on Business, where Viewers are free - see
  account-guest-viewer-access.

## Troubleshooting

**Symptom: nobody accepted their invitation.**
Invitations last 7 days and often land in corporate spam filters. Resend from Settings > Team, or
copy the invitation link and send it yourself.

**Symptom: the import failed with ERR_3007.**
Duplicate or empty column headers, or a date that is not ISO 8601. Nothing was written; fix and
re-upload.

**Symptom: an upload was rejected with ERR_5012.**
The file is over the plan limit, the type is not allowed, or the upload token expired. See
tech-err-5012-upload.

**Symptom: the team says they are drowning in email.**
Set the digest default to daily or weekly under Settings > Notifications.

## Related articles

- onboarding-invite-flow, onboarding-import-data, onboarding-integrations.

## If this did not help

Contact support with the workspace name and where you got stuck. Setup questions in the first
fortnight are answered quickly, and if you are on Business or Enterprise we can walk through it
with you live.
