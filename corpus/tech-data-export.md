---
title: Exporting your data
category: technical
---

# Exporting your data

You can export everything in a workspace at any time, on any plan, without asking us. Exports run
as background jobs and arrive as a downloadable archive. This article covers running one and what
you get; tech-export-slow covers what to do when one is slow or never arrives.

## Running an export

1. Open Settings > Export.
2. Click New export.
3. Choose the scope: the whole workspace, or specific projects.
4. Choose a date range, or leave it as everything.
5. Choose whether to include attachments. Excluding them makes the job dramatically smaller and
   faster if you only need the records.
6. Choose the format: JSON (complete, machine-readable) or CSV (one file per record type, easier
   for spreadsheets).
7. Start. You can close the tab.

Members and above can export. Viewers cannot, and get ERR_2031 - see
account-guest-viewer-access.

## What you get

An archive containing:

- Records in the chosen format, one file per type.
- Attachments in their original formats, in a folder structure mirroring the projects, if you
  included them.
- Comments and item history.
- A `manifest.json` listing every file, its size and a checksum, plus the export parameters and
  the time it ran.

What is **not** included: invoices (download those from Billing > Invoices, see
billing-invoice-access), the audit log (export separately from Settings > Audit log, see
account-audit-logs), and workspace settings such as integrations and webhook configuration.

## Getting the archive

The archive is emailed as a **signed download link that expires in 24 hours**. It is also listed
under Settings > Export > History, where you can generate a fresh link if the first expires.

The link is signed but not authenticated - anyone with the URL can download it within its window.
Treat it as sensitive and do not forward the email outside your organisation.

## Timing

A workspace with more than **500,000 records** can take 30-45 minutes. Attachments are usually the
dominant factor: a records-only export of the same workspace typically finishes in a few minutes.
You get an email when it completes.

## Limits

The generated archive cannot exceed **10 GB per job**. Beyond that the job fails with ERR_5108.
The remedies are to narrow the date range, export project by project, or exclude attachments and
export those separately in parts. See tech-export-slow.

Exports do not consume workspace storage - the archive is held separately and expires with its
link. So exporting is a safe thing to do when you are near a storage limit, see
tech-storage-quota.

## Edge cases and gotchas

- Export before deleting a workspace. After the 14-day deletion window, backups are purged within
  30 days and nothing can be recovered - see account-close-workspace.
- A read-only workspace, after cancellation or an unpaid invoice, can still export. That is
  deliberate: you never lose the ability to take your data out - see refund-cancellation.
- A downgrade applies the new plan's limits to exports started after it lands. Start large exports
  before a scheduled downgrade, see account-downgrade-plan.
- Only one export job per workspace runs at a time. A second request queues behind the first.
- Export jobs and downloads are written to the audit log with the actor, which is what an auditor
  will ask about.
- Exports cannot be started from the mobile app, see onboarding-mobile-app.
- Removing a member cancels any export job they had running, see account-remove-member.

## Troubleshooting

**Symptom: ERR_5108.**
The archive would exceed 10 GB. Narrow the range, exclude attachments, or export in parts.

**Symptom: no email after an hour.**
Check spam, then Settings > Export > History for the job status. See tech-export-slow.

**Symptom: the link says expired.**
Generate a new one from Settings > Export > History.

**Symptom: ERR_2031 starting an export.**
You are a Viewer. Ask a Member or above to run it.

**Symptom: the archive is missing attachments.**
Include attachments was not ticked, or they were excluded to stay under the size limit. Check
`manifest.json`, which records the parameters used.

**Symptom: the download is corrupt.**
Compare against the checksums in `manifest.json`. A truncated download on a poor connection is
far more common than a bad archive.

## Related error codes

- ERR_5108 - export archive exceeded the 10 GB per-job limit.
- ERR_2031 - the Viewer role cannot export.

## Related articles

- tech-export-slow, tech-storage-quota, account-close-workspace.

## If this did not help

Contact support with the workspace name and the export job ID from Settings > Export > History.
If you are exporting because you are leaving, say so - we will make sure the archive is complete
before anything is deleted.
