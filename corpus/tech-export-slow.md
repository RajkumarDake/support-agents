---
title: Exports that are slow or never arrive
category: technical
---

# Exports that are slow or never arrive
Exports run as background jobs and are emailed as a signed download link that expires in 24
hours. A workspace with more than 500,000 records can take 30-45 minutes.

If no email arrives, check the spam folder and confirm the export did not fail with ERR_5108,
which means the generated archive exceeded the 10 GB job limit. Narrow the date range and export
in parts.
