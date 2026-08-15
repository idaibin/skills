#!/usr/bin/env node
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

function parse(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || !value) throw new Error("expected --forgeway-cli <file> --installed-repo-map <directory>");
    values[key.slice(2)] = value;
  }
  return values;
}

function files(root, relative = "") {
  const result = [];
  for (const entry of readdirSync(path.join(root, relative), { withFileTypes: true })) {
    if ([".DS_Store", "__pycache__"].includes(entry.name) || entry.name.endsWith(".pyc")) continue;
    const child = path.join(relative, entry.name);
    if (entry.isDirectory()) result.push(...files(root, child));
    else if (entry.isFile()) result.push(child);
  }
  return result.sort();
}

function digest(filename) {
  return createHash("sha256").update(readFileSync(filename)).digest("hex");
}

function invoke(cli, ...args) {
  return JSON.parse(execFileSync(process.execPath, [cli, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }));
}

function assertPortable(result, schema) {
  for (const field of schema.required) assert.ok(Object.hasOwn(result, field), `portable result missing ${field}`);
  assert.equal(result.schema_version, schema.properties.schema_version.const);
  assert.ok(schema.properties.capability_id.enum.includes(result.capability_id));
  assert.equal(result.capability_version, schema.properties.capability_version.const);
  assert.match(result.snapshot_ref, /^scan:/);
  assert.equal(result.validation.valid, true);
}

const args = parse(process.argv.slice(2));
assert.ok(args["forgeway-cli"] && args["installed-repo-map"], "both runtime paths are required task-local inputs");
const forgewayCli = path.resolve(args["forgeway-cli"]);
const installedRepoMap = path.resolve(args["installed-repo-map"]);
const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceRepoMap = path.join(repositoryRoot, "skills", "repo-map");
const sourceFiles = files(sourceRepoMap);
assert.deepEqual(files(installedRepoMap), sourceFiles, "installed repo-map publishable file set differs from source");
for (const relative of sourceFiles) {
  assert.equal(digest(path.join(installedRepoMap, relative)), digest(path.join(sourceRepoMap, relative)), `installed repo-map differs: ${relative}`);
}

const runRoot = mkdtempSync(path.join(tmpdir(), "repo-map-forgeway-e2e-"));
try {
  const adapterManifest = path.join(runRoot, "runtime-adapters.json");
  writeFileSync(adapterManifest, `${JSON.stringify(invoke(forgewayCli, "capability", "adapter"), null, 2)}\n`);
  const registry = path.join(repositoryRoot, "skills-index.json");
  for (const capabilityId of ["repository.asset.scan", "repository.asset.query"]) {
    const resolution = invoke(forgewayCli, "capability", "resolve", "--registry", registry, "--adapters", adapterManifest, "--capability-id", capabilityId, "--capability-version", "1.0.0");
    assert.equal(resolution.selected_adapter.adapter_id, "forgeway.repository-asset-graph");
    assert.equal(resolution.static_manifest_authorizes, false);
    assert.equal(resolution.runtime_adapter_authorizes, false);
  }

  const fixture = path.join(runRoot, "fixture");
  mkdirSync(path.join(fixture, "src", "domain"), { recursive: true });
  writeFileSync(path.join(fixture, "src", "domain", "Order.ts"), "export class Order {}\n");
  const db = path.join(runRoot, "repo-graph.db");
  const scan = invoke(forgewayCli, "graph", "scan", "--db", db, "--root", fixture, "--repository-id", "repo-map-forgeway-e2e");
  const schema = JSON.parse(readFileSync(path.join(repositoryRoot, "docs", "skills", "schemas", "asset-map-result.v1.schema.json"), "utf8"));
  assertPortable(scan.portable_result, schema);
  const query = invoke(forgewayCli, "graph", "query", "--db", db, "--repository-id", "repo-map-forgeway-e2e", "--scan-id", scan.scan_id, "--kind", "domain-entity");
  assertPortable(query.portable_result, schema);
  assert.equal(query.assets[0].symbol, "Order");
} finally {
  rmSync(runRoot, { recursive: true, force: true });
}

console.log("installed repo-map + Forgeway runtime adapter E2E passed");
