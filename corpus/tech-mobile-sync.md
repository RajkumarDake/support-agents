---
title: Mobile app not syncing
category: technical
---

# Mobile app not syncing

Stale data on a phone is almost always the operating system suspending the app rather than
anything wrong with your account. This article is the diagnosis path, from the cheapest fix to the
most thorough.

## How syncing works

The app syncs in three situations:

- **On open**, every time.
- **On foreground**, when you switch back to it.
- **Every 15 minutes in the background**, if the OS allows it.

That last one is the fragile part. Both iOS and Android decide for themselves whether to grant
background time, based on battery state, how often you use the app, and their own heuristics.
When the OS declines, the app shows whatever it last fetched.

## Fixes, in order

1. **Pull to refresh.** Forces an immediate sync. If this shows current data, the account is fine
   and the problem is background scheduling.
2. **Check background refresh is enabled in the OS settings.** iOS: Settings > General >
   Background App Refresh. Android: the app's battery setting must not be Restricted.
3. **Check the device clock is set automatically.** A clock that is out by more than a few minutes
   causes sync requests to be rejected. This is the same class of problem behind ERR_1104 on SAML
   sign-in, see tech-sso-saml.
4. **Check connectivity properly.** A captive portal on hotel or office Wi-Fi returns HTTP
   responses that are not ours, which the app reports as a sync failure.
5. **Sign out and back in.** This forces a full resync and clears the local cache. It is the
   thorough fix and costs you only the cached attachments.

## Known incident: Android 15

Background refresh is being suspended aggressively by the OS on some Android 15 devices, leaving
the app showing data up to a day old. This is incident **INC-2274**, status investigating, started
2026-09-05.

Workaround: pull to refresh, or sign out and back in to force a full resync. If you are on Android
15 and seeing day-old data despite background refresh being enabled, this is what you are hitting
and there is currently no configuration change that avoids it. See tech-service-status.

## The local cache

The app caches the last **30 days** of activity, and cached attachments are kept for 30 days.
Signing out clears both. Uninstalling clears them immediately too, and does not sign you out on
other devices - see account-session-timeout.

Offline edits are queued and sent on reconnection. If someone else changed the same item
meanwhile, you get a conflict prompt rather than a silent overwrite.

## Edge cases and gotchas

- The app is read-and-comment only on Starter, so an edit that appears not to sync may simply not
  be permitted - see onboarding-mobile-app.
- A workspace in read-only mode after an unpaid invoice behaves identically to the Starter
  restriction, see billing-payment-failed.
- Sync does not consume your API rate limit; the app uses its own path.
- Low Power Mode on iOS and Battery Saver on Android both suspend background refresh entirely.
- Content in projects you are not a member of never syncs, which can look like missing data. Check
  project membership, see account-roles-permissions.
- A device with an old app version can fail to sync after a server change. Update from the store
  before diagnosing anything else.

## Troubleshooting

**Symptom: pull to refresh works, background does not.**
OS scheduling. Check background refresh and battery restrictions, and on Android 15 see INC-2274.

**Symptom: pull to refresh also shows old data.**
Sign out and back in. If it persists, the account may not have access to the content you expect.

**Symptom: sync fails with an authentication error.**
The session ended - a password reset elsewhere, Sign out everywhere, or removal from the
workspace. Sign in again.

**Symptom: attachments will not open offline.**
Only cached attachments from the last 30 days are available offline.

**Symptom: one item is stale, everything else is current.**
A queued offline edit is stuck in conflict. Open the item and resolve the prompt.

**Symptom: the app was fine and stopped after a plan change.**
Check whether the workspace downgraded to Starter, see account-downgrade-plan.

## Related error codes

- ERR_1104 - can appear during SSO sign-in from the app, usually clock skew.

## Related articles

- onboarding-mobile-app, tech-service-status, account-session-timeout, tech-sso-saml,
  onboarding-notifications.

## If this did not help

Contact support with the device model, the OS version, the app version from the account menu, and
roughly how stale the data is. Say whether pull to refresh fixes it - that single answer splits
the problem into two completely different causes.
