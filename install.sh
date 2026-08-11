#!/bin/sh
# Install every skill in this package into every platform present on this machine.
# No flags, no options, no questions: what it does is all it does.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
touched=""

for platform in .claude .codex; do
    [ -d "$HOME/$platform" ] || continue
    mkdir -p "$HOME/$platform/skills"
    # Whatever is in skills/ is what gets installed. Naming them here as well
    # would mean a new skill arrives in the repository and silently never
    # reaches anyone's machine.
    for source in "$here"/skills/*/; do
        skill=$(basename "$source")
        target="$HOME/$platform/skills/$skill"
        staging="$target.incoming"
        # Copy beside the target first and only move it over the old version once
        # the copy is complete. Removing the target first, as this did, meant a
        # copy that failed halfway — an incomplete clone, a full disk, an
        # interrupt — took a working skill with it. The move also replaces rather
        # than nests: a plain copy onto an existing directory would land inside it.
        rm -rf "$staging"
        if ! cp -R "$source" "$staging"; then
            rm -rf "$staging"
            echo "Copying $skill from $here failed; $target is untouched." >&2
            exit 1
        fi
        rm -rf "$target"
        mv "$staging" "$target"
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
