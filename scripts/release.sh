#!/usr/bin/env bash
# coding=utf-8
#
# Release a new version of Pulp Smash.
#
# Test Pulp Smash for sanity. If all is well, generate a new commit, tag it,
# and print instructions for further steps to take.
#
# NOTE: This script should be run from the repository root directory. That is,
# this script should be run from this script's parent directory.
#
set -euo pipefail
set -x

# See: http://mywiki.wooledge.org/BashFAQ/028
readonly script_name='release.sh'

# Print usage instructions to stdout.
show_help() {
fmt <<EOF
Usage: $script_name [options] <new-version>

Release a new version of Pulp Smash. More specifically, write <new-version> to
the VERSION file, build new packages, test them for sanity, generate a new
tagged commit, and print instructions for next steps.

Options:
    --help
        Show this message.
    --repo-path
        The path to the root of the Pulp Smash repository. Defaults to '.'.
EOF
}

# Transform $@. $temp is needed. If omitted, non-zero exit codes are ignored.
temp=$(getopt \
    --options '' \
    --longoptions help,repo-path: \
    --name "$script_name" \
    -- "$@")
eval set -- "$temp"
unset temp

# Read arguments. (getopt inserts -- even when no arguments are passed.)
if [ "${#@}" -eq 1 ]; then
    show_help
    exit 1
fi
while true; do
    case "$1" in
        --help) show_help; shift; exit 0;;
        --repo-path) cd "$2"; shift 2;;
        --) shift; break;;
        *) echo "Internal error! Encountered unexpected argument: $1"; exit 1;;
    esac
done
new_version="$1"; shift

old_version="$(git describe)"  # e.g. 1!0.0.1-4-g5525f17
old_version="${old_version%-*}"  # Drop commit hash
old_version="${old_version%-*}"  # Drop number of commits
if [ "${new_version}" = "${old_version}" ]; then
    echo Nothing to release!
    exit 1
fi

# Generate new packages.
echo "${new_version}" > VERSION
make dist-clean dist

# Create a venv, and schedule it for deletion.
cleanup() { if [ -n "${venv:-}" ]; then rm -rf "${venv}"; fi }
trap cleanup EXIT  # bash pseudo signal
trap 'cleanup ; trap - SIGINT ; kill -s SIGINT $$' SIGINT
trap 'cleanup ; trap - SIGTERM ; kill -s SIGTERM $$' SIGTERM
venv="$(mktemp --directory)"
python3 -m venv "${venv}"

# Sanity check the new packages.
set +u
source "${venv}/bin/activate"
set -u
for dist in dist/*; do
    pip install --quiet "${dist}"
    pulp-smash settings --help 1>/dev/null
    pip uninstall --quiet --yes pulp_smash
done
set +u
deactivate
set -u

# Create a new commit and annotated tag.
git add VERSION
commit_message="$(git shortlog "${old_version}.." | sed 's/^./    &/')"
git commit \
    --message "Release version ${new_version}" \
    --message "Shortlog of commits since last release:" \
    --message "${commit_message}"
git tag --annotate "${new_verison}" --message "Pulp Smash ${new_version}" \
        --message "${commit_message}"

fmt <<EOF

This script has made only local changes: it has updated the VERSION file,
generated a new commit, tagged the new commit, and performed a few checks along
the way. If you are confident in these changes, you can publish them with
commands like the following:
EOF

cat <<EOF

    git push --tags origin master && git push --tags upstream master
    make publish

EOF
