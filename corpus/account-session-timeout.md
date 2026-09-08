---
title: Session length and automatic sign-out
category: account
---

# Session length and automatic sign-out

A session is how long you stay signed in before we ask you to authenticate again. The defaults
suit most teams; regulated workspaces usually want them shorter. This article covers the
defaults, how to change them, how "Sign out everywhere" differs from waiting for a timeout, and
what to check when you are being signed out far more often than expected.

## Defaults

| Surface | Idle timeout | Absolute maximum |
|---|---|---|
| Web, "Remember this device" ticked | 30 days | 90 days |
| Web, not remembered | 12 hours | 12 hours |
| Mobile app | none | 90 days |
| Personal API token | none | until revoked |

The idle timeout is reset by activity. The absolute maximum is not: after 90 days you sign in
again no matter how active you have been.

## Changing the policy for your workspace

On Business and Enterprise, an Owner can shorten these under Settings > Security > Session policy.

1. Open Settings > Security.
2. Under Session policy, set Idle timeout and Maximum session length.
3. Optionally turn off "Allow remember this device", which forces the 12 hour behaviour for
   everyone.
4. Save. The new policy applies to sessions created from that point on; existing sessions are not
   shortened retroactively unless you also click Sign out all members.

Starter and Pro workspaces use the defaults and cannot change them.

## Signing out other devices

Settings > Security > Sign out everywhere ends every session on every device, including mobile,
and revokes your personal API tokens. Use it when you have lost a device or suspect your password
was exposed. Resetting your password on its own does not do this - see account-password-reset.

An Owner or Admin can force-sign-out another person from Settings > Team > the person > Sign out
all sessions. This does not remove them or free their seat; for that see account-remove-member.

## SSO workspaces

When SSO is enforced, we honour the session lifetime from the SAML assertion if the identity
provider sends one, and fall back to our own policy if it does not. In practice this means your
identity provider's timeout usually wins, and shortening our setting has no visible effect. Set
the timeout at the identity provider instead. See tech-sso-saml.

Signing out here does not sign you out of the identity provider, so clicking sign-in again can
put you straight back in without a prompt. That is the identity provider's session, not ours.

## Edge cases and gotchas

- Each browser profile is a separate session. Signing out in one does not affect the other.
- The mobile app has no idle timeout by design, so a phone that is not locked is a real exposure.
  Enforce 2FA and a device passcode - see account-two-factor.
- Changing your password ends sessions on other devices only if you also use Sign out everywhere.
- Session expiry never destroys unsaved work in the editor; drafts are held locally and reappear
  after you sign back in.
- Sign-outs caused by policy are written to the audit log with the reason. See
  account-audit-logs.

## Troubleshooting

**Symptom: signed out every few minutes.**
Almost always the browser discarding cookies. Check for a privacy extension or a "clear cookies
on close" setting, and confirm third-party cookie blocking is not applied to our domain. Test in
an incognito window with extensions off - see tech-browser-support.

**Symptom: signed out whenever you switch networks.**
A corporate proxy is rewriting requests and dropping the session cookie. Ask IT to exempt our
domain from TLS interception.

**Symptom: the mobile app asks for sign-in daily.**
The OS is evicting the app's storage under memory pressure. On Android 15 this is related to the
aggressive background suspension tracked in tech-mobile-sync.

**Symptom: "Remember this device" never sticks.**
The device is shared or the browser is in a private window, where the flag cannot persist.

**Symptom: an API script started returning 401 overnight.**
Someone used Sign out everywhere on the account that owns the token, which revokes personal
tokens too. Create a workspace token instead, see tech-api-keys.

## Related articles

- account-password-reset, account-two-factor, tech-sso-saml, tech-api-keys,
  account-audit-logs.

## If this did not help

Contact support with the workspace name, whether the problem is on web or mobile, the browser and
version, and roughly how long a session lasts before it drops. If it is one person only, that
points at the device; if it is everyone, that points at the policy.
