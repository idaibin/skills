#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON_BIN:-}"
if [[ -z "$python_bin" ]]; then
  if [[ "$(uname -s)" == "Darwin" ]]; then
    if ! command -v brew >/dev/null 2>&1; then
      echo "validation requires Homebrew Python on macOS; brew was not found" >&2
      exit 2
    fi
    brew_prefix="$(brew --prefix)"
    python_bin="$brew_prefix/bin/python3"
  else
    python_bin="$(command -v python3 || true)"
  fi
fi

if [[ -n "$python_bin" && "$python_bin" != */* ]]; then
  python_bin="$(command -v -- "$python_bin" || true)"
fi

if [[ -z "$python_bin" || ! -x "$python_bin" ]]; then
  echo "validation Python is not executable: ${python_bin:-not found}" >&2
  exit 2
fi

resolved_python="$("$python_bin" -c 'import os, sys; print(os.path.realpath(sys.executable))')"
if [[ "$(uname -s)" == "Darwin" ]]; then
  brew_prefix="$(brew --prefix)"
  case "$resolved_python" in
    "$brew_prefix"/*) ;;
    *)
      echo "validation refuses non-Homebrew Python on macOS: $resolved_python" >&2
      exit 2
      ;;
  esac
fi

if command -v uv >/dev/null 2>&1; then
  export UV_CACHE_DIR="${UV_CACHE_DIR:-${TMPDIR:-/tmp}/aicraft-skills-uv-cache}"
  python_runner=(
    uv run
    --python "$python_bin"
    --no-managed-python
    --no-python-downloads
    --with-requirements requirements-dev.txt
    python
  )
else
  "$python_bin" -c 'import jsonschema, yaml' 2>/dev/null || {
    echo "validation dependencies are missing; install requirements-dev.txt or install uv" >&2
    exit 2
  }
  python_runner=("$python_bin")
fi

echo "validation python: $resolved_python"
"${python_runner[@]}" scripts/sync-shared-protocols.py --check
"${python_runner[@]}" scripts/validate-skills.py
routing_base_sha="${SKILLS_BASE_SHA:-}"
if [[ -n "$routing_base_sha" ]]; then
  if ! git cat-file -e "$routing_base_sha^{commit}" 2>/dev/null; then
    echo "SKILLS_BASE_SHA does not resolve to a commit: $routing_base_sha" >&2
    exit 2
  fi
elif git rev-parse --verify origin/main >/dev/null 2>&1; then
  routing_base_sha="$(git merge-base HEAD origin/main)"
else
  echo "cannot resolve routing baseline authority: set SKILLS_BASE_SHA or fetch origin/main" >&2
  exit 2
fi
if git cat-file -e "$routing_base_sha":evals/skill-routing-baseline.json 2>/dev/null; then
  echo "routing baseline: $routing_base_sha (immutable Git authority)"
  "${python_runner[@]}" scripts/run-skill-routing-evals.py --baseline-ref "$routing_base_sha"
else
  base_index_version="$(git show "$routing_base_sha":skills-index.json 2>/dev/null | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin).get("version", 0))' 2>/dev/null || true)"
  if [[ "$base_index_version" != "1" ]]; then
    echo "published base $routing_base_sha is missing its routing baseline; refusing candidate bootstrap" >&2
    exit 2
  fi
  echo "routing baseline: first v2 bootstrap (base index version 1 has no baseline)"
  "${python_runner[@]}" scripts/run-skill-routing-evals.py --baseline-report evals/skill-routing-baseline.json
fi
"${python_runner[@]}" scripts/report-skill-context.py
"${python_runner[@]}" scripts/validate-frontend-visual-evidence.py \
  skills/dev-frontend/assets/frontend-visual-evidence.example.json
"${python_runner[@]}" -m unittest discover -s scripts -p 'test_*.py'
bash scripts/test_design_md_contract.sh
git diff --check
