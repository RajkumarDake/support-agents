---
title: Importing your data
category: onboarding
---

# Importing your data
Settings > Import accepts CSV and JSON up to 200 MB per file. The importer validates the whole
file before writing anything, so a failed import changes nothing.

Column headers must be unique and non-empty. Dates are parsed as ISO 8601; anything else is
rejected with the row number. Large imports run in the background and email you when done.
