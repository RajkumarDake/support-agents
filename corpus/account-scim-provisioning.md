---
title: SCIM directory provisioning
category: account
---

# SCIM directory provisioning

SCIM lets your identity provider create, update and deactivate people in the workspace
automatically, so joining and leaving your company is the only thing anyone has to do. It is
available on Enterprise, and on Business as an add-on. It is normally set up alongside SAML
sign-in - see tech-sso-saml, which handles authentication while SCIM handles the account
lifecycle.

## Before you start

- SSO must already be configured and working. SCIM without SSO creates accounts nobody can sign
  in to.
- You need the Owner role. Admins can view the configuration but not change it.
- Decide your group-to-role mapping first. Once SCIM is live, roles set in our UI are overwritten
  at the next sync.

## Setup

1. Open Settings > Security > Directory provisioning.
2. Click Enable SCIM. We show the SCIM base URL and generate a bearer token.
3. Copy both into your identity provider's provisioning configuration. The token is shown once;
   regenerate it from the same screen if you lose it.
4. Map attributes. We require `userName` (the email address), and use `givenName`, `familyName`
   and `active`. Anything else is ignored.
5. Map groups to roles under Group mapping. A person in no mapped group is provisioned as a
   Member by default; change the fallback on the same screen.
6. Push a test user from the identity provider and confirm the row appears under Settings > Team
   with the status `Provisioned`.
7. Enable full sync.

## How the lifecycle works

| Identity provider event | What happens here |
|---|---|
| User assigned to the app | Account created, invitation skipped, seat consumed |
| Group membership changed | Role updated at the next sync |
| `active` set to false | Account deactivated, sessions ended, seat still billed |
| User unassigned or deleted | Account removed, seat freed, content reassigned to the Owner |
| Attribute changed | Name and email updated in place |

Syncs are pushed by your identity provider, so the cadence is theirs - typically every 20 to 40
minutes, with immediate pushes on assignment for most providers.

## Edge cases and gotchas

- **Removing someone in our UI does not stick.** The next sync recreates them. Deprovision
  upstream. This surprises people during offboarding, so see account-remove-member for the manual
  route and use it only for non-SCIM accounts.
- Seats are consumed the moment SCIM creates the account, not when the person first signs in. A
  bulk assignment of 40 people bills 40 seats immediately, and can fail with ERR_2044 partway
  through if the plan does not have room. Raise the plan before a bulk push.
- Deactivating with `active: false` does not free the seat. Unassign to free it. This is the
  single most common cause of an unexpectedly large invoice after a SCIM rollout.
- The Owner cannot be deprovisioned by SCIM. If the Owner is unassigned upstream we keep the
  account and log a warning; transfer ownership first, see account-transfer-ownership.
- Free Viewers on Business and Enterprise still work: map a group to the Viewer role and those
  people consume no seat, see account-guest-viewer-access.
- All SCIM operations are written to the audit log with a `scim` actor, see account-audit-logs.

## Troubleshooting

**Symptom: the identity provider reports 401 on every SCIM call.**
The bearer token is wrong or was regenerated. Copy it again from Settings > Security > Directory
provisioning.

**Symptom: the identity provider reports 403 or ERR_2031.**
SCIM is not enabled for the plan, or the workspace dropped to Pro. Provisioning stops on
downgrade, see account-downgrade-plan.

**Symptom: users are created but cannot sign in.**
SAML is not configured, or the assertion is missing the `email` attribute, which surfaces as
ERR_1104. See tech-sso-saml.

**Symptom: provisioning fails partway through a bulk push with ERR_2044.**
The plan ran out of seats mid-batch. Raise the plan, then retry the push - already-created users
are skipped.

**Symptom: roles keep reverting.**
Expected. Group mapping is authoritative. Change the group, not the role.

**Symptom: duplicate accounts for the same person.**
The `userName` changed upstream without a matching update, so we treated it as a new user. Merge
by removing the stale account after confirming which one has the current email.

## Related error codes

- ERR_2044 - seat limit reached during provisioning.
- ERR_2031 - SCIM not available on this plan or role.
- ERR_1104 - SAML assertion rejected at sign-in.

## Related articles

- tech-sso-saml, account-roles-permissions, account-seat-reassignment.

## If this did not help

Contact support with the workspace name, your identity provider and its version, and the raw
request and response from a failing SCIM call if your provider exposes them. Those three make
almost every provisioning problem obvious in one pass.
