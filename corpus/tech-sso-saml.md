---
title: SSO and SAML sign-in problems
category: technical
---

# SSO and SAML sign-in problems
The two errors we see most are a clock skew over five minutes between your identity provider and
our servers, and an assertion that does not include the `email` attribute. Both surface as
ERR_1104.

SSO is available on Business and Enterprise. When SSO is enforced, password sign-in is disabled
for everyone except break-glass admin accounts, which should have their recovery codes stored
offline.
