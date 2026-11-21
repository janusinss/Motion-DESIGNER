@AGENTS.md

## Claude Code Skill Discovery

All 47 workspace skills live canonically in `.agents/skills/<name>/SKILL.md` (discovered natively by Antigravity and OpenAI Codex).

Claude Code discovers skills in `.claude/skills/` (project) and `~/.claude/skills/` (user-global). Run the sync helper to expose all 47 skills to Claude Code without duplicating them in Git:

- **Windows (PowerShell)**: `.\scripts\sync-skills.ps1` (add `-Global` for `~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`)
- **macOS / Linux (Bash)**: `./scripts/sync-skills.sh` (add `--global` for user-global paths)

Treat `.agents/skills/` as the single source of truth; `.claude/skills/` is a local generated mirror (gitignored).
