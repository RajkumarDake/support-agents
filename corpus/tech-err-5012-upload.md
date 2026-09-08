---
title: ERR_5012: upload rejected
category: technical
---

# ERR_5012: upload rejected
ERR_5012 means the upload was rejected by the storage service before it finished. The three
causes, in the order you should check them:

1. The file is larger than the plan limit (100 MB on Starter, 2 GB on Pro and Business).
2. The file type is not on the allow list. Executables, archives with nested archives, and
   files with no extension are rejected.
3. The upload token expired. Tokens are valid for 15 minutes; a paused or resumed upload on a
   slow connection can outlive its token.

Retrying a fresh upload fixes cause 3. Causes 1 and 2 need the file changed or the plan raised.
