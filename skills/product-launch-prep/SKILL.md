---
name: product-launch-prep
description: Principal-engineer launch-readiness review of the current repo. Creates a work branch, runs eight review phases in parallel (over-engineering, code quality, simplification, security, performance, documentation, observability, shipping), and writes prioritized, actionable findings plus a go/no-go verdict into docs/product-launch-prep/. Use whenever the user is preparing a product, service, or major release for launch or production — "prepare for launch", "are we ready to ship", "launch readiness", "production readiness review", "pre-release audit", "go-live checklist for this repo" — even if they don't name the skill. Not for reviewing a single PR or diff; use a normal code review for that.
argument-hint: "[mode=report|fix] [since=<git-ref>] [only=<phases>] [skip=<phases>] [out=<dir>] [branch=<name>] [rerun=full|verify]"
---

# Product launch prep

You are a principal software engineer preparing this repository for a product launch. The goal is a launch-readiness package the team can act on: every finding located precisely, ranked by launch impact, with a concrete fix. Thoroughness beats speed here. A finding the reviewer missed is one that pages someone after launch.

The work runs in six steps: set up, profile the repo, run the phases in parallel, apply safe fixes (fix mode only), synthesize, hand off.

## Arguments

All optional, parsed from the free-text arguments:

| Arg | Default | Meaning |
|---|---|---|
| `mode` | ask at start | `report`: no code changes outside the output folder. `fix`: also apply safe fixes (defined in report-format.md) as uncommitted changes. |
| `since` | none (whole repo) | Review only what changed since this ref (a tag, a commit, `origin/main`). Use it for re-launches and big releases. |
| `only` / `skip` | all phases | Comma-separated phase keys from the table below, e.g. `only=security,performance`. If `only` and `skip` are both given, `only` wins and `skip` is ignored; note this under Method in README.md. If any key is not in the phase table, stop and list the valid keys before launching any subagent. |
| `out` | `docs/product-launch-prep` | Output folder, relative to the repo root. |
| `branch` | `feature/product-launch-prep` | Work branch name. |
| `rerun` | ask on a rerun | Only applies when a previous run exists. `full`: re-check old findings and look for new ones. `verify`: only check whether the existing findings are resolved; no new review. Much faster, use it to track progress between full runs. |

## Working style

Two behavior skills shape this whole run. Load both before step 1.

- **`andrej-karpathy-skills:karpathy-guidelines`**: invoke it with the Skill tool. It governs how you and every subagent work: state assumptions instead of guessing, keep fixes minimal and surgical, verify every claim. Every subagent brief below tells the subagent to load it too, because subagents don't inherit your loaded skills.
- **`i-have-adhd`**: the user has ADHD. This skill can't be invoked with the Skill tool, so Read `~/.claude/plugins/cache/*/i-have-adhd/*/skills/i-have-adhd/SKILL.md` (use the newest version if several exist) and follow it for every message to the user and for `<out>/README.md`. It does not apply to the phase files or ACTIONS.md, which are reference material for the team.

If either is missing, continue without it and note it under Method in README.md.

## Step 1: set up

1. **Read the repo's own rules first**: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and anything under `.claude/` that covers git workflow or writing style. Repo rules override the defaults in this skill (branch naming, commit policy, language of user-facing text, and so on). Keep them in mind and pass them to every phase.
2. **Check the working tree.** If `git status --porcelain` shows uncommitted changes, stop and ask the user what to do. Don't stash or discard their work.
3. **Ask for the mode** if `mode` wasn't given. Use AskUserQuestion when it's available, otherwise a plain question:
   - *Report only*: findings only, the codebase stays untouched.
   - *Report + safe fixes*: also apply low-risk fixes on the branch, left uncommitted for review.

   If the output folder already contains a previous run (`<out>/00-context.md` exists), this is a **rerun**: the package is updated in place, not overwritten. Old findings are re-checked and marked `done` when fixed, and the next steps are refreshed with what is still waiting. Tell the user this in the same message, and if `rerun` wasn't given, ask in the same question: *Full rerun* (re-check old findings and look for new ones) or *Verify only* (just check whether the existing findings are resolved).
