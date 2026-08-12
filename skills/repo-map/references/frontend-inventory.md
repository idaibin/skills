# Frontend Graph Profile

Use this profile only to select frontend extractor and query scope.

Index route/entry registrations, pages/screens, reusable and feature components,
hooks/composables, state/data owners, API clients and request types, style/theme/config
owners, tests, and the resolved `<design-root>/DESIGN.md` binding when adopted. Emit
typed Assets and Edges such as `registers`, `renders`, `imports`, `calls`, `consumes`,
`verifies`, `owned-by`, and `derived-from` according to the graph schema.

Keep Product Markdown, Feature UI Markdown, `DESIGN.md`, and live source as separate
authorities. Graph records carry their IDs, paths, symbols, roles, hashes, and edges;
they do not copy tokens, component interfaces, API schemas, page composition, or target-
only states. A current implementation adapter does not become design authority.

For reuse or impact queries, return the canonical definition, export/registration,
owner/provider root, representative consumers, states proven by current source, scan
basis, and unresolved/conflict records. A query miss means `Not found in this
snapshot`; perform bounded live discovery before recommending `new`.
