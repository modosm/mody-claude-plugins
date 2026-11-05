# Publishing rules

This repo is public on GitHub. Anything committed is world-readable, and a commit pushed once stays in history even after it is reverted.

- Private values (rates, salary, health, diet, body metrics, addresses, tokens, keys) live only in `*.local.*` files (e.g. `*.local.md`, `*.local.json`). `.gitignore` covers that pattern. Never `git add -f` them.
- A skill that needs private values reads them from `config/<name>.local.md` and ships a template as `<name>.example.md` next to its SKILL.md. Templates use `<placeholders>`, never real numbers.
- A new private file must have `.local.` in its name and must not end in `.example`. Check with `git check-ignore -v <path>` before relying on it.
- Never copy values from a `.local` file into a SKILL.md, README, example, script, test fixture, or commit message.
- Before every commit, read `git diff --cached` for personal data or secrets. If you find any, stop and tell me instead of committing.
- `main` has a ruleset: changes land via PR only, no force-push, no deletion. Secret scanning push protection is on, but it only catches credentials, not personal data. The rules above cover that.
