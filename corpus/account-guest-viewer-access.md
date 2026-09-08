---
title: Viewers, guests and free read-only access
category: account
---

# Viewers, guests and free read-only access

A Viewer can read and comment but cannot create, edit, upload or export. On Business and
Enterprise a Viewer is free and does not consume a seat, which makes it the right role for
clients, auditors, contractors and stakeholders who need visibility but not write access. On
Starter and Pro a Viewer occupies a normal billed seat, so the economics are different.

## Adding a Viewer

1. Settings > Team > Invite member.
2. Enter the email address.
3. Choose the role Viewer.
4. Tick the projects they should see. A Viewer with no projects sees an empty workspace, which
   is a common false alarm.
5. Send. The invitation behaves exactly like any other, valid for 7 days - see
   account-add-team-member.

Converting an existing person is the same dropdown used for any role change: Settings > Team >
the role dropdown > Viewer. On Business and Enterprise this frees their billed seat and issues a
credit on the next invoice.

## What a Viewer can and cannot do

Can: open projects they belong to, read content and attachments, download individual files,
comment, be mentioned, receive notifications, use the mobile app in read mode.

Cannot: create or edit anything, upload files, delete anything, run an export
(tech-data-export), see Billing or invoices, see Settings > Team management actions, create API
tokens, or manage integrations. Attempting any of these returns ERR_2031.

## Cost by plan

| Plan | Viewer cost | Notes |
|---|---|---|
| Starter | Consumes one of the 3 seats | No free tier; a Viewer costs the same as a Member |
| Pro | Consumes one of the 25 seats | Billed at $49/seat/month like any other |
| Business | Free, unlimited | Does not count toward the seat total |
| Enterprise | Free, unlimited | Fair-use limits may be set in the contract |

This is why an upgrade from Pro to Business sometimes pays for itself: ten read-only
stakeholders on Pro cost ten seats, and on Business cost nothing. Work it out on Settings > Plan
and usage before assuming Business is more expensive.

## Edge cases and gotchas

- Free Viewers are the first thing lost on a downgrade. Every Viewer becomes a billed seat at the
  moment a Business workspace drops to Pro, which can exceed the 25-member cap and block the
  downgrade entirely. See account-downgrade-plan.
- Viewers count toward nothing in billing but everything in access reviews. They appear in the
  audit log and in security questionnaires like anyone else.
- A Viewer can still be an SSO user and is subject to 2FA enforcement.
- Viewers can download files they can see. "Read-only" is not "cannot take a copy". If that
  matters, do not put the content in a project they belong to.
- There is no separate "guest" role. Use Viewer plus tight project membership.
- Mentions notify Viewers normally, so they can be pulled into a thread - see
  onboarding-notifications.

## Troubleshooting

**Symptom: a Viewer on Business is being billed.**
Check their actual role in Settings > Team. People are often invited as Member by mistake and
never corrected. Change the role and the credit appears on the next invoice.

**Symptom: ERR_2044 when inviting a Viewer.**
The workspace is on Starter or Pro, where Viewers do consume seats. Free the seat or raise the
plan.

**Symptom: the Viewer sees nothing after signing in.**
No project membership. Add them under Settings > Team > the person > Projects.

**Symptom: a Viewer needs to upload one file.**
There is no per-action exception. Raise them to Member for the moment, then lower them again -
on Business both changes are free.

**Symptom: ERR_2031 when a Viewer runs an export.**
Exports need Member or above. Ask a Member to run it and share the archive.

## Related error codes

- ERR_2031 - the Viewer role cannot perform the attempted action.
- ERR_2044 - seat limit reached on a plan where Viewers are billed.

## Related articles

- account-roles-permissions, account-add-team-member, billing-seat-pricing.

## If this did not help

Contact support with the workspace name and the list of people you want to give read-only access
to. If the aim is external sharing rather than internal read access, say so - the answer may be a
different feature entirely.
