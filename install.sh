#!/bin/sh
# Install every skill in this package into every platform present on this machine.
# No flags, no options, no questions: what it does is all it does.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
touched=""

# Directories this package shipped once and no longer does. Upgrading used to
# leave them behind for ever: the installer only ever replaced what it was about
# to install, so a renamed skill stayed in the developer's list, still offering a
# slash command that pointed at nothing. The manifest below covers every future
# rename; this line covers the machines that installed before the manifest
# existed, which is exactly the population that cannot be reached any other way.
retired="agentic-coding-rubric"

for platform in .claude .codex; do
    [ -d "$HOME/$platform" ] || continue
    mkdir -p "$HOME/$platform/skills"
    manifest="$HOME/$platform/.agentic-coding-skills-manifest"
    shipped=""
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
        shipped="$shipped $skill"
    done

    # Remove what this package installed here before and does not ship any more.
    # Only ever what the manifest recorded, plus the names retired before it
    # existed: a directory the installer did not put there is not its business,
    # and `references` in particular is a name someone else could plausibly own.
    previous=""
    if [ -f "$manifest" ]; then
        previous=$(cat "$manifest")
    fi
    for old in $previous $retired; do
        still_shipped=no
        for name in $shipped; do
            if [ "$name" = "$old" ]; then
                still_shipped=yes
            fi
        done
        if [ "$still_shipped" = no ] && [ -d "$HOME/$platform/skills/$old" ]; then
            rm -rf "$HOME/$platform/skills/$old"
            echo "removed $HOME/$platform/skills/$old"
        fi
    done

    # Written last, so a run that died halfway leaves the older list standing
    # rather than a list of things it had not finished installing.
    printf '%s\n' $shipped > "$manifest"
    touched="$touched $platform"
done

if [ -z "$touched" ]; then
    echo "Found neither $HOME/.claude nor $HOME/.codex, so there is nothing to install into." >&2
    echo "Install Claude Code or Codex first, then run this script again." >&2
    exit 1
fi

echo "platforms:$touched"
