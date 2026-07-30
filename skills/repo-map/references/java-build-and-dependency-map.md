# Java Build And Dependency Mapping

Use this profile after Maven, Gradle, or JVM source-set evidence appears. Map current
build and runtime ownership without turning the repo map into a dependency report.

## Recognition And Build Roots

1. Resolve Git and workspace boundaries before assigning build ownership. A non-Git
   container may hold many independent Maven or Gradle repositories; one Git
   repository may also hold several independently built or deployed JVM services.
2. For Maven, inspect the nearest owning `pom.xml`, parent chain, `<packaging>`,
   `<modules>`, properties, `dependencyManagement`, plugin management, profiles, and
   Maven Wrapper when present. Distinguish an aggregator POM, inherited parent,
   executable application, library/SDK, test fixture, and deployment-only module.
3. For Gradle, inspect `settings.gradle[.kts]`, `build.gradle[.kts]`, Wrapper
   properties, version catalogs, `buildSrc` or convention plugins, included builds,
   declared projects, plugins, configurations, and packaging tasks. Treat legacy
   `compile`/`runtime` configurations as current evidence when the pinned Gradle build
   uses them; do not silently reinterpret them as a modernized target.
4. Treat `src/main/java`, familiar package names, or a copied helper as supporting
   evidence only. Do not infer the build root, framework family, or module ownership
   from directory names alone.

## Runtime And Toolchain Evidence

Record the JDK requirement from the strongest current repository source: Maven
compiler release/source/target or toolchains, Gradle Java toolchain or compatibility,
Wrapper and CI configuration, `.java-version`, `.tool-versions`, container/build
images, then current documentation. Preserve conflicts and mark the effective runtime
`Not verified` when these authorities disagree.

Record verified executable entry points, application/library packaging, framework
plugins, and the command source. Prefer repository-owned Wrapper commands and current
CI/task definitions. Never invent a Maven goal, Gradle task, active profile, service
port, or deployment command from framework convention alone.

## Bounded Dependency Map

Record only dependencies that change architecture or task routing:

- declared internal module edges and their direction;
- parent POM, dependency-management BOM, Gradle platform, version catalog, or
  convention-plugin authority;
- application framework and executable packaging owner;
- persistence and migration owners;
- authentication/authorization, messaging, scheduling, cache, search, object storage,
  remote-client, API/IDL, generated-code, and observability boundaries;
- build, test, architecture-test, packaging, and deployment plugins when they define a
  required validation or delivery path.

For each retained edge, record the declaring manifest, owner/provider, consumer or
module role, why the edge changes routing, and its live verification source. Do not
copy the full direct or transitive dependency tree, every version property, downloaded
artifact state, or tool-generated effective model. A declared dependency proves a
build edge, not successful resolution or runtime use.

## Configuration And Framework Boundaries

Record configuration file paths, profile naming, configuration-center or environment
ownership, and migrations only when they change task routing. Never copy credentials,
tokens, endpoints, connection strings, or application configuration values into the
map. Treat remote configuration, active profiles, deployed values, and runtime service
discovery as `Not verified` without direct evidence.

For Spring applications, distinguish executable bootstrap modules from domain,
application, API, infrastructure, common, SDK, and test modules using manifests,
entry points, declared edges, architecture tests, and current guidance. Directory
names or a nominal layered layout do not prove dependency direction.

When the user supplies another Java project or framework as a design reference,
extract candidate documentation sections, module-role vocabulary, dependency
directions, command ownership, architecture-test seams, and validation questions.
Compare those candidates with the target repository's current manifests, entry points,
guidance, and consumers. Record only verified target facts; keep useful but unadopted
patterns as proposals outside the current-truth map, and do not create a
framework-specific profile from a reference example.

## Output Boundary

Add the smallest useful Java section to the authoritative root map or a justified
specialist page. Include build roots, JDK evidence, module roles, critical dependency
routes, executable/configuration owners, commands, and `Not verified` gaps. Link
existing architecture or deployment authorities instead of duplicating them.
