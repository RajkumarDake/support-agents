---
title: Glossary
category: onboarding
---

# Glossary

The words this product and this help centre use, with the meaning we actually attach to them.
Several of these have a specific billing or permission consequence, noted where it matters.

## Structure

**Workspace.** The top-level container. It holds billing, members, settings and projects. Almost
everything - seats, storage, API limits, the audit log - is scoped to one workspace. Two
workspaces never share anything, including account credit.

**Project.** A scoped area inside a workspace with its own membership. Project membership
controls what someone sees; their role controls what they can do. A person in no project sees an
empty workspace even with a full role.

**Item.** Anything created inside a project - a record, a document, an attachment.

## People and access

**Owner.** Exactly one per workspace. The only role that can change the plan, change the payment
method, configure SSO, delete the workspace or transfer ownership. See
account-transfer-ownership.

**Admin.** Manages people, projects, integrations and settings, and can read invoices. Cannot
delete the workspace.

**Member.** Creates and edits content in their projects.

**Viewer.** Read-only plus commenting. Free on Business and Enterprise; a billed seat on Starter
and Pro. See account-guest-viewer-access.

**Seat.** A billed, active member. Pending invitations are not seats; deactivated people still
are. See billing-seat-pricing.

**Deactivated.** Signed out and blocked from signing in, but still holding a seat and still
billed. Business and Enterprise only.

## Billing

**Period.** The current billing month or year. Usage counts against it and API allowances reset
at its start. See billing-cycle.

**Renewal date.** The day the next period begins and the recurring charge is raised.

**Proration.** Charging or crediting for part of a period when something changes mid-cycle.
Appears on invoices as `Plan change adjustment`. See billing-proration.

**Credit.** A balance applied automatically to your next invoice. Not cash, not transferable, and
forfeited if the workspace is closed. See refund-downgrade-credit.

**Refund.** Money returned to the original payment method. Distinct from credit. See
refund-policy.

**Read-only.** The state a workspace enters at the end of a cancelled period, or on day 15 of an
unpaid grace period. Everything is readable, nothing is writable, no data is lost.

**Suspended.** Stricter than read-only: nobody can sign in at all. Caused by an open chargeback.
See billing-dispute-chargeback.

## Technical

**Error code.** An identifier of the form `ERR_NNNN`. The first digit gives the family: 1xxx
authentication, 2xxx permissions, 3xxx validation, 4xxx rate limiting, 5xxx storage and uploads,
6xxx integrations and webhooks. See tech-error-codes-overview.

**Incident.** A recorded service problem with an ID of the form `INC-NNNN`, published on the
status page. Referenced when claiming a service credit. See tech-service-status.

**Audit log.** The immutable record of admin actions, readable and exportable by Owners and
Admins on Business and above. See account-audit-logs.

**Export.** A background job that packages workspace data into a downloadable archive, emailed as
a signed link valid for 24 hours. See tech-data-export.

**Webhook.** An HTTP callback we send to your endpoint when something happens. Delivered at least
once, so handlers must be idempotent. See tech-webhooks.

**Rate limit.** The cap on API requests per minute, distinct from the per-period call allowance.
Both surface as ERR_4029. See tech-api-rate-limits.

**Token.** An API credential. Personal tokens inherit their creator's role and die with their
sessions; workspace tokens do not. See tech-api-keys.

**SSO / SAML.** Signing in through your identity provider. Business and Enterprise. See
tech-sso-saml.

**SCIM.** Automatic account creation and removal driven by your directory. See
account-scim-provisioning.

## Related articles

- onboarding-first-week, account-roles-permissions, billing-seat-pricing,
  tech-error-codes-overview.

## If this did not help

If a term in the product is not defined here, tell support where you saw it. Undefined vocabulary
in the interface is a bug in our writing, and we would rather fix it than explain it repeatedly.
