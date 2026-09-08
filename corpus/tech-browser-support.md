---
title: Supported browsers and blank screens
category: technical
---

# Supported browsers and blank screens
We support the current and previous major versions of Chrome, Edge, Firefox and Safari. A blank
screen after sign-in is nearly always an extension blocking our application bundle, or a stale
service worker.

Try an incognito window first. If that works, disable extensions one at a time. To clear a stale
worker, hard reload with the developer tools open and `Disable cache` ticked.
