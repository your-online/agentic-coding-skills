#!/bin/sh
# Install the three skills into every platform present on this machine.
# No flags, no options, no questions: what it does is all it does.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
touched=""

for platform in .claude .codex; do
    [ -d "$HOME/$platform" ] || continue
    for skill in advise-me review-my-work log-feedback; do
        target="$HOME/$platform/skills/$skill"
        # Remove first: an upgrade has to replace the old version, and a copy
        # onto an existing directory would nest inside it instead.
        rm -rf "$target"
        mkdir -p "$HOME/$platform/skills"
        cp -R "$here/skills/$skill" "$target"
        echo "installed $target"
    done
    touched="$touched $platform"
done

if [ -z "$touched" ]; then
    echo "Found neither $HOME/.claude nor $HOME/.codex, so there is nothing to install into." >&2
    echo "Install Claude Code or Codex first, then run this script again." >&2
    exit 1
fi

echo "platforms:$touched"
