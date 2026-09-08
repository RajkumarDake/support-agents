---
title: Workspace storage quota and ERR_5140
category: technical
---

# Workspace storage quota and ERR_5140

Every workspace has a total storage limit. When it is reached, new writes to storage are rejected
with ERR_5140 - uploads, attachments, new file versions and the attachment portion of an import.
Nothing existing is deleted, and everything already stored stays readable.

This is different from the per-file limit, which rejects a single oversized file with ERR_5012.
See tech-upload-limits.

## The limits

| Plan | Total workspace storage |
|---|---|
| Starter | 10 GB |
| Pro | 250 GB |
| Business | 1 TB |
| Enterprise | custom, typically 5 TB |

Storage is a standing total, not a per-period allowance. It does not reset at the start of a
billing period the way API calls do - it goes down only when you delete something. See
billing-cycle.

## Checking usage

Settings > Plan and usage shows storage consumed against the limit, updated within a few minutes
of a change. At 80% we email the Owner; at 100% the soft cap applies and writes to storage stop.

The breakdown by project is on the same screen under Storage details, which is where you find the
one project holding most of it.

## Freeing space

1. Find the largest attachments. Settings > Plan and usage > Storage details sorts by size.
2. Delete what you do not need.
3. **Empty the trash.** Deleted files continue to occupy storage until the trash is emptied -
   Settings > General > Trash > Empty trash. This is the step people miss, and until it is done
   the usage figure does not move at all.
4. Consider old file versions. Every version of a file counts separately; ten versions of a
   100 MB file is 1 GB. Prune versions from the file's history panel.
5. Export and remove archival material you must keep but do not need live - see
   tech-data-export.

Space is reclaimed within a few minutes of emptying the trash.

## Raising the limit

If the usage is legitimate, raise the plan under Settings > Plan. Upgrades take effect
immediately and are prorated, so the space is available at once - see billing-proration. There is
no storage-only add-on below Enterprise; on Enterprise, additional storage is negotiated in the
contract.

## Edge cases and gotchas

- Removing a member does not free storage. Their files stay and are reassigned to the Owner. See
  account-remove-member.
- A downgrade that puts you over the new limit does not delete anything. The workspace sits
  soft-capped, readable but unable to accept new files, until you are back under. See
  account-downgrade-plan.
- An import that runs out of storage partway fails the remaining rows with ERR_5140. The rows
  already written stay. See onboarding-import-data.
- Exports do not consume workspace storage; the archive is held separately and expires with its
  download link.
- The audit log and invoices do not count toward storage.
- Trash is emptied automatically after 30 days, so a workspace can free space on its own - but
  not on a schedule you can rely on when you need space now.

## Troubleshooting

**Symptom: ERR_5140 on every upload.**
The workspace is at 100% of its storage limit. Free space or raise the plan.

**Symptom: you deleted a lot and usage has not moved.**
The trash has not been emptied. This is by far the most common cause.

**Symptom: usage is higher than the sum of the files you can see.**
File versions, and attachments inside projects you are not a member of. An Owner or Admin sees
the full picture in Storage details.

**Symptom: ERR_5012 rather than ERR_5140.**
That is the individual file being too large or the wrong type, not the workspace being full. See
tech-err-5012-upload.

**Symptom: usage went up with no new uploads.**
Check integrations that sync attachments in, and check whether someone imported. Both are visible
in the audit log, see account-audit-logs.

**Symptom: an export failed with ERR_5108 while you were trying to clear space.**
That is the export archive exceeding the 10 GB per-job limit, a separate limit. Narrow the range
and export in parts - see tech-export-slow.

## Related error codes

- ERR_5140 - storage quota exhausted, new writes to storage rejected.
- ERR_5012 - individual upload rejected.
- ERR_5108 - export archive too large.

## Related articles

- tech-upload-limits, tech-err-5012-upload, account-plan-and-usage.

## If this did not help

Contact support with the workspace name and the figure shown under Settings > Plan and usage. If
the number looks wrong to you, say what total you expect - we can produce a breakdown by project
and by file version that the UI does not show.