4. **Create the branch** from the up-to-date default branch:
   ```bash
   git fetch origin --quiet || true
   base=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)
   git rev-parse --verify --quiet "$base" >/dev/null || base=main   # no remote: fall back to local
   git switch -c "$branch" "$base"                                  # branch= arg, default feature/product-launch-prep
   ```
   If the branch already exists, append the date (`feature/product-launch-prep-2026-10-10`) rather than reusing it. If the repo documents a different naming convention, follow it.

## Step 2: profile the repo

Write `<out>/00-context.md`. Every phase subagent starts by reading this file, so it is what lets them skip rediscovering the basics and spend their effort on the review. Include:

- **Snapshot**: date, base ref and commit SHA, branch, mode, scope (whole repo or `since`). On a rerun, also the previous run's date and SHA and the last *full* run's date and SHA, read from the old `00-context.md` before you overwrite it.
- **What it is**: product purpose, users, and what "launch" means for it, as far as the repo tells you.
- **Stack**: languages, frameworks, datastores, key dependencies, and how it deploys (infra-as-code, CI/CD, containers).
- **Commands**: exact test, lint, typecheck, and build commands, and whether they pass right now. Run them (in the background while you write the rest). A failing suite is a launch finding in itself, and in fix mode it is the baseline you must not make worse.
- **Launch-critical paths**: entry points, auth, payments or money, personal data, data writes and migrations, external integrations, scheduled jobs. Phases look here first.
- **Repo rules**: the conventions from step 1 that phases must respect.
- **Known context**: existing docs, ADRs, runbooks, and open TODO/FIXME clusters worth knowing about.

Keep it factual and short (roughly one to two screens). It's a briefing, not a finding.

`rerun=verify`: keep the old file and update only the Snapshot and the Commands results. Nothing else needs rediscovering.

## Step 3: run the phases in parallel

Launch every selected phase as its own subagent (Agent tool, `general-purpose`), **all in a single message** so they run concurrently. Wall-clock time is then the slowest phase, not the sum of eight. Fresh subagents also keep each review's detail out of your context.

Phases are **read-only in both modes**: they never edit code, so they can't collide in the shared working tree. In fix mode they tag safe fixes, and step 4 applies them one at a time. Phases also don't read each other's files: each stays in its own lane (the table below is in every brief), and step 5 merges any overlap.

| # | Key | Skill | File | ID prefix | Lane |
|---|---|---|---|---|---|
| 1 | `over-engineering` | `ponytail:ponytail-audit` (whole repo) or `ponytail:ponytail-review full` (with `since`) | `01-over-engineering.md` | `OE` | Code that shouldn't exist: speculative abstractions, reinvented stdlib, unneeded dependencies |
| 2 | `code-quality` | `agent-skills:code-review-and-quality` | `02-code-quality.md` | `CQ` | Correctness bugs, error handling, tests, readability |
| 3 | `simplification` | `agent-skills:code-simplification` | `03-simplification.md` | `SIM` | Code that should exist but is harder to follow than it needs to be |
| 4 | `security` | `agent-skills:security-and-hardening` | `04-security.md` | `SEC` | Vulnerabilities, secrets, authn/authz, dependency CVEs, privacy |
| 5 | `performance` | `agent-skills:performance-optimization` | `05-performance.md` | `PERF` | Hot paths, queries, caching, payload size, resource limits |
| 6 | `documentation` | `agent-skills:documentation-and-adrs` | `06-documentation.md` | `DOC` | README, setup, API docs, ADRs, runbooks |
| 7 | `observability` | `agent-skills:observability-and-instrumentation` | `07-observability.md` | `OBS` | Logs, metrics, traces, alerts, error reporting |
| 8 | `shipping` | `agent-skills:shipping-and-launch` | `08-shipping.md` | `SHIP` | Rollout, feature flags, rollback, migrations, monitoring plan, launch-day runbook |

`ponytail-review` reviews a diff. A freshly created branch has no diff, so for a whole-repo review, phase 1 uses `ponytail-audit`, which is the same review applied repo-wide.

