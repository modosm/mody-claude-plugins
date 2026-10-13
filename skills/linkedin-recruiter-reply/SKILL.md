---
name: linkedin-recruiter-reply
description: "Triage a recruiter message (LinkedIn InMail, email, or DM) against Máté's rate floor, work-format filters and career goals, then draft a ready-to-send reply in his voice. Use whenever a recruiter approach is pasted in."
---

# Recruiter reply playbook

When a recruiter message is pasted in, produce three things: a verdict, a finished draft, and the honest read behind it. Do not ask clarifying questions first — triage, draft, then flag what needs checking.

## Current parameters

Read `~/github/mody-claude-plugins/config/recruiter-profile.local.md` first. It holds the rate floor, decline threshold, availability, base, career goal and the has / does-not-have tooling lists. It is gitignored, so it only exists on Máté's machines. If it is missing, stop and say so, pointing at `recruiter-profile.example.md` next to this file as the template; do not triage from guessed numbers.

## Step 1 — triage

Apply in order. The first hard fail decides it.

| Signal | Verdict |
|---|---|
| Permanent employment, or hybrid/office-based | Decline. Non-negotiable. |
| Day rate under the decline threshold | Decline. Not a haggle. |
| Requires relocation | Decline. |
| Remote B2B, at or above floor | Engage — draft a reply that takes the call |
| Remote B2B, rate not stated | Engage, and make them state their band first |
| Leadership scope (Head of / Director) | Engage even if the rate framing is unusual — different pricing world, reopen the number |

## Step 2 — how to handle the rate

The single most common mistake is naming a number at the wrong moment.

- **Name the floor figure** when the gap is so wide there is nothing to negotiate, or when declining. Stating it calibrates that recruiter for their next approach.
- **Do not name it** when the role is a live prospect and the client may pay above it. Ask what they have budgeted and let them go first. Opening at the floor anchors him at the floor of a range that may run higher.
- **Watch for nearshore pricing.** Consultancies with a Budapest or CEE delivery centre will instinctively price a Hungary-based contractor as nearshore rather than at London or New York rates. Name that dynamic in the read, not in the letter.
- When a number matters to the advice, search current market rates (ITJobsWatch for UK contract medians, TechPays for Hungarian permanent bands) rather than asserting one. Cite what you find and give the period it covers.

For a permanent role that needs a gross-equivalent comparison: Hungarian employee deductions are 33.5% (15% SZJA + 18.5% TB), so net = 66.5% of gross. Roughly 21 working days a month.

## Step 3 — never overclaim

A consultancy putting his CV in front of a client will get caught on an overclaim, and that costs him with that firm on every future role, not just the one in play.

Use the "Has" and "Does not have" lists from the profile file. If a JD names tooling not on the "has" list, either leave it out of the draft or state the gap plainly. Do not soften it into an implication. Declaring gaps directly reads as senior, not weak — write it that way.

Separate cheap gaps from expensive ones in the read. Swapping ArgoCD for Flux is a weekend; Kustomize is trivial with manifests; a new observability suite is query syntax and a UI. What is not cheap is depth — self-managed Kubernetes control-plane work (etcd, upgrades, cert rotation, CNI, node lifecycle) is a different skill from running EKS, and a JD that stresses "not just managed services" is screening for exactly that.

## Step 4 — career fit

Say whether the role moves him toward Director or not. A well-paid hands-on IC contract is a legitimate bridge between engagements — it just should not be booked as progression. Name it as income and continuity when that is what it is.

## Step 5 — write the draft

Read `~/github/mody-claude-plugins/config/anti-ai-writing-style.md` and follow it. Beyond that:

- Lead with the verdict or the blocker. No warm-up paragraph.
- Plain and direct, never brusque. He is turning down people he may want to hear from again.
- Put questions as questions, with the specific thing he needs to know (core hours, on-call, budgeted band) rather than a vague "tell me more".
- Every decline leaves the door open with a concrete condition attached — "if something comes up remote and at market rate" beats "keep me in mind".
- No bullet lists of his skills. Prose.
- Sign off `Best regards,\nMáté`.

Offer a shorter variant when the decline is clear-cut and the longer version risks over-explaining.

## Step 6 — deliver

Save to `OUTPUTS/linkedin-recruiter-replies/` with a version marker in the filename. Each new recruiter message appends a numbered section to a new version of the running file (`linkedin-recruiter-replies-v6.md` and so on) rather than overwriting the previous one.

Each section carries: the verdict, the draft, a **Before sending** list of anything he must verify or fill in, and the honest read (rate dynamics, fit, what the technical round will actually test).

In chat, show the draft and the read. Do not restate the file's contents twice.