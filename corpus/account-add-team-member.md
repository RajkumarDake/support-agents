---
title: Adding a team member
category: account
---

# Adding a team member

Adding a team member invites someone into your workspace and gives them a role that decides what
they can see and change. This article covers how to add a member, what the person receives, when
the seat starts being billed, and what to do when the invite does not arrive or is refused.

## Who can add a team member

Only Owners and Admins can invite. Members and Viewers do not see the Invite member button at
all, and an API call to the invite endpoint from a Member token returns ERR_2031. If you cannot
find the button, check your own role first under Settings > Team - your role is shown next to
your name at the top of the list.

## Steps

1. Open Settings > Team.
2. Click Invite member in the top right.
3. Enter the email address. You can paste several comma-separated addresses to invite a batch.
4. Choose the role: Admin, Member or Viewer. Owner cannot be granted here - see
   account-transfer-ownership.
5. Optionally tick the projects the person should join immediately. Doing this now is worth the
   extra few seconds, because a new member who belongs to no project lands on an empty screen.
6. Click Send invitation.

The person appears in the team list straight away with the status `Invited`.

## What the invited person receives

They get one email with a single sign-up link. The invitation is valid for 7 days. If their
email domain matches a verified domain on the workspace they go straight in; otherwise they set
a password, or are redirected to your identity provider when SSO is enforced. See
onboarding-invite-flow for what the first screens look like from their side.

To resend, open Settings > Team, find the pending row, and use the overflow menu > Resend
invitation. Resending issues a new link and invalidates the old one, so tell the person to use
the newest email.

## Seats and billing

A pending invitation does not consume a seat and is not billed. The seat becomes active the
moment the invitation is accepted, and it is charged prorated for the remaining days of the
current billing period. The prorated amount appears on your next invoice as a
`Plan change adjustment` line rather than as a separate charge. billing-seat-pricing has the
full detail.

| Plan | Members included | Viewers | Per-seat price |
|---|---|---|---|
| Starter | 3 total | Count as a seat | $29/month flat |
| Pro | up to 25 | Count as a seat | $49/seat/month |
| Business | unlimited | Free, no seat used | $90/seat/month |
| Enterprise | unlimited | Free, no seat used | Contract |

## Edge cases and gotchas

- Inviting an address that already belongs to a member of the workspace is a no-op and shows
  "already a member".
- An address that has a pending invitation cannot be invited twice; resend instead.
- On Starter, the third member is the last one. The fourth invitation fails with ERR_2044 before
  the email is sent, so nothing is charged.
- Deactivated members still hold their seat until they are removed. See account-remove-member.
- If you want to hand a departing person's seat to someone else without paying twice, read
  account-seat-reassignment - remove first, then invite.

## Troubleshooting

**Symptom: "Seat limit reached" / ERR_2044.**
Every seat included in the plan is in use. Either remove an inactive member to free a seat, or
raise the plan under Settings > Plan. On Business and Enterprise, inviting the person as a Viewer
costs nothing and does not consume a seat.

**Symptom: "You do not have permission" / ERR_2031.**
You are signed in as a Member or Viewer. Ask an Owner or Admin to send the invitation.

**Symptom: the invitation email never arrives.**
Check the spam folder, then confirm the address has no typo in the team list. Corporate mail
filters are the usual cause; ask IT to allow our sending domain. As a workaround, copy the
invitation link from the overflow menu and send it over your own channel - the link is the same
one that was emailed.

**Symptom: the person clicks the link and is told it expired.**
Invitations last 7 days. Resend from Settings > Team.

**Symptom: they sign in but see nothing.**
They are not in any project yet. Add them to projects from Settings > Team > the person >
Projects, or from the project's own member list.

## Related error codes

- ERR_2044 - seat limit reached, the invitation was not sent.
- ERR_2031 - insufficient permissions, your role cannot invite.

## Related articles

- account-roles-permissions - what each role can actually do.
- account-remove-member - freeing a seat.
- billing-seat-pricing - how seats are counted and billed.
- onboarding-invite-flow - the new teammate's first experience.

## If this did not help

Send support the workspace name, the email address you tried to invite, and the exact error text
or code. If the invite was sent but never delivered, include the time you sent it so we can check
the delivery log.
