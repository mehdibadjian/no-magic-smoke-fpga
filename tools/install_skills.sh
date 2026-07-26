#!/usr/bin/env bash
#
# Install the book's agent skills so they work from any project, not just from
# inside this repo.
#
#   ./tools/install_skills.sh              # install to ~/.claude/skills
#   ./tools/install_skills.sh --uninstall
#   SKILLS_DIR=/some/where ./tools/install_skills.sh
#
# The retrieval skill needs to find the book. Rather than requiring you to
# remember an environment variable, the installer records this checkout's path
# in the installed copy, so `lookup.py` resolves it wherever you run it from.
# Move or delete this checkout and the skill falls back to telling the agent to
# read the published site.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
SKILLS=(fpga-ultrafast ultrafast-authoring)

if [[ "${1:-}" == "--uninstall" ]]; then
    for skill in "${SKILLS[@]}"; do
        if [[ -d "$SKILLS_DIR/$skill" ]]; then
            rm -rf "${SKILLS_DIR:?}/$skill"
            echo "removed  $SKILLS_DIR/$skill"
        fi
    done
    echo "Done. Restart your agent session to pick up the change."
    exit 0
fi

if [[ ! -d "$REPO/docs/sections" ]]; then
    echo "error: $REPO does not look like the no-magic-smoke-fpga checkout" >&2
    exit 1
fi

mkdir -p "$SKILLS_DIR"

for skill in "${SKILLS[@]}"; do
    src="$REPO/.claude/skills/$skill"
    dst="$SKILLS_DIR/$skill"

    if [[ ! -d "$src" ]]; then
        echo "error: $src not found" >&2
        exit 1
    fi

    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "installed $dst"
done

# Pin the book location into the installed retrieval skill.
echo "$REPO" > "$SKILLS_DIR/fpga-ultrafast/scripts/book_path.txt"
echo "pinned    book at $REPO"

# Prove it resolves from somewhere that is definitely not this repo.
if (cd / && python3 "$SKILLS_DIR/fpga-ultrafast/scripts/lookup.py" --list >/dev/null 2>&1); then
    echo "verified  lookup works from outside the repo"
else
    echo "warning:  lookup could not find the book from outside the repo" >&2
fi

cat <<EOF

Installed: ${SKILLS[*]}

Restart your agent session, then the skills trigger automatically on FPGA,
Vivado, XDC, timing and CDC work. To check by hand:

  python3 $SKILLS_DIR/fpga-ultrafast/scripts/lookup.py --search "clock domain crossing"

Uninstall with: $0 --uninstall
EOF
