# Audit Rule Priority

Read this reference for every audit route. Resolve conflicts in this order:

1. the user's current explicit request;
2. effective repository guidance;
3. applicable Product, UI, and resolved design authorities;
4. live source, toolchain, configuration, and repository-declared systems as current
   implementation facts;
5. this package and its selected profiles;
6. external reference repositories.

Live implementation facts do not override an applicable accepted contract; report the
conflict as drift. External repositories and this package provide questions and review
criteria, not stylistic defects or authority to rewrite a working local structure.
