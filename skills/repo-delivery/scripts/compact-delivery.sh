#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: compact-delivery.sh --message MESSAGE [--rebase] [--push] [--remote NAME] -- PATH...'
}

message=''
remote='origin'
do_rebase=0
do_push=0
paths=()

while (($#)); do
  case "$1" in
    --message)
      (($# >= 2)) || { usage >&2; exit 2; }
      message=$2
      shift 2
      ;;
    --remote)
      (($# >= 2)) || { usage >&2; exit 2; }
      remote=$2
      shift 2
      ;;
    --rebase)
      do_rebase=1
      shift
      ;;
    --push)
      do_push=1
      shift
      ;;
    --)
      shift
      paths=("$@")
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$message" && ${#paths[@]} -gt 0 ]] || { usage >&2; exit 2; }
git rev-parse --is-inside-work-tree >/dev/null

for path in "${paths[@]}"; do
  case "$path" in
    ''|.|..|/*|*'..'*|*'*'*|*'?'*|*'['*)
      printf 'unsafe path: %s\n' "$path" >&2
      exit 2
      ;;
  esac
done

git diff --cached --quiet || {
  printf '%s\n' 'refusing pre-existing staged content' >&2
  exit 3
}

branch=$(git symbolic-ref --quiet --short HEAD) || {
  printf '%s\n' 'detached HEAD is not supported' >&2
  exit 3
}

git add -- "${paths[@]}"
git diff --cached --quiet && {
  printf '%s\n' 'nothing staged from requested paths' >&2
  exit 3
}
git diff --cached --check
staged_files=$(git diff --cached --name-only | wc -l | tr -d ' ')
git commit --quiet -m "$message"

if ((do_rebase)); then
  git fetch --quiet "$remote" "$branch"
  git rebase "$remote/$branch"
elif ((do_push)); then
  git fetch --quiet "$remote"
fi

commit=$(git rev-parse HEAD)
remote_sha='not-requested'
if ((do_push)); then
  git push --quiet "$remote" "HEAD:refs/heads/$branch"
  remote_sha=$(git ls-remote --heads "$remote" "refs/heads/$branch" | awk 'NR == 1 {print $1}')
  [[ "$remote_sha" == "$commit" ]] || {
    printf 'remote SHA mismatch: local=%s remote=%s\n' "$commit" "${remote_sha:-missing}" >&2
    exit 4
  }
fi

remaining_entries=$(git status --porcelain=v1 | wc -l | tr -d ' ')
printf 'delivery_result branch=%s commit=%s pushed=%s remote_sha=%s staged_files=%s remaining_entries=%s\n' \
  "$branch" "$commit" "$do_push" "$remote_sha" "$staged_files" "$remaining_entries"
