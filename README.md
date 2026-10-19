# mody-claude-plugins

Personal Claude Code plugin `mody`. Each skill is invoked as `/mody:<skill>` in any repo.

| Skill | What it does |
|---|---|
| `product-launch-prep` | Launch-readiness review: branch, 8 parallel review phases, findings + go/no-go in `docs/product-launch-prep/` |
| `linkedin-recruiter-reply` | Triage a recruiter message against my rate floor, work format and career goals, then draft the reply. Reads private numbers from `config/recruiter-profile.local.md` (gitignored; on a new machine copy `skills/linkedin-recruiter-reply/recruiter-profile.example.md` there and fill it in) |
| `session-handoff` | Write a handoff `.md` so a fresh session can pick up the work without re-deriving it |

## Install (once per machine)

```bash
claude plugin marketplace add modosm/mody-claude-plugins
claude plugin install mody@mody
```

`product-launch-prep` delegates to four other user-scope plugins; install them too:

```bash
claude plugin marketplace add https://github.com/DietrichGebert/ponytail.git && claude plugin install ponytail@ponytail
claude plugin marketplace add addyosmani/agent-skills && claude plugin install agent-skills@addy-agent-skills
claude plugin marketplace add forrestchang/andrej-karpathy-skills && claude plugin install andrej-karpathy-skills@karpathy-skills
claude plugin marketplace add ayghri/i-have-adhd && claude plugin install i-have-adhd@i-have-adhd
```

Missing ones degrade gracefully (the phase runs from first principles and says so).

## Session-start hook

`hooks/hooks.json` tells Claude, on every new session (and `/clear`), to load `ponytail`, `karpathy-guidelines` and `using-agent-skills` via the Skill tool before its first reply. `i-have-adhd` disables model invocation, so the hook `cat`s its SKILL.md into context instead. Claude's first reply opens with a "Skills loaded: ..." line and names any skill that failed to load. Edit the list there.

## User config

`config/` holds my user-scope Claude Code config:

- `settings.json`: plugins, marketplaces, model, permissions, sandbox. Committed.
- `settings.local.json`: personal values (the local `mody` marketplace path). Gitignored. Wins over `settings.json`.
- `CLAUDE.md`: global instructions. `~/.claude/CLAUDE.md` symlinks here. It `@`-imports `config/anti-ai-writing-style.md` and `config/git-workflow.md` via `~/github/mody-claude-plugins/`, so keep the clone there or edit those paths.

After editing either settings file, and once on a new machine:

```bash
config/install.sh
```

Run it from your own terminal, not through Claude: Claude Code deletes `~/.claude/settings.json` when its Bash tool writes it. It merges both into `~/.claude/settings.json`, keeping the old file as `settings.json.bak`. Changes Claude Code makes itself (`/config`, "always allow") go to `~/.claude/settings.json`; copy any you want to keep into `config/` before rerunning, or they are overwritten. On a new machine, create `config/settings.local.json` with the `mody` marketplace pointing at your clone; if a plugin doesn't load, run the install commands above.

## Use

```
/mody:product-launch-prep
/mody:product-launch-prep mode=report since=v1.4.0 skip=performance
```

## Update

Edit the skill, bump `version` in `.claude-plugin/plugin.json`, then `claude plugin marketplace update mody && claude plugin update mody@mody`.
