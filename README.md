# mody-claude-plugins

Personal Claude Code plugin `mody`. Each skill is invoked as `/mody:<skill>` in any repo.

| Skill | What it does |
|---|---|
| `product-launch-prep` | Launch-readiness review: branch, 8 parallel review phases, findings + go/no-go in `docs/product-launch-prep/` |

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

`hooks/hooks.json` tells Claude, on every new session (and `/clear`), to load `ponytail`, `karpathy-guidelines` and `using-agent-skills` via the Skill tool before its first reply. `i-have-adhd` disables model invocation, so the hook `cat`s its SKILL.md into context instead. Edit the list there.

## Use

```
/mody:product-launch-prep
/mody:product-launch-prep mode=report since=v1.4.0 skip=performance
```

## Update

Edit the skill, bump `version` in `.claude-plugin/plugin.json`, then `claude plugin marketplace update mody && claude plugin update mody@mody`.
