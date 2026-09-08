---
title: Mobile app not syncing
category: technical
---

# Mobile app not syncing
The mobile app syncs on open, on foreground, and every 15 minutes in the background. If a device
shows stale data, check that background refresh is enabled in the OS settings and that the
device clock is set automatically.

Signing out and back in forces a full resync and clears the local cache. Cached attachments are
kept for 30 days.
