---
title: File size and type limits
category: technical
---

# File size and type limits

Two different limits apply to every file you add: the size of the individual file, and the total
storage the workspace has used. Both depend on the plan, and hitting each one produces a different
error. This article covers the per-file rules; tech-storage-quota covers the workspace total.

## Per-file limits

| Plan | Per file | Total workspace storage |
|---|---|---|
| Starter | 100 MB | 10 GB |
| Pro | 2 GB | 250 GB |
| Business | 2 GB | 1 TB |
| Enterprise | 10 GB | custom, typically 5 TB |

There is no soft margin. A 101 MB file on Starter is rejected with ERR_5012, and there is no
per-file override available on request.

A separate limit applies to imports: 200 MB per CSV or JSON file, on every plan, regardless of
the attachment limit above. See onboarding-import-data.

## Allowed file types

**Allowed:** images (JPEG, PNG, GIF, WebP, HEIC, SVG), video (MP4, MOV, WebM), audio (MP3, WAV,
M4A), PDF, Office documents (Word, Excel, PowerPoint and their OpenDocument equivalents), CSV,
JSON, plain text, Markdown, and single-level zip archives.

**Rejected:** executables and installers of any platform, scripts with an executable bit,
archives that contain other archives, disk images, and files with no extension at all.

The type is determined from the file's content, not from its name, so renaming does not get past
the check. Zipping a rejected file does work, provided the resulting zip does not itself contain
another archive.

## Large uploads

Uploads over **500 MB** automatically switch to a chunked, resumable transfer. Individual chunks
are retried on failure, so a brief network interruption does not restart the whole file.

Two things still matter:

- The upload token is valid for **15 minutes**. A transfer slow enough to outlive it fails with
  ERR_5012 and must be restarted from a fresh page load.
- Browsers throttle background tabs. Keep the tab in the foreground for the duration of a large
  upload, or the throttling can slow it below the token window.

## Edge cases and gotchas

- Deleted files still count toward workspace storage until the trash is emptied.
- File versions count separately. Ten versions of a 100 MB file consume 1 GB.
- The per-file limit drops immediately when a plan downgrade lands, so a file that uploaded fine
  last month may be rejected this month. Existing files are never removed. See
  account-downgrade-plan.
- Viewers cannot upload at all - that is ERR_2031, not a size problem. See
  account-guest-viewer-access.
- A workspace in read-only mode after an unpaid invoice rejects uploads regardless of size, see
  billing-payment-failed.
- Mobile uploads are subject to exactly the same limits, and hit the token window far more often
  on cellular connections. See onboarding-mobile-app.

## Troubleshooting

**Symptom: ERR_5012 immediately on a large file.**
Over the per-file limit. Check the plan row above.

**Symptom: ERR_5012 on a small file.**
Type. Check whether it is an executable, a nested archive, or has no extension.

**Symptom: ERR_5012 partway through a big upload.**
Token expiry. Fresh page load, foreground tab. Full diagnosis in tech-err-5012-upload.

**Symptom: ERR_5140 rather than ERR_5012.**
That is the workspace total, not the file. Free space or raise the plan, see tech-storage-quota.

**Symptom: intermittent failures on files over 50 MB.**
Possibly incident INC-2291, which affects a small proportion of uploads in eu-west-1. Retry from
a fresh page load, see tech-service-status.

**Symptom: a file uploaded but will not preview.**
Previews are generated for common types only and are capped at 100 MB regardless of plan. The
file itself is intact and downloadable.

## Related error codes

- ERR_5012 - upload rejected: size, type or expired token.
- ERR_5140 - workspace storage quota exhausted.
- ERR_5108 - export archive over the 10 GB job limit.

## Related articles

- tech-err-5012-upload, tech-storage-quota, onboarding-import-data.

## If this did not help

Contact support with the file name, its exact size in bytes, its type, and the workspace name.
If you need a limit raised, tell us the largest file you realistically need to store - the answer
is usually a plan change rather than an exception.
