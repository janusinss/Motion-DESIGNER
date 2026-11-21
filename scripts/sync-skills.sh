#!/usr/bin/env bash
# Syncs canonical workspace skills from .agents/skills/ to Claude Code and/or user-global agent skill directories.
# Operates per-skill so existing unrelated skills in global directories are preserved.

set -euo pipefail

GLOBAL=0
TARGET="auto"
MODE="symlink"
FORCE=0
CLEAN=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: ./scripts/sync-skills.sh [options]

Options:
  --global             Sync to user-global dirs (~/.claude/skills, ~/.agents/skills, ~/.codex/skills)
                       instead of project-local .claude/skills/
  --target <name>      Filter target: auto | claude | agents | codex | all
                       (default: auto -> claude for project, all for --global)
  --mode <strategy>    Sync strategy: symlink | copy (default: symlink)
  --force              Replace existing skill entries in target directory
  --clean              Remove only entries matching .agents/skills/* from target directory
  --dry-run            Preview planned actions without modifying the filesystem
  -h, --help           Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)  GLOBAL=1; shift ;;
    --target)  TARGET="${2:?Missing value for --target}"; shift 2 ;;
    --mode)    MODE="${2:?Missing value for --mode}"; shift 2 ;;
    --force)   FORCE=1; shift ;;
    --clean)   CLEAN=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: unknown option '$1'" >&2; usage >&2; exit 1 ;;
  esac
done

case "$TARGET" in
  auto|claude|agents|codex|all) ;;
  *) echo "Error: invalid --target '$TARGET' (expected auto|claude|agents|codex|all)" >&2; exit 1 ;;
esac

case "$MODE" in
  symlink|copy) ;;
  *) echo "Error: invalid --mode '$MODE' (expected symlink|copy)" >&2; exit 1 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.agents/skills"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Error: source skills directory not found: $SOURCE_DIR" >&2
  exit 1
fi

SKILLS=()
for dir in "$SOURCE_DIR"/*/; do
  [[ -f "${dir}SKILL.md" ]] || continue
  SKILLS+=("$(basename "${dir%/}")")
done

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "Error: no skills (folders containing SKILL.md) found in: $SOURCE_DIR" >&2
  exit 1
fi

DEST_DIRS=()
if [[ $GLOBAL -eq 1 ]]; then
  if [[ "$TARGET" == "auto" || "$TARGET" == "all" ]]; then
    EFFECTIVE_TARGETS=(claude agents codex)
  else
    EFFECTIVE_TARGETS=("$TARGET")
  fi
  for t in "${EFFECTIVE_TARGETS[@]}"; do
    case "$t" in
      claude) DEST_DIRS+=("$HOME/.claude/skills") ;;
      agents) DEST_DIRS+=("$HOME/.agents/skills") ;;
      codex)  DEST_DIRS+=("$HOME/.codex/skills") ;;
    esac
  done
else
  if [[ "$TARGET" == "auto" ]]; then
    EFFECTIVE_TARGETS=(claude)
  elif [[ "$TARGET" == "all" ]]; then
    EFFECTIVE_TARGETS=(claude codex)
  else
    EFFECTIVE_TARGETS=("$TARGET")
  fi
  for t in "${EFFECTIVE_TARGETS[@]}"; do
    case "$t" in
      claude) DEST_DIRS+=("$REPO_ROOT/.claude/skills") ;;
      codex)  DEST_DIRS+=("$REPO_ROOT/.codex/skills") ;;
      agents) echo "Warning: project target 'agents' is already the canonical source ($SOURCE_DIR); skipping." >&2 ;;
    esac
  done
fi

if [[ ${#DEST_DIRS[@]} -eq 0 ]]; then
  echo "No target directories selected. Nothing to do."
  exit 0
fi

SCOPE_LABEL="project"
[[ $GLOBAL -eq 1 ]] && SCOPE_LABEL="global"
ACTION_LABEL="sync ($MODE)"
[[ $CLEAN -eq 1 ]] && ACTION_LABEL="clean"
DRY_SUFFIX=""
[[ $DRY_RUN -eq 1 ]] && DRY_SUFFIX=" [DRY-RUN]"

echo "Source: $SOURCE_DIR (${#SKILLS[@]} skills)"
echo "Scope:  $SCOPE_LABEL | Action: $ACTION_LABEL$DRY_SUFFIX"

for dest_root in "${DEST_DIRS[@]}"; do
  created=0
  skipped=0
  removed=0

  echo ""
  echo "Target: $dest_root"

  if [[ $CLEAN -eq 1 ]]; then
    if [[ ! -d "$dest_root" ]]; then
      echo "  (not present; nothing to clean)"
      continue
    fi
    for skill in "${SKILLS[@]}"; do
      dst="$dest_root/$skill"
      if [[ -e "$dst" || -L "$dst" ]]; then
        if [[ $DRY_RUN -eq 1 ]]; then
          echo "  [dry-run] remove $dst"
        else
          rm -rf "$dst"
        fi
        removed=$((removed + 1))
      fi
    done
    echo "  Cleaned: $removed skill(s)"
    continue
  fi

  if [[ ! -d "$dest_root" ]]; then
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "  [dry-run] mkdir -p $dest_root"
    else
      mkdir -p "$dest_root"
    fi
  fi

  for skill in "${SKILLS[@]}"; do
    src="$SOURCE_DIR/$skill"
    dst="$dest_root/$skill"

    if [[ "$src" == "$dst" ]]; then
      skipped=$((skipped + 1))
      continue
    fi

    if [[ -e "$dst" || -L "$dst" ]]; then
      if [[ $FORCE -eq 0 ]]; then
        skipped=$((skipped + 1))
        continue
      fi
      if [[ $DRY_RUN -eq 0 ]]; then
        rm -rf "$dst"
      fi
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
      created=$((created + 1))
      continue
    fi

    if [[ "$MODE" == "symlink" ]]; then
      ln -s "$src" "$dst"
    else
      cp -R "$src" "$dst"
    fi
    created=$((created + 1))
  done

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  [dry-run] would sync: $created | already present (skip; use --force to replace): $skipped"
  else
    echo "  Synced: $created | Skipped (already present): $skipped"
  fi
done
