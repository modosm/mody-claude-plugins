# Phase report format

Every phase file uses this structure, so the package reads as one document and the synthesis step can merge the files without guessing.

## Severity

Rank by **launch impact**, not by how interesting the finding is.

| Severity | Meaning | Examples |
|---|---|---|
| **Blocker** | Launching with this open risks a data breach, data loss, an outage, legal exposure, or a broken core flow. Fix before launch. | Auth bypass, secrets in the repo, unbounded query on the hot path, no rollback for a destructive migration, failing test suite |
| **High** | Likely to cause incidents or real user pain soon after launch. Fix before launch, or accept the risk explicitly with an owner. | Missing rate limit on login, N+1 query on a list endpoint, errors swallowed with no logging, no alert on the main failure mode |
| **Medium** | Real cost, but it won't bite on launch day. Schedule it soon after. | Duplicated business logic, missing index on a growing table, an undocumented ops procedure |
| **Low** | Polish and hygiene. | Naming, dead code with no runtime effect, comment drift |

When unsure between two levels, pick the higher one and say why in "Why it matters". Inflating everything to Blocker makes the list useless, so a Blocker must name the concrete failure it would cause.

**Effort**: `S` (under an hour), `M` (under a day), `L` (more than a day, or needs a design decision).

## File template

```markdown
# <NN> · <Phase title>

> Skill: `<skill name>` · Scope: <whole repo | since <ref>> · Mode: <report | fix> · Commit: <short SHA>
> <"skill unavailable, reviewed from first principles", only if that applies>

## Summary

<2–4 sentences: overall state of this dimension and the single most important thing to do.>

| Blocker | High | Medium | Low | Fixed on branch |
|---|---|---|---|---|
| 0 | 2 | 5 | 3 | 1 |

## Findings

### SEC-001 · High · Login endpoint has no rate limiting

- **Where**: `routes/api.php:42`, `app/Http/Controllers/AuthController.php:18-35`
- **Evidence**: <what you saw: a short code excerpt, the command output, or the config value>
- **Why it matters**: <the concrete failure at launch, e.g. credential stuffing locks out real users and burns DB CPU>
- **Fix**: <specific change: what to add or edit and where; a short snippet if it helps>
- **Effort**: S
- **Status**: open | open (safe fix) | fixed on branch | needs decision | done
- **New** / **Resolved**: <rerun only: "New" on findings first seen in this run; "Resolved: <date>, <commit or evidence>" on done ones>
- **Related**: <IDs from other phases, if any>

<…more findings, ordered Blocker → High → Medium → Low…>

## Done

<Rerun only: findings from earlier runs that are now fixed, as full finding blocks with Status `done` and a Resolved line, so their anchors keep working. Write "None" on a first run.>

## Applied changes

<Write "None". In fix mode, the fix step (SKILL.md step 4) replaces it with one line per applied change, as "ID: file(s), what changed".>

## Not verified

<What this phase couldn't check and what it would take: production metrics, load testing, a third-party console, secrets in the deployment environment. Write "Nothing" if everything was checked.>

## What's already good

<Up to five things done well that should be kept. This stops someone "fixing" them later. Keep it short.>
```

Rules that keep findings actionable:

- **One problem per finding.** If the same pattern shows up in twelve files, write one finding that lists every location (or the first five and a count), not twelve findings.
- **Precise locations.** Give `path:line` or `path:start-end`. Use paths relative to the repo root.
- **Show evidence.** "Might be vulnerable" isn't a finding. Either show the vulnerable code path or put it under "Not verified".
- **Concrete fixes.** "Improve error handling" isn't a fix. "Wrap the S3 call in `try`, log at error level with the request ID, and return 502" is.
- **Anchors**: the heading `### SEC-001 · …` renders an anchor like `#sec-001--high--…`. In ACTIONS.md, link to the file plus the ID, as in `04-security.md#sec-001`. That's close enough to find, and it survives title edits.

## Safe fixes (fix mode only)

Phases only tag safe fixes as `open (safe fix)`; the fix step applies them afterwards, one at a time. A fix is safe only when all of these hold:

- It doesn't change behavior, or it fixes something that is unambiguously a bug with an obvious correct fix.
- It is local: a few files, no change to a public API, wire format, or database schema.
- The existing tests and linters still pass afterwards.

Typical safe fixes: deleting dead code, adding missing input validation that mirrors existing patterns, adding logging or metrics at an obvious seam, fixing doc drift, and tightening an over-broad CORS or header config when the intended value is clear from the repo.

Always report-only, even in fix mode: database migrations, infra-as-code, auth and permission logic, money calculations, dependency upgrades with breaking changes, and anything that needs a product decision. Mark them `needs decision` when they depend on a choice someone has to make.
