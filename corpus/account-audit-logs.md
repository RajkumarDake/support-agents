---
title: Audit logs
category: account
---

# Audit logs

The audit log is the immutable record of administrative actions in a workspace: who invited whom,
who changed a role, who connected an integration, who exported data, who changed the plan. It is
what you reach for during a security review, a compliance questionnaire, or an argument about who
deleted something.

Audit logs are available on Business and Enterprise. Starter and Pro workspaces do not have the
screen, and the export endpoint returns ERR_2031 for them.

## Reading the log

1. Open Settings > Audit log. Owners and Admins only.
2. Filter by actor, action type, or date range. The default view is the last 7 days.
3. Click a row to expand it. Each entry shows the timestamp in UTC, the actor, the action, the
   target, the source IP, and the client - web, mobile or API.

Entries appear within a minute of the action. They cannot be edited or deleted by anyone,
including us, and including the Owner.

## What is recorded

- Sign-in successes and failures, including the error code on failure.
- Sessions ended by policy or by Sign out everywhere (account-session-timeout).
- Invitations sent, accepted, revoked and expired.
- Role changes, deactivations and removals.
- Two-factor enrolment, reset and enforcement changes (account-two-factor).
- SSO and SCIM configuration changes (tech-sso-saml, account-scim-provisioning).
- API token creation and revocation (tech-api-keys).
- Integration connection and disconnection, webhook endpoint changes (tech-webhooks).
- Plan changes, payment method changes and workspace deletion scheduling.
- Export jobs started and downloaded (tech-data-export).
- Every error code raised by an admin action, which is why support asks for a code and a
  timestamp - see tech-error-codes-overview.

## What is not recorded

Content-level activity is not in the audit log. Editing a document, commenting, or moving an item
between projects lives in that item's own history, not here. If you need content history for a
compliance answer, say so - it is a different export.

## Exporting

Settings > Audit log > Export produces a CSV or JSON Lines file for the selected range.
Enterprise workspaces can also stream events to an external SIEM over a webhook; configure it
under Settings > Security > Audit streaming, and note that it uses the same delivery, retry and
signature rules as ordinary webhooks.

Retention is 1 year on Business and 3 years on Enterprise. Export before the window closes if you
need longer - once an entry ages out it is gone.

## Edge cases and gotchas

- Timestamps are UTC in the export and in your local time zone in the UI. Comparing the two
  without converting is the most common source of confusion.
- Actions taken by support staff on your behalf appear with a `support` actor and a ticket
  reference. You can see everything we did.
- Actions performed by an API token show the token name as the actor, not the person who created
  it. Name tokens after their purpose so the log stays readable.
- Downgrading from Business to Starter or Pro hides the screen immediately and stops new entries
  being written. Export first - see account-downgrade-plan.
- The log is workspace-scoped. There is no cross-workspace view.

## Troubleshooting

**Symptom: Settings > Audit log is not in the menu.**
The workspace is on Starter or Pro, or you are a Member or Viewer. Both are required: Business or
above, and Owner or Admin.

**Symptom: an action you know happened is missing.**
Check the date filter and the time zone first. Then check whether it is a content action rather
than an admin action - those are not in this log.

**Symptom: the export is empty.**
The range covers a period before the workspace was on Business. Entries are only written while
the feature is active; upgrading does not backfill.

**Symptom: audit streaming stopped.**
The endpoint was marked unhealthy after six consecutive failures, exactly as ordinary webhooks
are, and raised ERR_6002. Fix the endpoint and re-enable it, then replay the missed window.

**Symptom: an IP address you do not recognise.**
Compare it against your VPN egress ranges before raising an alarm. Mobile carriers rotate
addresses constantly.

## Related error codes

- ERR_2031 - the plan or the role does not allow audit log access.
- ERR_6002 - the audit streaming endpoint was marked unhealthy.

## Related articles

- account-roles-permissions, account-session-timeout, tech-webhooks, tech-data-export,
  onboarding-glossary.

## If this did not help

Contact support with the workspace name, the exact UTC time range, and what you are trying to
establish. For a security investigation say so explicitly - we prioritise those and can search
further back than the UI exposes.
