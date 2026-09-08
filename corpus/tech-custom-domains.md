---
title: Custom domains
category: technical
---

# Custom domains

A custom domain lets your workspace be reached at an address you control, such as
`work.example.com`, instead of the default one we assign. It is available on **Business and
Enterprise**. Setup is a DNS change on your side plus a verification step on ours, and it takes
under an hour of work spread over however long your DNS takes to propagate.

## Before you start

- You need the Owner role, and access to the DNS for the domain.
- Choose a subdomain rather than an apex domain. Apex domains cannot carry a CNAME, and the
  workarounds vary by DNS provider.
- Decide in advance whether your identity provider configuration references the old hostname. It
  usually does - see the SSO note below.

## Setup

1. Open Settings > General > Custom domain.
2. Enter the hostname, for example `work.example.com`.
3. We show two DNS records: a `CNAME` pointing at our endpoint, and a `TXT` record for
   verification.
4. Add both at your DNS provider.
5. Click Verify. We check the records; propagation usually takes minutes but the TTL on your
   existing records governs it and can be up to 48 hours.
6. Once verified, we issue a TLS certificate automatically. This takes a few minutes and needs the
   CNAME to be live.
7. When the certificate is issued, the domain goes active. The default hostname continues to work
   and redirects to the custom one.

## Certificates

Certificates are issued and renewed automatically. Renewal happens well before expiry and requires
the CNAME to remain in place - removing it later causes renewal to fail and the domain to stop
working with no warning other than the email we send to the Owner.

You cannot upload your own certificate on Business. Enterprise contracts can arrange it.

## What changes once it is active

- Everyone uses the new address. The old one redirects, so bookmarks keep working.
- **SSO must be updated.** The Assertion Consumer Service URL in your identity provider changes
  to the new hostname. Update it before or immediately after the switch, or sign-in fails with
  ERR_1104. See tech-sso-saml.
- **Webhook endpoints are unaffected** - those are your URLs, not ours.
- **API base URL is unaffected.** The API keeps its own hostname regardless. See tech-api-keys.
- Invitation and notification emails link to the new address.

## Edge cases and gotchas

- Removing the DNS records does not release the domain in our configuration. Remove it in Settings
  > General > Custom domain too, or certificate renewal failures continue.
- A domain can be attached to one workspace at a time. Attaching it elsewhere requires removing it
  first.
- **A downgrade to Pro or Starter releases the custom domain** at the moment the downgrade lands,
  and everyone falls back to the default hostname. Update your identity provider again if you do
  this. See account-downgrade-plan.
- Deleting a workspace does not release the domain immediately; it is freed at the deletion date,
  14 days out. See account-close-workspace.
- Corporate proxies that pin certificates by hostname need updating too, see
  tech-browser-support.
- Custom domain changes are written to the audit log, see account-audit-logs.

## Troubleshooting

**Symptom: verification fails.**
The TXT record has not propagated, or your DNS provider appended the domain to a value that
already contained it, producing `_verify.work.example.com.example.com`. Check the record as
resolved, not as typed.

**Symptom: verified but the certificate never issues.**
The CNAME is missing or points somewhere else. Certificate issuance validates over the live
CNAME.

**Symptom: a certificate warning in the browser.**
Renewal failed, usually because the CNAME was removed or changed. Restore it; renewal retries
automatically.

**Symptom: SSO broke immediately after the switch.**
The ACS URL at your identity provider still points at the old hostname. Update it - the symptom
is ERR_1104.

**Symptom: the domain works for some people and not others.**
Cached DNS. It resolves for everyone once the old TTL expires.

**Symptom: the domain stopped working after a plan change.**
The workspace dropped below Business.

## Related error codes

- ERR_1104 - SSO assertion rejected, common after a hostname change.
- ERR_2031 - only the Owner can configure a custom domain.

## Related articles

- tech-sso-saml, account-downgrade-plan, account-close-workspace, tech-browser-support,
  account-audit-logs.

## If this did not help

Contact support with the workspace name, the hostname, and the output of a DNS lookup for the
CNAME and TXT records. Nearly every custom domain problem is visible in that lookup.
