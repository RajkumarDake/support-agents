---
title: Notification settings
category: onboarding
---

# Notification settings

Notifications are configured per person, with a workspace-level default that applies to new
members. The design principle is that an individual always wins: an admin can set what people
start with, but cannot override what they choose afterwards.

## Your own settings

Settings > Notifications, per person:

| Channel | Options | Default |
|---|---|---|
| In-app | on or off | on |
| Email digest | off, daily, weekly | daily |
| Mobile push | on or off | on if the app is installed |

The digest is sent at 08:00 in your profile time zone. Change the time zone on your profile and
the digest moves with it.

## Workspace defaults

An Owner or Admin sets the default for new members under Settings > Notifications > Workspace
defaults. This applies at the moment someone joins and never again. Changing the default does not
touch anyone who has already been through onboarding, by design - see account-roles-permissions
for who can set it.

If your team says the product is noisy, change the default to a weekly digest and tell people
they can turn it up. That is much better received than the reverse.

## Mentions always notify

Being mentioned notifies you regardless of digest settings, in-app and by push, unless you have
muted the specific project. Mentions are the one thing that bypasses the digest, because the
alternative - someone waiting a week for an answer - is worse than an extra email.

To mute, open the project and use the bell icon > Mute project. Muting is per person and per
project, and survives digest changes.

## What generates a notification

- Mentions of you by name.
- Items assigned to you.
- Comments on items you created or are following.
- Invitations and role changes affecting you.
- For Owners and Admins: payment failures, renewal notices, and the 80%-of-limit usage warnings
  described in account-plan-and-usage.

Billing notices go to the Owner and to the billing email, and are not affected by these settings
at all - see billing-update-billing-details.

## Edge cases and gotchas

- Viewers receive notifications normally. Read-only access does not mean silence, so a Viewer who
  is mentioned will hear about it - see account-guest-viewer-access.
- Muting a project mutes mentions in it too. That is the intended trade-off.
- A digest with nothing in it is not sent. Silence usually means no activity, not a broken
  setting.
- Push requires OS-level permission as well as the setting here. Both must be on, see
  onboarding-mobile-app.
- Removing someone sends their outstanding mentions and assignments to the Owner, who gets a
  burst of notifications - see account-remove-member.
- Slack notifications are configured in the integration, not here, and are workspace-wide rather
  than personal. See onboarding-integrations.

## Troubleshooting

**Symptom: no email at all.**
Check the digest is not set to off, then check spam, then check your profile email address is one
you actually read.

**Symptom: the digest arrives at a strange hour.**
Your profile time zone is wrong. Set it on your profile; the digest follows it.

**Symptom: too many emails.**
Move the digest from daily to weekly, and mute noisy projects individually rather than turning
everything off.

**Symptom: no push on mobile.**
Check the OS notification permission for the app, then check mobile push here. If the app is also
showing stale data, the OS may be suspending it - see tech-mobile-sync.

**Symptom: an admin changed the default and nothing happened for the existing team.**
Expected. Defaults apply to new members only; individual settings are never overridden.

**Symptom: you stopped hearing about a project you care about.**
Check whether it is muted - the bell icon in the project shows the state.

## Related articles

- onboarding-mobile-app, onboarding-integrations, account-plan-and-usage,
  billing-update-billing-details, tech-mobile-sync, account-guest-viewer-access.

## If this did not help

Contact support with the workspace name, your email address, and an example of a notification you
expected but did not receive, with roughly the time it should have arrived. We can check whether
it was generated and whether it was delivered - those are different failures with different
fixes.
