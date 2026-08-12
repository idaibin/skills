# API Contract Graph Profile

Use this profile only to select HTTP/API extractor and query scope. It does not create
or copy an API schema.

Resolve the native source/module owner, route registration, method/path and operation
ID when present, request/success/error/auth declaration owners, client adapter,
representative consumers, tests, and generated pipeline only when one already exists.
Keep source owner, build/deploy owner, runtime service identity, and gateway alias
separate.

Emit typed Assets and Edges such as `defines`, `registers`, `exports`, `calls`,
`consumes`, `implements`, and `verifies`. Record basis, path/symbol, hashes,
extractor/version, evidence status, confidence, and unresolved duplicate-authority or
DTO candidates. OpenAPI and generated clients remain native authorities/artifacts, not
graph-owned copies.

An API query result proves only the indexed static chain at its snapshot basis. It does
not prove authentication enforcement, target routing, runtime compatibility, delivery,
or deployment; those claims require typed delivery Observations or Receipts.
