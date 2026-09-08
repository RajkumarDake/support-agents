---
title: SSO and SAML sign-in problems
category: technical
---

# SSO and SAML sign-in problems

SSO lets people sign in through your identity provider instead of with a password. It is available
on **Business and Enterprise**. This article covers setup, the two failures that account for
almost every ERR_1104, and how to avoid locking your whole team out.

## Setting it up

1. Open Settings > Security > SSO. Owner only.
2. Copy our Entity ID and Assertion Consumer Service URL into your identity provider.
3. Configure the assertion to send `email` as an attribute. This is mandatory - see below.
4. Download the metadata XML from your identity provider and upload it under Settings > Security >
   SSO.
5. Test with the Test connection button before enforcing anything. It signs you in through the
   provider without changing the workspace.
6. Once it works, turn on Enforce SSO.

Automatic account creation and removal is a separate feature - see account-scim-provisioning.

## The two errors we see most

Both surface as **ERR_1104**, "SSO assertion rejected":

**Clock skew over five minutes.** SAML assertions carry validity windows. If the identity
provider's host or the signing-in machine drifts more than five minutes from real time, the
assertion is outside its window and is rejected. Confirm both the IdP host and the local machine
sync time via NTP.

**A missing `email` attribute.** We identify people by email address. An assertion that omits it
has nobody to sign in. Confirm the IdP sends an `email` attribute; some providers call the mapping
`mail` or `emailaddress` and need it aliased.

Two further steps resolve most remaining cases: re-download the metadata XML and re-upload it
under Settings > Security > SSO, and sign in from an incognito window so a cached session is not
involved.

## Break-glass accounts

When SSO is enforced, password sign-in is disabled for everyone **except break-glass admin
accounts**. Designate at least one under Settings > Security > SSO > Break-glass accounts before
you enforce.

Store that account's recovery codes offline. If your identity provider goes down and you have no
break-glass account, nobody can sign in, including to turn SSO off. This is the single most
serious self-inflicted lockout available in the product. See account-two-factor.

## Known incident: Okta metadata

A certificate rotation on our side invalidated cached IdP metadata for some Okta tenants,
producing ERR_1104 on sign-in. This is incident INC-2279, resolved, started 2026-08-29. The fix
was to re-upload the metadata XML under Settings > Security > SSO. If you are seeing ERR_1104 on
an Okta tenant and have not re-uploaded since late August, do that first. See
tech-service-status.

## Edge cases and gotchas

- SSO is Business and Enterprise only. A downgrade to Pro disables it at the moment the downgrade
  lands, and everyone needs a password again - see account-downgrade-plan and
  account-password-reset.
- Enforcing SSO disables the Forgot password flow entirely. Reset passwords at the identity
  provider.
- Session length is taken from the assertion when the provider sends one, so your provider's
  timeout usually overrides ours - see account-session-timeout.
- 2FA is best enforced at the identity provider when SSO is on, rather than in both places.
- API tokens are unaffected by SSO. They authenticate directly, see tech-api-keys.
- Group-to-role mapping makes the identity provider authoritative for roles; changes made in our
  UI are overwritten at the next sign-in.
- Mobile sign-in opens a browser window to the provider and returns to the app, see
  onboarding-mobile-app.
- SSO configuration changes are written to the audit log, see account-audit-logs.

## Troubleshooting

**Symptom: ERR_1104 for everyone, suddenly.**
Certificate or metadata. Re-download and re-upload the metadata XML. Check whether your provider
rotated a signing certificate.

**Symptom: ERR_1104 for one person only.**
Their machine's clock, or their account missing an email attribute in the directory.

**Symptom: sign-in loops back to the provider.**
A cached session. Try incognito. If it persists, the ACS URL in the provider does not match ours
exactly - check for a trailing slash.

**Symptom: signs in but lands with no access.**
Group mapping put them in no group and the fallback role gives no project membership. See
account-roles-permissions.

**Symptom: the provider is down and nobody can sign in.**
Use a break-glass account. If none exists, contact support from the billing email; verification
takes one business day, which is why you configure one in advance.

**Symptom: SSO stopped after a plan change.**
The workspace dropped below Business.

## Related error codes

- ERR_1104 - SAML assertion rejected: missing `email`, or clock skew over five minutes.
- ERR_1077 - password reset link expired, seen when someone tries the password route in an
  SSO-enforced workspace.

## Related articles

- account-scim-provisioning, account-two-factor, account-session-timeout,
  account-password-reset, tech-service-status, account-audit-logs.

## If this did not help

Contact support with the workspace name, your identity provider, the exact time of a failed
attempt, and a copy of the SAML response if your provider can export one. The assertion itself
usually shows the cause in one line.
