---
title: Setting up integrations
category: onboarding
---

# Setting up integrations

Integrations connect the workspace to the other tools your team already uses. They are configured
once by an Owner or Admin, owned by the workspace rather than by the person who set them up, and
revocable from the same screen.

## What is available

| Integration | What it does | Scopes requested |
|---|---|---|
| Slack | Posts notifications to channels, unfurls links | channel read, chat write |
| GitHub | Links items to issues and pull requests | repo read, webhook |
| Jira | Two-way link between items and issues | project read, issue write |
| Zendesk | Attaches support tickets to items | ticket read |
| Google Workspace | Attaches Drive files, syncs calendar events | drive read, calendar read |

Anything else is built against the API - see tech-api-keys and tech-webhooks.

## Connecting one

1. Open Settings > Integrations. Owner and Admin only; Members and Viewers get ERR_2031.
2. Click Connect next to the integration.
3. You are redirected to that service to authorise. Read the scopes - each integration asks only
   for what it needs.
4. Approve, and you are returned to Settings > Integrations with the integration listed as
   Connected.
5. Configure the specifics: which Slack channels, which GitHub repositories, which Jira projects.

## Who owns the connection

An integration is owned by the workspace, not by the person who connected it, so it keeps working
after that person leaves the workspace. Removing them from the team does not break it - see
account-remove-member.

It does **not** keep working if the granting account loses access on the other side. If the
person who authorised the Slack connection is deprovisioned from Slack, the OAuth token is
revoked upstream and we start returning ERR_6015. This is the most common integration failure and
it is why you should authorise with a service account or a long-lived admin account rather than
whoever happened to be setting things up. See tech-integrations-troubleshooting.

## Disconnecting

Settings > Integrations > the integration > Disconnect. This revokes our token on that side and
stops all traffic in both directions. Reconnecting later requires going through the OAuth flow
again; nothing is remembered.

Disconnecting does not delete anything already brought into the workspace. Linked issues stay
linked as plain references.

## Edge cases and gotchas

- Integrations do not consume seats and do not count as members.
- Integration traffic counts against your API allowance in some cases; a chatty Jira sync on
  Starter can contribute to ERR_4029. Check Settings > Plan and usage, see
  account-plan-and-usage.
- Connecting an integration does not change notification settings. If Slack is suddenly noisy,
  that is configured per channel in the integration, and separately per person under Settings >
  Notifications - see onboarding-notifications.
- Some scopes cannot be granted by a non-admin on the other service. If the OAuth screen offers
  fewer options than expected, an administrator of that service must approve it.
- Connections, disconnections and scope changes are written to the audit log, see
  account-audit-logs.
- Downgrading a plan does not disconnect integrations, but a workspace that goes read-only stops
  writing to them.

## Troubleshooting

**Symptom: ERR_6015 "integration token revoked".**
The OAuth token was revoked upstream, usually because the granting account lost access on the
other side. Reconnect from Settings > Integrations and grant the scopes with an account that will
stay active.

**Symptom: ERR_2031 when connecting.**
You are a Member or Viewer. Integrations are Owner and Admin only.

**Symptom: the OAuth flow completes but nothing happens.**
The scopes were reduced during approval. Disconnect and reconnect, approving everything asked
for.

**Symptom: events stop appearing without any error.**
Check whether the integration relies on a webhook endpoint that has been marked unhealthy after
six failed deliveries, which raises ERR_6002 - see tech-webhooks.

**Symptom: duplicate posts in Slack.**
Two channels are configured for the same event, or the workspace is connected twice. Check the
integration's channel configuration.

## Related error codes

- ERR_6015 - integration token revoked upstream.
- ERR_6002 - webhook endpoint unhealthy.
- ERR_2031 - insufficient permissions.
- ERR_4029 - rate limit or API allowance exhausted.

## Related articles

- tech-integrations-troubleshooting, tech-webhooks, tech-api-keys, onboarding-notifications,
  onboarding-first-week.

## If this did not help

Contact support with the workspace name, the integration, the error code, and the time it last
worked. If the token was revoked on the other side, the fix is on that side and we will tell you
exactly what to ask their administrator for.
