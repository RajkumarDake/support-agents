---
title: API rate limits
category: technical
---

# API rate limits
The API allows 60 requests per minute on Starter, 600 on Pro and Business, and negotiated
limits on Enterprise. Exceeding the limit returns HTTP 429 with ERR_4029 and a `Retry-After`
header.

Back off exponentially and honour `Retry-After`. Bursts are smoothed over a 10 second window,
so a tight loop will trip the limit even when your per-minute average is well under it.
