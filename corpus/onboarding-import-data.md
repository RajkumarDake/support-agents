---
title: Importing your data
category: onboarding
---

# Importing your data

The importer brings existing records into a workspace from CSV or JSON. It is deliberately
all-or-nothing: the whole file is validated before anything is written, so a failed import changes
nothing and is always safe to retry.

## Steps

1. Open Settings > Import.
2. Choose the target project. Everything in the file lands there.
3. Upload the file. CSV and JSON are accepted, up to 200 MB per file.
4. Map the columns to fields. We suggest a mapping from the headers; check it rather than
   trusting it.
5. Click Validate. This reads the whole file and reports problems without writing.
6. Click Import. Small files finish in seconds. Large ones run in the background and email you
   when they are done.

Members and above can import. Viewers cannot - see account-roles-permissions.

## File requirements

- **Format:** CSV (comma-separated, UTF-8) or JSON array of objects.
- **Size:** 200 MB per file. Split larger data sets and import in parts.
- **Headers:** every column header must be unique and non-empty. This is the single most common
  failure.
- **Dates:** parsed as ISO 8601. `2026-09-08` works; `08/09/2026` does not, because it is
  ambiguous and we will not guess.
- **Encoding:** UTF-8. A file saved as Latin-1 imports mangled characters rather than failing, so
  check a sample row afterwards.
- **Line endings:** either style works.

## Validation and ERR_3007

If validation fails you get ERR_3007 with the row number that caused it. The usual causes:

- Two columns with the same header, often `Name` and `name`.
- A trailing comma in the header row creating an empty column.
- A date in a local format.
- A file exported from a spreadsheet with a title row above the real headers.

Fix the source file and re-upload. Nothing was written, so there is nothing to clean up.

## Large imports

Imports over roughly 50,000 rows run in the background. You can close the tab. You get an email
when it finishes, with a summary of rows created and rows skipped.

Check Settings > Plan and usage before a large import: attachments referenced by the import count
against workspace storage, and hitting the limit mid-import fails the remaining rows with
ERR_5140. Starter workspaces have 10 GB, Pro 250 GB, Business 1 TB. See tech-storage-quota.

## Importing through the API

The API accepts the same records in batches, which is the better route for a recurring sync. It
is subject to the ordinary rate limits - 60 requests per minute on Starter, 600 on Pro and
Business - so batch your writes rather than sending a row per request. See tech-api-rate-limits
and tech-api-keys.

## Edge cases and gotchas

- The importer does not deduplicate. Importing the same file twice creates everything twice.
  There is no undo; delete the duplicates or restore from an export.
- Column mapping is not remembered between imports. Re-check it each time.
- Empty cells create empty fields rather than being skipped.
- Very wide files (hundreds of columns) validate slowly. Trim to the columns you need.
- Imported items are attributed to you, not to their original authors.
- The import is written to the audit log with the file name and row count, see
  account-audit-logs.

## Troubleshooting

**Symptom: ERR_3007 with a row number.**
Open that row in the source file. Duplicate or empty column headers, or a non-ISO date. Nothing
was written.

**Symptom: the upload of the file itself fails with ERR_5012.**
That is the upload, not the import. The file is over 200 MB, the type is not allowed, or the
15-minute upload token expired. See tech-err-5012-upload.

**Symptom: the import ran but the numbers are wrong.**
Check for a skipped-rows count in the completion email, and check whether the file had a title
row that became the header.

**Symptom: characters are mangled.**
The file is not UTF-8. Re-export it as UTF-8 and import again into a fresh project.

**Symptom: no completion email.**
Check spam, and check the address on your profile. The job itself is visible under Settings >
Import > History.

## Related error codes

- ERR_3007 - import validation failed, with a row number.
- ERR_5012 - the file upload was rejected before the import began.
- ERR_5140 - storage quota exhausted mid-import.

## Related articles

- onboarding-first-week, tech-upload-limits, tech-storage-quota.

## If this did not help

Contact support with the workspace name, the row number from ERR_3007, and the header row of your
file. Those three almost always identify the problem without us needing the data itself.
