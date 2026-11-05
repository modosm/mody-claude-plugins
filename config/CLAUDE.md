@~/github/mody-claude-plugins/config/anti-ai-writing-style.md
@~/github/mody-claude-plugins/config/git-workflow.md

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

## Chat status

Title = one circle + space + existing title (replace any leading circle). 🔵 working · 🟠 blocked on my answer or approval · 🟣 ended, a confirmed automation on this chat reruns · 🟢 done. Priority 🟠>🔵>🟣>🟢. Rename only when the circle changes: final circle just before the last reply, 🔵 only for long or background work. Subagents never rename. Desktop app: set_session_title("self"), get_session("self") only if the title is unknown. CLI: load chat-status once per session.