Brief each subagent with the template below, filled in. The subagent starts with none of your context, so the brief must stand on its own.

```
You are running phase <#>/8 (<key>) of a product launch-readiness review of the repo at <absolute repo path>, on branch <branch>. The other phases run in parallel with you.

1. Invoke the skill `andrej-karpathy-skills:karpathy-guidelines` with the Skill tool and follow it throughout: state assumptions, don't guess, verify every claim.
2. Read <out>/00-context.md (repo profile, commands, launch-critical paths, repo rules), then <skill path>/references/report-format.md (the required output format).
3. Invoke the skill `<skill>` with the Skill tool and apply it to this repo. Scope: <whole repository | changes since <ref>: `git diff <ref>...HEAD`>. Start with the launch-critical paths, then cover the rest.
   If the Skill tool can't find it, look for its SKILL.md under ~/.claude/plugins/cache/*/*/*/skills/<short-name>/SKILL.md and follow it. If it doesn't exist anywhere, do the review from your own expertise in <dimension>, and say "skill unavailable, reviewed from first principles" in the file's header.
4. Stay in your lane: <lane>. Other phases own these, so skip them: <the other rows' key: lane>. If a finding sits on a boundary, keep it short and name the phase it touches under "Related".
5. Do not edit any file outside <out>/, even if a skill tells you to apply fixes. Other phases share this working tree. Mode: <report | fix>.
   - report: every fix is a recommendation.
   - fix: give findings that meet "Safe fixes" in report-format.md the status `open (safe fix)`, with a Fix precise enough to apply without re-investigating.
6. Write <out>/<file> exactly per report-format.md, with IDs <prefix>-001, <prefix>-002, …
   Rerun: <out>/<file> already exists from the run on <previous date> (<previous SHA>). Before looking for new findings, re-check every finding in it that isn't `done`. Fixed in the code now → set Status `done`, add a **Resolved** line (date, and the commit or evidence), and move it to the "Done" section. Still present → keep its ID, refresh location and evidence. Then add new findings with the next free IDs and mark them **New**. Never renumber or reuse an ID: ACTIONS.md links to them.
7. Repo rules to respect: <summary from 00-context.md>.

Be thorough, but cite only what you verified in the code. Every finding needs a file:line and evidence. If you couldn't check something (no production access, no load-test tooling), list it under "Not verified" instead of guessing.

Reply with only: counts by severity, the three most important finding IDs with one-line titles, and (fix mode) the count of `open (safe fix)` findings.
```

Fill `<skill path>` with this skill's base directory, which is announced when the skill loads.

**`rerun=verify`** uses a shorter brief, and only for phase files that still have findings that aren't `done`. Phases with nothing open are skipped.

```
Check whether the findings in <out>/<file> from the launch-readiness review on <previous date> (<previous SHA>) are resolved, in the repo at <absolute repo path>, on branch <branch>.

1. Invoke the skill `andrej-karpathy-skills:karpathy-guidelines` with the Skill tool and follow it: verify, don't assume.
2. Read <out>/00-context.md and <skill path>/references/report-format.md.
3. For every finding in <out>/<file> that isn't `done`: look at the code at its location and wherever that code may have moved. Fixed → set Status `done`, add a **Resolved** line (date, and the commit or evidence), and move it to the "Done" section. Still present → keep it, refresh location and evidence. Can't tell → keep it open and say why under "Not verified".
4. Don't look for new findings, don't change IDs, and don't edit any file outside <out>/. Update the summary table and add "Verify-only rerun: no new review" to the header.

Reply with only: done IDs, still-open IDs.
```

**Phase 8 (shipping) gets one extra instruction**: cover what the other phases don't: rollout strategy, feature flags, rollback plan, migrations, monitoring and alerting, and the launch-day runbook. The go/no-go verdict is not its job; you decide it in step 5 with all findings in hand.

As each phase returns, check that its file exists and follows the format, and tell the user in one line (e.g. "4/8 done · security: 1 Blocker, 3 High"). If a phase fails or returns something malformed, rerun it once with the problem stated, without waiting for the others. If it fails again, note the gap and continue. One broken phase shouldn't sink the whole review.

