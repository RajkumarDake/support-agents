---
title: What your teammates see
category: onboarding
---

# What your teammates see

This article describes the invitation from the other side - what lands in the inbox, what the
first screens look like, and why a new joiner sometimes reports seeing "nothing". If you are the
one doing the inviting, see account-add-team-member for the mechanics.

## The email

An invited person gets one email with a single sign-up link. It names the workspace, the person
who invited them, and the role they have been given. The link is valid for **7 days** and is
personal to that address - forwarding it to a colleague does not work.

Resending an invitation issues a new link and invalidates the previous one, so anyone with two
emails in their inbox must use the newest.

## The three sign-up paths

**Verified domain.** If their email domain matches a verified domain on the workspace, they skip
straight in. No password step at all.

**Password.** Otherwise they set a password: minimum 12 characters, and they are prompted to
enable two-factor authentication if the workspace requires it, see account-two-factor.

**SSO.** If SSO is enforced, the link redirects to your identity provider and they come back
signed in. They never set a password with us. If the assertion is missing the `email` attribute
or clocks are out by more than five minutes, they see ERR_1104 - see tech-sso-saml.

## The first screens

1. A three-step tour of the interface. It can be skipped and re-run later from the help menu.
2. Their profile: display name, avatar, time zone. The time zone matters - it drives digest
   timing and every timestamp they see, see onboarding-notifications.
3. The workspace, showing **only the projects they have been added to**.

That last point is the one to plan for. A new joiner with a full Member role but no project
membership sees an empty screen and reasonably concludes something is broken. Add people to
projects before inviting them, or immediately after.

## What they can do on day one

Their role decides it, not their newness. A Member can create and edit in their projects; a
Viewer can read and comment only. Nothing is unlocked over time and there is no probation
period. See account-roles-permissions.

They can install the mobile app straight away with the same credentials. On Starter the app is
read-and-comment only; on Pro and above it is fully editable, see onboarding-mobile-app.

## Edge cases and gotchas

- A pending invitation consumes no seat, so a wave of invitations costs nothing until people
  accept - see billing-seat-pricing.
- Inviting an address that is already a member does nothing and reports "already a member".
- If the workspace hits its seat cap before someone accepts, their acceptance fails with
  ERR_2044. Free a seat and ask them to try again.
- A person invited to two workspaces gets two emails and two separate accounts' worth of context;
  they switch between them from the workspace menu.
- Under SCIM, invitations are skipped entirely - accounts are created by the directory and the
  person simply signs in. See account-scim-provisioning.
- New joiners are not automatically notified about existing content. Mention them, or they will
  not know where to look.

## Troubleshooting

**Symptom: "this invitation has expired".**
Older than 7 days. Ask an Owner or Admin to resend from Settings > Team.

**Symptom: "this invitation is not for you".**
The link was forwarded. Invitations are bound to the address they were sent to.

**Symptom: the email never arrived.**
Check spam, then confirm the address in Settings > Team has no typo. Corporate filters are the
usual cause; the invitation link can be copied from the team list and sent by other means.

**Symptom: signed in successfully but the workspace is empty.**
No project membership. An Owner or Admin adds them under Settings > Team > the person > Projects.

**Symptom: ERR_1104 at the identity provider step.**
Missing `email` attribute or clock skew over five minutes. See tech-sso-saml.

**Symptom: ERR_2044 on acceptance.**
The seat cap was reached between the invitation and the acceptance.

## Related error codes

- ERR_2044 - seat limit reached at acceptance.
- ERR_1104 - SSO assertion rejected.
- ERR_1077 - a password reset link expired, if they went that route instead.

## Related articles

- account-add-team-member, account-roles-permissions, onboarding-first-week,
  onboarding-mobile-app, tech-sso-saml.

## If this did not help

Contact support with the workspace name, the invited address, and a screenshot of what they see.
If it is one person out of many, the cause is nearly always the address or their mail filter; if
it is everyone, it is the workspace configuration.
