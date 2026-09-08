---
title: Installing the mobile app
category: onboarding
---

# Installing the mobile app

The mobile app covers reading, commenting and light editing on the move. It is not a replacement
for the web application and does not include any administrative features - billing, team
management, integrations and settings are web only.

## Installing and signing in

1. Install from the App Store or Google Play. Search for the product name; there is one official
   app and no separate "lite" version.
2. Open it and enter the email address you use for the workspace.
3. Sign in with your password, or, in an SSO workspace, the app opens a browser window to your
   identity provider and returns you to the app when it succeeds. See tech-sso-saml.
4. Complete two-factor authentication if enabled. Security keys work over NFC on both platforms;
   authenticator codes work everywhere. See account-two-factor.
5. Choose the workspace if you belong to more than one. Switch later from the account menu.

Minimum versions are iOS 16 and Android 12. Older devices can use the web application in a mobile
browser, subject to tech-browser-support.

## What you can do, by plan

| Plan | Mobile capability |
|---|---|
| Starter | Read and comment only |
| Pro | Full editing |
| Business | Full editing |
| Enterprise | Full editing |

This catches people out after a downgrade: dropping from Pro to Starter makes the app read-only
for everyone at the moment the downgrade lands, see account-downgrade-plan.

## Offline mode

The app caches the last **30 days** of activity, so recently touched items are readable with no
connection. Cached attachments are also kept for 30 days.

Comments written offline are queued and sent when connectivity returns. Edits to an item that
someone else changed in the meantime are flagged as a conflict rather than being applied blindly;
you choose which version wins.

## Syncing

The app syncs on open, on foreground, and every 15 minutes in the background. If it is showing
old data, tech-mobile-sync has the full diagnosis - the short version is to check that background
refresh is enabled in the OS settings and that the device clock is set automatically.

There is a known issue with aggressive background suspension on some Android 15 devices,
tracked as INC-2274. Pull to refresh, or sign out and back in to force a full resync. See
tech-service-status.

## Edge cases and gotchas

- Push notifications need both the OS permission and the mobile push setting under Settings >
  Notifications. Both must be on, see onboarding-notifications.
- The app has no idle timeout by design. A phone without a passcode is a real exposure; workspace
  session policy does not protect it, see account-session-timeout.
- Uploading from a phone is subject to the same per-file limits as the web - 100 MB on Starter,
  2 GB on Pro and Business - and large uploads on a mobile connection frequently outlive the
  15-minute upload token and fail with ERR_5012. See tech-err-5012-upload.
- Exports cannot be started from the app. Use the web application, see tech-data-export.
- The app does not show invoices or plan settings at all.
- Uninstalling clears the local cache immediately; it does not sign you out on other devices.

## Troubleshooting

**Symptom: sign-in loops back to the email screen.**
Usually an SSO redirect being intercepted by an in-app browser. Set the default browser to
Safari or Chrome and retry.

**Symptom: everything is read-only.**
Check the plan. Starter is read-and-comment by design, and so is a workspace that has gone
read-only after a cancellation or an unpaid invoice, see billing-payment-failed.

**Symptom: stale data.**
Pull to refresh, then check background refresh in OS settings. See tech-mobile-sync.

**Symptom: an upload from the phone fails.**
Move to Wi-Fi, keep the app in the foreground, and retry. Mobile uploads over 100 MB on a cellular
connection rarely finish inside the token window.

**Symptom: no push notifications.**
OS permission first, app setting second, then check whether the project is muted.

## Related error codes

- ERR_5012 - upload rejected, common on slow mobile connections.
- ERR_1104 - SSO assertion rejected during the browser hand-off.

## Related articles

- tech-mobile-sync, onboarding-notifications, account-session-timeout.

## If this did not help

Contact support with the device model, the OS version, the app version from the account menu, and
what you were doing. Mobile problems are very often platform-specific, and those four details
narrow it immediately.
