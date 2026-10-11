#!/bin/sh
# Builds ~/.claude/settings.json from settings.json + gitignored settings.local.json
# (local wins), and symlinks ~/.claude/CLAUDE.md here. Rerun after editing either file.
set -e
umask 077
cd "$(dirname "$0")"
mkdir -p ~/.claude
[ -f settings.local.json ] || echo '{}' > settings.local.json
jq -s '.[0] * .[1]' settings.json settings.local.json > ~/.claude/settings.json.tmp
[ -e ~/.claude/settings.json ] && cp ~/.claude/settings.json ~/.claude/settings.json.bak
mv ~/.claude/settings.json.tmp ~/.claude/settings.json
ln -sfn "$PWD/CLAUDE.md" ~/.claude/CLAUDE.md
echo "Wrote ~/.claude/settings.json (previous copy: settings.json.bak)"
