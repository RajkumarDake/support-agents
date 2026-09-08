---
title: Downgrading your subscription
category: account
---

# Downgrading your subscription

Downgrading moves the workspace to a cheaper plan - Enterprise to Business, Business to Pro, or
Pro to Starter. Unlike an upgrade, a downgrade does not take effect
immediately: you keep the higher plan and its features until the end of the current billing
period, and the saving arrives as account credit rather than as money back. The important part of
this article is the list of things that stop working the moment the downgrade lands, because
several of them need action beforehand.

## Steps

1. Open Settings > Plan.
2. Click Change plan and choose the lower tier.
3. The confirmation screen lists everything that will be lost, and the date it happens - the end
   of your current period, not today.
4. Reduce seats and usage below the target plan's limits if the screen says you are over. You
   cannot schedule a downgrade that the workspace would not fit into.
5. Confirm.

Owner only. Admins can read the plan screen but not change it - see account-roles-permissions.
A banner shows the scheduled change until it applies; the Owner can cancel it any time before
then from the same screen.

## Money

Downgrades are never refunded pro rata. The difference becomes account credit, applied
automatically to the next invoice and visible under Billing > Credits. Credit cannot be
transferred between workspaces, is not redeemable for cash, and is forfeited if the workspace is
closed. refund-downgrade-credit covers this in full, and billing-proration explains why upgrades
behave differently.

Annual plans do not downgrade mid-term. The change is queued for the renewal date.

## What you lose at each step down

**Business or Enterprise to Pro**
- SSO and SAML enforcement stops. Everyone signs in with a password again, so make sure people
  have one before the date - see account-password-reset and tech-sso-saml.
- SCIM provisioning stops syncing (account-scim-provisioning).
- Free Viewer seats end. Every Viewer becomes a billed seat, which can push you over the Pro cap
  of 25 - see account-guest-viewer-access.
- The audit log screen disappears and no new entries are written. Export first
  (account-audit-logs).
- Workspace-wide 2FA enforcement is turned off. Individual 2FA is untouched.
- Session policy reverts to defaults (account-session-timeout).
- Custom domains are released (tech-custom-domains).
- Storage drops from 1 TB to 250 GB and API allowance from 2,000,000 to 600,000 calls.
- Service credits for outages no longer apply (refund-outage-credit).

**Pro to Starter**
- Members are capped at 3. Remove people first or the downgrade cannot be scheduled.
- Per-file uploads drop from 2 GB to 100 MB, storage from 250 GB to 10 GB.
- API drops to 60 requests per minute and 60,000 calls per period.
- The mobile app becomes read-and-comment only (onboarding-mobile-app).

## Being over the limit on the new plan

If storage is over the new limit when the downgrade lands, the workspace does not delete
anything. It goes into a soft-capped state: existing files stay readable, and new uploads are
rejected with ERR_5140 until you are back under. See tech-storage-quota. Seats are the exception -
those must be resolved before the downgrade is accepted at all.

## Edge cases and gotchas

- Downgrading is not cancelling. If you want to stop paying entirely, see refund-cancellation.
- A scheduled downgrade plus a mid-period upgrade cancels the downgrade. Check the banner.
- If the workspace is past due, the downgrade is queued behind the outstanding invoice - see
  billing-payment-failed.
- Exports started before the downgrade complete under the old limits; exports started after are
  subject to the new ones.

## Troubleshooting

**Symptom: "Reduce your team before downgrading".**
You have more members than the target plan allows. Remove or convert to Viewer where the target
plan supports free Viewers, then retry.

**Symptom: the price did not drop on the very next invoice.**
The change applies at the period boundary, and the saving arrives as a credit line. Check
Billing > Credits.

**Symptom: SSO stopped working and nobody can sign in.**
The downgrade landed. Users need passwords; have each of them use Forgot password.

**Symptom: you changed your mind after the date.**
Upgrade again. It takes effect immediately and is prorated, but anything purged by the lower
plan's limits - audit entries in particular - does not come back.

## Related error codes

- ERR_5140 - storage over the new plan's quota.
- ERR_2044 - too many seats for the target plan.
- ERR_2031 - only the Owner can change the plan.

## Related articles

- billing-proration, refund-downgrade-credit, refund-cancellation.

## If this did not help

Contact support with the workspace name, the plan you are on, the plan you want, and the date you
need it to happen. If you are downgrading because of a cost problem rather than a feature one,
say that - there are usually cheaper answers than losing a tier.
