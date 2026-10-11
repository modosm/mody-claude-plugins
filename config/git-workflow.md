# GIT WORKFLOW

These rules apply to both PRs (GitHub) and MRs (GitLab) — same rules, different name depending on platform.

## Rules
- Do not commit to the branch before requiring review first.
- Do not create a PR/MR. Wait for approval before creating a PR/MR.
- Commit messages must not mention that they were created with Claude.
- Commit messages must not contain a `Co-Authored-By: Claude ...` trailer.
- PR/MR descriptions must be short and focused on the reason for the change, not sprawling.
- PR/MR descriptions must not contain a `Co-Authored-By: Claude ...` trailer.

## Branch & commit conventions
- Branch naming: `<type>/<short-description>` (e.g. `feature/`, `fix/`, `chore/`, `refactor/`). Include the ticket/issue ref if one exists (e.g. `fix/JIRA-123-retry-logic`).
- Commit messages: imperative mood, concise subject line (~50 chars), body only if the "why" isn't obvious from the diff. No conventional-commit prefixes (`feat:`, `fix:`) unless the repo already uses that convention.
- Prefer small, focused commits over one large commit per branch.

## History & force-push rules
- Never force-push to a shared/protected branch (`main`, `master`, `develop`, or any branch others may be working on).
- Never rewrite history (rebase, amend, squash) on commits already pushed to a shared branch without explicit confirmation first.
- Confirm before any interactive rebase, `reset --hard`, or `git clean` — these are destructive and irreversible for uncommitted/unpushed work.

## Review & approval rules
- Always show the diff (`git status` / `git diff`) before committing so it can be reviewed.
- Never push directly to protected branches (`main`, `master`, `develop`) — always via a branch + PR/MR.
- Wait for explicit approval (not just silence) before committing or creating a PR/MR.
