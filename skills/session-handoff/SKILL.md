---
name: session-handoff
description: >-
  Write a context-handoff .md file that captures everything a fresh Claude
  session needs to continue this work without re-deriving it. Use this whenever
  the user wants to preserve context before starting a new session — triggers
  include "summarize this conversation", "save context", "hand this off",
  "context dump", "I'm running low on context / hitting the limit", "write me a
  handoff", "so I can continue in a new chat", "pick up where we left off", or
  any request to carry the current work into a new session. Prefer this skill
  even when the user doesn't say the word "handoff" but the intent is clearly to
  not lose the thread across sessions. Do NOT use it for polished human-facing
  summaries, meeting minutes, or reports — this produces a working document
  aimed at the next AI session, not a deliverable for other people.
---

# Session Handoff

## What this is for

Long sessions accumulate expensive context: decisions and the reasoning behind
them, constraints the user stated once, dead ends already ruled out, the exact
state of half-finished work. Starting a new session throws all of that away. The
user then wastes the first ten minutes re-explaining, and you waste tokens
re-deriving conclusions you already reached.

This skill produces a single `.md` file whose sole job is to let a **fresh Claude
session** resume as if it had been here the whole time. The primary reader is the
next model, not a human — so favor density, precision, and unambiguous references
(exact paths, names, versions, IDs) over narrative polish. A human should still be
able to skim it, but never sacrifice a concrete detail to make a sentence read
nicely.

The failure mode to avoid: a vague recap that sounds complete but forces the next
session to ask "wait, what did we decide about X?" A good handoff answers those
questions before they're asked.

## The core judgment call

Most of the work is deciding **what's expensive to reconstruct** versus what's
cheap. Include the expensive stuff; cut the cheap stuff.

- **Expensive (always include):** decisions and *why* they were made, rejected
  alternatives and why they were rejected, constraints the user stated, gotchas
  discovered the hard way, the precise current state of unfinished work, and
  exact identifiers (file paths, function names, package versions, resource
  names, URLs, ticket IDs).
- **Cheap (cut or compress):** general knowledge the next session already has,
  blow-by-blow narration of how the conversation unfolded, restating things that
  are obvious from the files themselves, and pleasantries.

When in doubt about a decision, include the *reasoning*, not just the outcome —
the outcome is often recoverable from the files, but the reasoning is what took
the conversation to produce.

## Output structure

Write the file using this template. Keep section headers exactly as below so the
next session can navigate predictably. Omit a section only if it is genuinely
empty (e.g. no open questions) — and if you omit one, don't renumber the rest.

```markdown
# Handoff: <project / task name> — <YYYY-MM-DD HH:MM>

## TL;DR
<2–4 sentences: what this work is, where it stands right now, and the single
most important thing the next session should do first.>

## Goal
<What the user is ultimately trying to achieve. The success condition.>

## Current status
<Where things actually stand. What is done, what is in progress, what has not
been started. Be concrete about the state of in-progress work — "the migration
script is written and tested locally but not yet run against staging".>

## Decisions made (and why)
<The reasoning that would be expensive to reconstruct. For each meaningful
decision: what was decided, why, and — where it matters — what was rejected and
why. Bullet form is fine here.>

## Technical context & constraints
<Stack, environment, versions, config, credentials location (never the secrets
themselves), and any constraint the user stated: budget, compliance, deadlines,
"must stay on AWS", "avoid adding new dependencies", etc. Include gotchas
discovered during the session — things that will bite the next session if it
doesn't know them.>

## Open threads & next steps
<Prioritized. What is unfinished and what to do next, most important first. Be
specific enough to act on: not "fix the tests" but "the auth test in
tests/test_login.py::test_expired_token fails because the clock mock isn't
applied — needs freezegun or an injected clock".>

## Key files & artifacts
<Paths to files created or modified this session, each with a one-line note on
what it is and its state. Include the path to this handoff file's project folder
if relevant.>

## Open questions
<Anything unresolved that needs the user's input, or ambiguities the next
session should confirm before proceeding. Omit the section if there are none.>

## Resume prompt
<A short block the user can paste into a new session to bootstrap it, e.g.:
"Read <path-to-this-file> — it's the handoff from my last session. We're
continuing <task>. Start with <the top next step>.">
```

## Where to save it

Save to `OUTPUTS/<project>/` per the user's standing rule, where `<project>` is a
short, stable, kebab-case name derived from the work (e.g. `terraform-vpc-refactor`,
`q3-cost-report`). Reuse the exact project folder name if this conversation already
established one — consistency lets multiple handoffs for the same effort sit
together.

Name the file `handoff-<YYYY-MM-DD>.md`. If a handoff already exists for today in
that folder, append `-HHMM` so you never silently overwrite a prior handoff.

If no `OUTPUTS/` folder is reachable (no connected directory), fall back to the
working outputs folder and tell the user where you put it and that they should
move it somewhere durable.

## How to build it

1. **Scan the whole conversation, not just the end.** Constraints and decisions
   are often stated early and never repeated. A recency-biased summary misses
   them.
2. **Derive the project name** from the substance of the work, and check whether
   one was already established.
3. **Sort by reconstruction cost, not by chronology.** Lead with what would be
   hardest for a fresh session to recover.
4. **Use exact identifiers.** Every file path, function name, version number,
   resource name, and URL that matters should appear verbatim. Approximate
   references ("the config file") force the next session to go hunting.
5. **Never invent state.** If you're unsure whether something was completed, say
   so explicitly rather than asserting it's done. A confidently wrong handoff is
   worse than one that flags its own uncertainty.
6. **Keep secrets out.** Reference *where* credentials live, never the values.

## Quality bar

Before finishing, read the file back and ask: *if I started a brand-new session
with only this document, could I continue the work competently without asking the
user to re-explain anything expensive?* If any decision's rationale, any stated
constraint, or the true state of in-progress work is missing, add it. That test —
not length or polish — is what makes the handoff good.

After saving, tell the user the path and give them the one-line resume prompt so
they can paste it straight into the next session.