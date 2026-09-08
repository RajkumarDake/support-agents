---
title: Resetting a password
category: account
---

# Resetting a password

If you cannot remember your password, you reset it yourself from the sign-in screen. Support
cannot read or set your password. This article covers the reset flow, why links expire, what
changes when SSO or 2FA is on, and how to get back in when the usual route is closed.

## Steps

1. Go to the sign-in screen and click Forgot password.
2. Enter the email address you use for the workspace.
3. We send a reset email. It arrives within a minute in normal conditions.
4. Open the link and choose a new password. It must be at least 12 characters and cannot be one
   of your last five passwords.
5. You are signed in on that device.

If you know your current password and simply want to change it, use Settings > Security > Change
password instead. That route asks for the old password and does not send an email.

## Rules the reset link follows

- Valid for one hour from the moment it is requested.
- Single use. Clicking it twice, or having a mail scanner pre-fetch it, burns it.
- Requesting a second reset invalidates the first link, so always use the newest email.
- We always answer "if that address exists we sent a link", whether or not the account exists, so
  the flow cannot be used to discover who has an account.

## What resetting does not do

Resetting a password does not sign you out of your other devices. If you are resetting because
you think someone else has your password, go to Settings > Security > Sign out everywhere
immediately after resetting. That ends every session on every device and invalidates your
personal API tokens. See account-session-timeout for how sessions expire on their own.

## SSO workspaces

If SSO is enforced for your workspace, password sign-in is disabled and the Forgot password link
does nothing useful - you must sign in through your identity provider. Reset your password there.
The exception is a break-glass admin account, which is excluded from enforcement so the workspace
is not locked out when the identity provider is down. See tech-sso-saml.

## Two-factor authentication

Resetting a password does not bypass 2FA. After setting the new password you are still asked for
your authenticator code or security key. If you have lost both the device and the recovery codes,
support cannot restore access - we have no other way to verify identity. account-two-factor
explains what to store and where.

## Troubleshooting

**Symptom: ERR_1077 "reset link expired".**
The link is older than one hour, or it has already been used once. Request a fresh link and open
it in the same browser you requested it from.

**Symptom: the email never arrives.**
Check spam. Confirm you typed the address that is actually on the account - an invited address
that was never accepted has no password to reset. Corporate filters sometimes quarantine the
mail; ask IT to allow our sending domain.

**Symptom: the link opens the sign-in page instead of the reset form.**
Something pre-fetched and consumed the link, usually a mail security scanner. Request a new link
and copy-paste it into the browser rather than clicking.

**Symptom: "password does not meet requirements".**
Minimum 12 characters, and it cannot match your last five. A passphrase of three or four words
is easier than a short complex string.

**Symptom: you reset the password and are immediately asked to reset it again.**
Your workspace enforces a password rotation policy and the new password was too close to the old
one. Choose something genuinely different.

**Symptom: you are the only Owner and cannot get in at all.**
Contact support from the billing email address on the account. We verify domain ownership with
the billing contact before doing anything, which takes one business day.

## Related error codes

- ERR_1077 - the reset link expired or was already used.
- ERR_1104 - SSO assertion rejected, which appears instead of a password error in SSO
  workspaces.

## Related articles

- account-two-factor - recovery codes and what happens if you lose them.
- account-session-timeout - session length and Sign out everywhere.
- tech-sso-saml - signing in through an identity provider.

## If this did not help

Contact support with the email address on the account and the time you requested the last reset
link. Do not send us a password. If 2FA is the blocker, say so up front so we can tell you
straight away whether recovery is possible.
