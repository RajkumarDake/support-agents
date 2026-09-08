---
title: ERR_5012 - upload rejected
category: technical
---

# ERR_5012: upload rejected

ERR_5012 means the upload was rejected by the storage service before it finished. Nothing was
saved, nothing is half-written, and retrying is always safe. There are three causes and they are
worth checking in this order, because the first two need the file or the plan changed and the
third fixes itself on a retry.

## Cause 1: the file is larger than the plan limit

| Plan | Per-file limit |
|---|---|
| Starter | 100 MB |
| Pro | 2 GB |
| Business | 2 GB |
| Enterprise | 10 GB |

Check the file size against your plan under Settings > Plan and usage. If the file is genuinely
too big, either split it, compress it, or raise the plan. There is no per-file override and no
soft margin - a 101 MB file on Starter is rejected. See tech-upload-limits.

## Cause 2: the file type is not on the allow list

Allowed: images, video, audio, PDF, Office documents, CSV, JSON, plain text, and single-level zip
archives.

Rejected: executables of any kind, archives containing other archives, and files with no
extension at all. Renaming an executable does not help; the type is determined from the content,
not the name. Zipping a rejected file type does work, provided the zip is not nested.

## Cause 3: the upload token expired

Upload tokens are valid for **15 minutes**. A paused or resumed upload on a slow connection can
outlive its token, and so can a browser tab left open for an hour before the file was chosen.

Retry the upload from a **fresh page load** so a new token is issued. Simply clicking retry on
the old page reuses the expired token and fails identically.

For files over 500 MB the transfer automatically switches to a chunked, resumable mode. Keep the
tab in the foreground while it runs - browsers throttle background tabs, which slows the transfer
enough to outlive the token.

## Known incident: uploads in eu-west-1

A storage node in eu-west-1 is returning intermittent rejections on uploads over 50 MB, affecting
roughly 3% of uploads in that region. This is incident **INC-2291**, currently at status
monitoring, started 2026-09-07.

Retrying from a fresh page load usually succeeds. Files under 50 MB are unaffected. If your
uploads are failing intermittently rather than consistently, and the file is well within your
plan limit and of an allowed type, this is very likely what you are hitting rather than any of
the three causes above. See tech-service-status.

## Diagnosis in order

1. Is the file within the plan limit? If not, cause 1.
2. Is the type allowed? If not, cause 2.
3. Does it fail every single time, immediately? Likely cause 1 or 2 - re-check.
4. Does it fail sometimes, or after a long wait? Cause 3, or INC-2291.
5. Does a small text file upload successfully in the same session? If yes, the problem is the
   file. If no, the problem is the session or the workspace.

## Edge cases and gotchas

- ERR_5012 is not a storage quota error. If the workspace is out of total storage you get
  ERR_5140 instead, see tech-storage-quota.
- Mobile uploads on a cellular connection hit cause 3 far more often than desktop ones, see
  onboarding-mobile-app.
- A workspace in read-only mode after an unpaid invoice rejects uploads with a permissions error,
  not ERR_5012 - see billing-payment-failed.
- Viewers cannot upload at all; that is ERR_2031, see account-guest-viewer-access.
- An import file that fails to upload raises ERR_5012 before the importer ever sees it, which is
  different from the importer rejecting the contents with ERR_3007. See onboarding-import-data.

## Troubleshooting

**Symptom: fails instantly, every time, for one file only.**
Size or type. Check both against the lists above.

**Symptom: fails after several minutes on a large file.**
Token expiry. Fresh page load, foreground tab, wired or Wi-Fi connection if possible.

**Symptom: fails intermittently on files over 50 MB.**
INC-2291. Retry from a fresh page load.

**Symptom: all uploads fail regardless of file.**
Check whether the workspace is read-only or over its storage quota, and check
tech-service-status.

**Symptom: it worked yesterday and not today.**
Check whether the plan changed. A downgrade drops the per-file limit at the moment it lands, see
account-downgrade-plan.

## What to send support

If it still fails, send us the **file name, size, type, and the timestamp of the attempt**, plus
the workspace name. With those we can find the exact rejection in the storage log and tell you
which of the causes applied.

## Related error codes

- ERR_5012 - upload rejected by storage.
- ERR_5140 - workspace storage quota exhausted.
- ERR_5108 - export archive too large, the same family but a different job.

## Related articles

- tech-upload-limits, tech-storage-quota, tech-service-status, onboarding-import-data,
  tech-error-codes-overview.

## If this did not help

Contact support with the file name, size, type and timestamp. Uploads leave a clear trace on our
side, so this is one of the faster things for us to diagnose.
