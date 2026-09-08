---
title: Supported browsers and blank screens
category: technical
---

# Supported browsers and blank screens

We support the **current and previous major versions** of Chrome, Edge, Firefox and Safari, on
desktop and mobile. Anything older may work and is not tested. A blank screen after sign-in is
nearly always one of two things: an extension blocking our application bundle, or a stale service
worker.

## The 60-second diagnosis

1. **Open an incognito or private window and sign in.** Extensions are disabled there by default.
2. If it works in incognito, the cause is an **extension**. Disable them one at a time in a normal
   window until the page loads. Ad blockers, privacy tools, corporate security extensions and
   script blockers are the usual candidates.
3. If it does not work in incognito, the cause is more likely a **stale service worker** or a
   network path. Continue below.

## Clearing a stale service worker

The application registers a service worker so it loads quickly and works briefly offline. A
partially updated worker can serve a broken bundle indefinitely, because it never asks the network
for a fresh one.

1. Open developer tools (F12, or Cmd-Option-I on macOS).
2. Go to the Network tab and tick **Disable cache**.
3. With developer tools still open, hard reload: Ctrl-Shift-R, or Cmd-Shift-R on macOS.
4. If that does not clear it, go to Application > Service workers > Unregister, then reload.

## Corporate networks

Three things regularly break the application on a managed network:

- **TLS interception.** A proxy that terminates and re-signs TLS breaks security keys for 2FA and
  can break the service worker. Ask IT to exempt our domain, see account-two-factor.
- **Content filtering** that blocks our application bundle or our CDN. This produces exactly the
  blank screen described above, and incognito does not help.
- **Cookie policies** that clear cookies on close or block them per-site, which shows up as being
  signed out constantly, see account-session-timeout.

## Other browser-related symptoms

- **Popups blocked.** The 3-D Secure challenge when saving a card opens a window; a blocker
  silently prevents it and the card appears to fail. See billing-payment-methods.
- **Security keys not detected.** Requires HTTPS, a supported browser, and no TLS interception.
- **Uploads stalling.** Browsers throttle background tabs, which can slow a large upload enough to
  outlive its 15-minute token and fail with ERR_5012. Keep the tab in the foreground, see
  tech-err-5012-upload.
- **Date and time wrong everywhere.** The interface uses your profile time zone, not the browser's.
  Set it on your profile.

## Edge cases and gotchas

- Browsers in "reduced data" or "lite" modes proxy requests through the vendor's servers and can
  serve stale assets.
- Extensions that inject CSS can make the interface look broken without any error.
- Firefox's Enhanced Tracking Protection in strict mode occasionally blocks our analytics endpoint;
  the application works but reports errors in the console. Harmless.
- Mobile browsers work, but the mobile app is a better experience, see onboarding-mobile-app.
- A blank screen that appears at exactly the same time for everyone in your team is not a browser
  problem. Check tech-service-status.

## Troubleshooting

**Symptom: blank white page after sign-in.**
Incognito first, then extensions, then service worker.

**Symptom: works for one person, not another, same browser version.**
Extensions or a local profile. Compare extension lists.

**Symptom: works at home, not in the office.**
Corporate network. TLS interception or content filtering.

**Symptom: the page loads but half the interface is missing.**
Partially blocked bundle, usually an ad blocker with an aggressive filter list. Allow our domain.

**Symptom: constant sign-outs rather than a blank screen.**
Cookies, not rendering. See account-session-timeout.

**Symptom: an old browser version you cannot update.**
We support current and previous major versions only. On a locked-down machine, the mobile app is
often the practical alternative.

## Related error codes

- ERR_5012 - upload rejected, sometimes caused by a throttled background tab.

## Related articles

- account-session-timeout, account-two-factor, tech-service-status.

## If this did not help

Contact support with the browser and its exact version, the operating system, whether incognito
works, and any errors from the developer tools console. Those four answers identify almost every
rendering problem without further exchange.
