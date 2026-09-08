---
title: Closing or deleting a workspace
category: account
---

# Closing or deleting a workspace

Deleting a workspace removes it, its projects, its files and its members permanently. It is the
most destructive action in the product and it is deliberately slow: there is a 14-day window in
which you can change your mind, and after that nothing can be recovered. If you only want to stop
paying, cancel the subscription instead - see refund-cancellation.

## Cancel or delete: pick the right one

| | Cancel subscription | Delete workspace |
|---|---|---|
| Billing stops | at end of period | at end of period |
| Data kept | yes, read-only | no, purged |
| Reversible | yes, resubscribe any time | only within 14 days |
| Who can do it | Owner | Owner |
| Refund | no, period runs out | no, period runs out |

## Before you delete: export

Once the 14 days pass, backups are purged within 30 days and there is no route back, including
for us. Run a full export first and confirm the archive downloads and opens.

1. Settings > Export > New export.
2. Choose Everything and include attachments.
3. Wait for the email with the signed download link, which expires in 24 hours.
4. Download it and open the archive before you continue.

Large workspaces take 30-45 minutes and can fail with ERR_5108 if the archive would exceed the
10 GB job limit, in which case export in parts. See tech-data-export and tech-export-slow.

Also worth capturing separately: the audit log (account-audit-logs) and your invoices, which are
retained by us for seven years but are easier to keep with your records now
(billing-invoice-access).

## Steps

1. Open Settings > General.
2. Scroll to the Danger zone and click Delete workspace.
3. Read the summary, which lists members, projects, files and storage that will go.
4. Type the workspace name exactly to confirm.
5. Confirm your password, and your second factor if 2FA is enabled.

Only the Owner can do this. Admins do not see the Danger zone at all.

## What happens next

- Deletion is scheduled 14 days out. The exact date is shown on the confirmation screen and
  emailed to the Owner.
- The workspace immediately becomes read-only for everyone. Members can sign in and read, but
  cannot create, edit or upload.
- The subscription is cancelled. You are not charged again, and the current period is not
  refunded - see refund-policy.
- Integrations stop delivering. Webhook endpoints stop receiving events; API tokens keep read
  access until the deletion date, then return 401.
- To cancel the deletion, the Owner signs in during the 14 days and clicks Cancel deletion on the
  banner. Everything returns to normal, but the subscription must be restarted separately.

## Edge cases and gotchas

- Account credit is forfeited when a workspace is closed. Spend it or ignore it - it is not
  refundable and cannot move to another workspace. See refund-downgrade-credit.
- Deleting the workspace does not cancel an Enterprise contract. Contractual terms run to the end
  of the term regardless.
- If a chargeback is open against the workspace, deletion is blocked until the bank closes the
  case, which can take up to 90 days. See billing-dispute-chargeback.
- Deleting does not release the workspace's custom domain immediately; it is freed at the
  deletion date. See tech-custom-domains.
- Members are not emailed automatically. Tell your team before you start the clock.

## Troubleshooting

**Symptom: Delete workspace is missing.**
You are an Admin, not the Owner. Ask the Owner, or transfer ownership first - see
account-transfer-ownership.

**Symptom: the typed confirmation is rejected.**
It matches the workspace name exactly, including case and spacing. Copy it from the top of the
settings page.

**Symptom: you were charged after deleting.**
Deletion cancels at the end of the period, so a charge dated before that boundary is correct. A
charge dated after it is not - send support the invoice ID and it is refunded in full, see
refund-cancellation.

**Symptom: the 14 days have passed and you need the data.**
Contact support the same day. Backups are purged within 30 days of the deletion date, and while
we cannot promise recovery, there is nothing at all to discuss once that window closes.

## Related articles

- refund-cancellation, refund-policy, tech-data-export, account-transfer-ownership,
  billing-invoice-access.

## If this did not help

Contact support with the workspace name and what you are trying to achieve - stop paying, remove
data for a compliance reason, or start again fresh. Those three have different answers and only
one of them needs deletion.
