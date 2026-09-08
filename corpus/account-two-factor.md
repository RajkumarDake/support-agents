---
title: Two-factor authentication
category: account
---

# Two-factor authentication

Two-factor authentication (2FA) adds a second step to sign-in, so a stolen password on its own is
not enough to get into your account. We support authenticator apps that generate time-based codes
(TOTP) and hardware security keys. We do not support SMS, because SMS codes can be intercepted
through SIM swapping.

## Enabling 2FA on your own account

1. Open Settings > Security.
2. Click Enable two-factor authentication.
3. Choose Authenticator app or Security key.
4. For an authenticator app, scan the QR code with your app of choice and type the six-digit code
   back to confirm. For a security key, insert or tap the key when the browser prompts.
5. We show ten single-use recovery codes. Save them now - this is the only time they are shown.
6. Click Done. You are asked for the second factor from your next sign-in onward.

You can register a second security key from the same screen. Doing so is the single best thing
you can do to avoid a lockout.

## Recovery codes

Each of the ten codes works once. Use one in place of the authenticator code when you do not have
the device. Store them in a password manager or print them and keep them somewhere physical - not
in the workspace itself, which you will not be able to reach.

Regenerate the codes from Settings > Security > Recovery codes at any time. Regenerating
invalidates the previous ten immediately.

**This is the irreversible part.** Without the device and without a recovery code, support cannot
restore access to an account with 2FA enabled. We have no other way to verify that you are you,
and making an exception would defeat the point of the feature. If you are the only Owner, an
Admin can transfer nothing on your behalf, so the workspace is stuck until you find a code. Read
account-transfer-ownership before you get into that position.

## Requiring 2FA for the whole workspace

On Business and Enterprise, an Admin can require 2FA for everyone under Settings > Security >
Require two-factor authentication. When you turn it on:

- Members who already have 2FA are unaffected.
- Members who do not are prompted to enrol at their next sign-in and cannot use the workspace
  until they finish.
- Pending invitations are unaffected until accepted, then enrolment is required.
- Personal API tokens keep working. 2FA gates interactive sign-in, not token auth. See
  tech-api-keys.

This option is not available on Starter or Pro. If your workspace enforces SSO, enforce the
second factor at the identity provider instead - see tech-sso-saml.

## Edge cases and gotchas

- TOTP codes depend on the clock. If your phone's clock drifts, codes are rejected even though
  they look right. Set the device clock to update automatically.
- Deleting the authenticator app entry, or resetting a phone without migrating the app, loses the
  secret. Recovery codes are the only way back.
- Resetting your password does not disable 2FA, and does not skip the second factor. See
  account-password-reset.
- Disabling 2FA on your own account asks for a current code first. If enforcement is on for the
  workspace, you cannot disable it at all.
- Enrolments and disablements are written to the audit log. See account-audit-logs.

## Troubleshooting

**Symptom: "invalid code" for every code the app generates.**
Clock drift. Enable automatic date and time on the device, then try again. In Google
Authenticator, Settings > Time correction for codes > Sync now.

**Symptom: the security key is not detected.**
Use a supported browser - current or previous major version of Chrome, Edge, Firefox or Safari,
see tech-browser-support. Security keys also require an HTTPS page and will not work through some
corporate proxies that terminate TLS.

**Symptom: you used all ten recovery codes.**
Sign in with a code you still have, then regenerate. If you are out of codes and out of device,
there is no route back.

**Symptom: a member is locked out of a workspace that enforces 2FA.**
An Owner or Admin can reset that person's 2FA enrolment from Settings > Team > the person >
Reset two-factor. They then enrol again at their next sign-in. Admins cannot reset the Owner's
2FA.

## Related articles

- account-password-reset - the reset flow with 2FA in the way.
- account-session-timeout - how long a verified session lasts.
- tech-sso-saml - enforcing a second factor at the identity provider.
- account-audit-logs - who enabled or reset 2FA and when.

## If this did not help

Contact support with the workspace name and the email address of the affected account. If you are
locked out with no recovery code, say so in the first message - we will tell you immediately
whether anything can be done rather than leaving you waiting.