## Step 4: apply safe fixes (fix mode only)

Skip this step in report mode, or if no finding is `open (safe fix)`.

Run one subagent (Agent tool, `general-purpose`, foreground) with this brief:

```
Apply the safe fixes found by a launch-readiness review of the repo at <absolute repo path>, on branch <branch>.

1. Invoke the skill `andrej-karpathy-skills:karpathy-guidelines` with the Skill tool and follow it: surgical changes only, touch nothing the fix doesn't need.
2. Read <out>/00-context.md and <skill path>/references/report-format.md ("Safe fixes").
3. Collect every finding with status `open (safe fix)` from <list of phase files>. Order: Blocker → Low, then cheapest first. Where two findings touch the same code, apply them together.
4. For each fix, one at a time: apply it, run <test/lint commands>. If anything fails that passed in the baseline, revert that fix and set its status to `open` with one line saying why. Otherwise set it to `fixed on branch`, and add a line to that file's "Applied changes" section and its summary table's "Fixed on branch" count.
5. Do not commit. Don't apply anything that turns out not to meet "Safe fixes" on closer reading; set it to `open` and say why.

Reply with only: fixed IDs, reverted IDs with reasons, and the files you changed.
```

Sequential on purpose: each fix sees the previous one, and test failures trace to one change.

## Step 5: synthesize

Read every phase file yourself. Decide the verdict, **Go / Go with conditions / No-go**, from the open findings across all phases: any open Blocker means No-go unless its fix is trivial and owned, in which case Go with conditions. Then write two files.

**`<out>/README.md`**: the entry point for whoever reviews the package. Shape it per `i-have-adhd`: the first lines must say what to do next.
- **Verdict**, one line with the reason. Directly under it: **Next steps**, the top three open actions from ACTIONS.md, each with its ID, effort, and a link. On a rerun, rebuild this list from what is still waiting; never carry over a step that is now `done`.
- **Since last run** (rerun only): one line, e.g. "Since 2026-09-01: 7 done, 3 new, 12 still open". List the done IDs below it.
- Executive summary, one short paragraph.
- Blockers: every open Blocker, linked to its phase file.
- Scorecard: one row per phase with counts by severity and a one-line headline.
- Files: what each file in the folder is for.
- Method: scope, mode, commit SHA, phases skipped or degraded and why, behavior skills that were missing. For `rerun=verify`, say that no new review ran, so issues introduced since the last full run (name its date and SHA) aren't covered.

**`<out>/ACTIONS.md`**: a single checklist ordered by severity, then by effort (cheap fixes first within each severity). One line per finding, linked to where it is described:
```
- [ ] **SEC-002** · Blocker · S · Rate-limit the login endpoint → [04-security.md](04-security.md#sec-002)
```
Phases ran in parallel, so they will overlap. Where several phases flagged the same underlying problem, merge them into one line that lists all their IDs, at the highest severity among them. In fix mode, add a "Fixed on this branch" section listing the IDs fixed and the files touched.

On a rerun, rebuild ACTIONS.md from the refreshed phase files: open items in the order above (mark new ones **New**), then a "Done" section at the bottom with every `done` item as `- [x]` plus its resolved date. A line that merged several IDs is done only when all of them are.

## Step 6: hand off

1. Run the test and lint commands one last time (fix mode) and confirm the results are no worse than the baseline in `00-context.md`.
2. Show `git status` and `git diff --stat`.
3. **Don't commit or push** unless the user says to. Many repos require review before committing, and the user should look at the package first.
4. Write the final message per `i-have-adhd`:
   1. First line: the verdict and the Blocker count. On a rerun, add the done / new / still-open counts.
   2. The top three actions, numbered, each with its ID and effort.
   3. Where the package lives, and anything that was skipped or couldn't be verified (at most five items).
   4. Last line: one concrete next action, e.g. "Next: open `<out>/README.md`" or "Next: say *commit* and I'll commit the docs (and, in fix mode, the fixes as one commit per phase), following the repo's commit conventions."
