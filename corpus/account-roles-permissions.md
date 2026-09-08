---
title: Roles and what each one can do
category: account
---

# Roles and what each one can do

Every person in a workspace has exactly one role. The role decides what they can see and change
across the whole workspace; project membership then decides which content they see inside it.
Most permission questions and most ERR_2031 errors come down to someone holding a lower role
than the action needs.

## The four roles

**Owner.** Everything. Billing, invoices, payment methods, plan changes, deleting the workspace,
transferring ownership, security settings, SSO, audit log export. There is exactly one Owner per
workspace and the role cannot be shared.

**Admin.** Manages people, projects, integrations and workspace settings, and can view and
download invoices. An Admin cannot delete the workspace, cannot transfer ownership, and cannot
remove the Owner. On Business and Enterprise, Admins can also read the audit log and enforce 2FA.

**Member.** Creates and edits content in the projects they belong to. Cannot see Settings > Team
management actions, cannot see invoices, cannot manage integrations.

**Viewer.** Read-only everywhere they have access, plus commenting. Cannot create, edit, delete,
upload or export. Viewers are free on Business and Enterprise and do not consume a seat; on
Starter and Pro a Viewer occupies a normal billed seat.

## Permission matrix

| Action | Owner | Admin | Member | Viewer |
|---|---|---|---|---|
| Invite and remove people | yes | yes | no | no |
| Change someone's role | yes | yes | no | no |
| View and download invoices | yes | yes | no | no |
| Change plan or payment method | yes | no | no | no |
| Delete the workspace | yes | no | no | no |
| Transfer ownership | yes | no | no | no |
| Manage integrations and webhooks | yes | yes | no | no |
| Configure SSO and SCIM | yes | no | no | no |
| Read and export the audit log | yes | yes | no | no |
| Create and edit content | yes | yes | yes | no |
| Upload files | yes | yes | yes | no |
| Run an export | yes | yes | yes | no |
| Comment | yes | yes | yes | yes |

## Changing someone's role

1. Open Settings > Team.
2. Click the role dropdown next to the person.
3. Pick the new role. The change applies immediately - no sign-out is needed, though open tabs
   may need a reload before the UI reflects it.

Raising a Viewer to Member on Business or Enterprise starts consuming a seat and is billed
prorated from that moment. Lowering a Member to Viewer on those plans frees the seat and issues
a credit on the next invoice.

## Edge cases and gotchas

- Role changes are workspace-wide. There is no per-project role; project membership is separate
  and only controls visibility.
- An Admin can raise another Member to Admin. They cannot grant Owner.
- API tokens inherit the role of the person who created them. Lowering someone's role
  immediately narrows what their existing tokens can do - it does not revoke them. See
  tech-api-keys.
- If SSO group mapping is configured, the identity provider is the source of truth and a role
  changed here is overwritten at the next sign-in. See account-scim-provisioning.
- The Owner cannot be demoted directly. Transfer ownership, which downgrades the old Owner to
  Admin in the same action.

## Troubleshooting

**Symptom: ERR_2031 "insufficient permissions".**
The signed-in role cannot perform the action. Check your role under Settings > Team, then either
ask an Owner or Admin to raise it or to do the action for you. Invoices and team management are
Owner and Admin only.

**Symptom: an Admin cannot see Billing > Payment method.**
That is by design. Admins can read invoices but not change how the workspace pays. Only the
Owner can.

**Symptom: someone's role reverts after they sign in again.**
SSO group mapping or SCIM is driving roles from your directory. Change the group membership
upstream.

**Symptom: a Viewer is being billed.**
Free Viewers are a Business and Enterprise feature. On Starter and Pro a Viewer is a normal seat.

## Related error codes

- ERR_2031 - insufficient permissions for the attempted action.
- ERR_2044 - seat limit reached, which can appear when raising a Viewer to Member.

## Related articles

- account-add-team-member - inviting with a role.
- account-guest-viewer-access - free Viewer seats in detail.
- account-transfer-ownership - moving the Owner role.

## If this did not help

Tell support the action you were trying to take, your role, and the full error code. Include the
workspace name so we can read the audit log entry for the denied attempt.
