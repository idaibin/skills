"""Prepare bounded inputs for open-ended owner tasks; keep reviewer criteria out of the prompt."""
import json
import os
import subprocess
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "evals/live-agent-owner-fixtures.json"


def write_inputs(root, files):
    for name, body in files.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or ".git" in path.parts:
            raise ValueError(f"invalid fixture input: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body.rstrip("\n") + "\n", encoding="utf-8")


def prepare_owner_input(workspace, case_root, fixture, initialize):
    write_inputs(workspace, fixture.get("files", {}))
    initialize(workspace)
    if "candidate" in fixture:
        write_inputs(workspace, fixture["candidate"])
        subprocess.run(["git", "add", "--", *fixture["candidate"]], cwd=workspace, check=True)
        subprocess.run(["git", "-c", "user.email=live-agent-eval", "commit", "--quiet",
                        "-m", "synthetic candidate"], cwd=workspace, check=True)
    write_inputs(workspace, fixture.get("dirty", {}))
    brief = fixture["brief"]
    if fixture.get("graph"):
        cli = os.environ.get("LIVE_EVAL_FORGEWAY_CLI")
        if not cli or not Path(cli).is_file():
            brief = ("No validated graph receipt was supplied. The host has not bound a "
                     "graph runtime for this evaluation.")
            (case_root / "input.txt").write_text(brief, encoding="utf-8")
            return brief
        db = workspace.parent / "graph.db"
        def graph(action, *args):
            command = ["node", cli, "graph", action, "--db", str(db), *args]
            return json.loads(subprocess.check_output(command, cwd=workspace, text=True))
        scan = graph("scan", "--root", str(workspace), "--exclude", ".git", "--repository-id", "fixture")
        ref = scan["scan_id"]
        validation = graph("validate", "--scan-id", ref)
        query = graph("query", "--repository-id", "fixture", "--scan-id", ref, "--path", "src/components")
        if not validation["valid"] or query["portable_result"]["snapshot_ref"] != ref:
            raise ValueError("invalid fixed graph input")
        receipt = {"snapshot": scan["local_snapshot"], "validation": validation,
                   "coverage": scan["coverage"], "assets": query["assets"],
                   "query_capability": query["portable_result"]["capability_id"]}
        brief += "\nFixed graph receipt:\n" + json.dumps(receipt, ensure_ascii=False)
    (case_root / "input.txt").write_text(brief, encoding="utf-8")
    return brief
