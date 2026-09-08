---
title: Exports that are slow or never arrive
category: technical
---

# Exports that are slow or never arrive

Exports run as background jobs, so there is no progress bar to watch and no obvious signal when
something has gone wrong. This article is the diagnosis path for an export that is taking too long
or has apparently vanished. For how to run one in the first place, see tech-data-export.

## What normal looks like

- A records-only export of a small workspace: seconds to a couple of minutes.
- A workspace with more than **500,000 records**: 30-45 minutes.
- Attachments dominate. Including them can multiply the time by ten on an attachment-heavy
  workspace.
- The result is emailed as a **signed download link that expires in 24 hours**.

So an export still running after 20 minutes on a large workspace is not stuck. One still running
after two hours is.

## Diagnosis in order

1. **Check Settings > Export > History.** Every job is listed with a status: queued, running,
   complete or failed. This answers most questions immediately.
2. **If it failed, read the error.** ERR_5108 means the generated archive exceeded the 10 GB
   per-job limit. That is the most common export failure by a wide margin.
3. **If it completed, check spam.** The email carries a link, which some filters strip or
   quarantine. You do not need the email: generate a fresh link from the History screen.
4. **If it is queued and not moving,** check whether another export is already running. Only one
   job per workspace runs at a time; a second request waits.
5. **If it is running and has been for hours,** contact support with the job ID.

## Fixing ERR_5108

The archive exceeded 10 GB. Three remedies, in order of how much they help:

- **Exclude attachments** if you only need the records. This usually shrinks the job by an order
  of magnitude.
- **Narrow the date range** and run several jobs covering consecutive periods.
- **Export project by project** rather than the whole workspace.

The limit is per job, not per day, so several jobs of 8 GB each are entirely acceptable.

## Edge cases and gotchas

- The download link expires in 24 hours, not the archive. Generate a new link from History; the
  job does not need re-running.
- A slow export does not consume workspace storage, so it will not push you toward ERR_5140 - see
  tech-storage-quota.
- Removing the person who started an export cancels the job, see account-remove-member.
- A read-only workspace can still export. Cancellation and unpaid invoices do not take that away,
  see refund-cancellation.
- Very large exports run more slowly during peak hours. If you have a deadline, start overnight.
- If the workspace has a scheduled downgrade, start the export before it lands - see
  account-downgrade-plan.
- Exports are not affected by API rate limits; the job runs on our side, not through the API.

## Troubleshooting

**Symptom: no email, job shows complete.**
Spam filter. Use Settings > Export > History to generate a link directly.

**Symptom: job shows failed with ERR_5108.**
Archive over 10 GB. Narrow it as above.

**Symptom: job shows failed with no code.**
Contact support with the job ID. That is an unexpected failure and worth reporting.

**Symptom: job stuck in queued.**
Another export is running. Wait for it, or cancel the other from History.

**Symptom: the archive downloaded but will not open.**
Check the size against `manifest.json` and re-download. Truncated downloads on poor connections
are the usual cause, not bad archives.

**Symptom: the export is missing recent data.**
The date range excluded it, or the job started before that data was created. Check the parameters
recorded in `manifest.json`.

**Symptom: exports are consistently slow every time.**
Check the record count under Settings > Plan and usage. Above half a million records, 30-45
minutes is expected rather than a fault.

## Related error codes

- ERR_5108 - export archive exceeded the 10 GB per-job limit.
- ERR_2031 - the Viewer role cannot start an export.

## Related articles

- tech-data-export, tech-storage-quota, tech-upload-limits, account-close-workspace,
  tech-service-status.

## If this did not help

Contact support with the workspace name, the export job ID from Settings > Export > History, and
the time you started it. If the export is blocking a deadline such as a migration or a workspace
deletion, say so and we will prioritise it.
