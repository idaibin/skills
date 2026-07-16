# ChatGPT Work Service Deployment And Page Verification

Use this prompt in a ChatGPT Work-style execution environment that provides a terminal, a writable persistent workspace, and local service access.

## Input

- Project source: `[repository URL or available workspace path]`
- Expected login route: `[optional; discover from the project when omitted]`
- Demo credentials: `[optional; prefer credentials documented by the project]`

## Task

Download or inspect the project, deploy it, start the service, and verify the real rendered pages instead of treating a successful build or listening port as sufficient evidence.

Use Playwright's official Firefox build in native headless mode for browser verification. This is the required browser path for restricted Linux environments where Chromium cannot start because of socket, sandbox, seccomp, Xvfb, or EGL constraints.

## Requirements

1. Inspect the project documentation and determine the correct build, startup, login, and demo-account flow. Do not invent missing credentials.
2. Build and start the service, then report the actual local URL and process state.
3. Launch Playwright Firefox in native headless mode with a `1920 x 1080` viewport and `deviceScaleFactor: 1`.
4. If Firefox cannot start, diagnose and resolve its Playwright installation, runtime dependencies, writable home directory, and permissions. Disable Firefox subprocess sandboxes only when necessary for a trusted local application in a restricted container.
5. Open the login page, wait for the page to become usable, and capture a screenshot.
6. Sign in with the project's documented demo account, wait for a stable authenticated-page signal, and capture the resulting home or dashboard page.
7. Collect failed network requests, `pageerror` events, and browser console errors or warnings. Distinguish application failures from environment or browser-launch failures.
8. Save artifacts under `<current persistent workspace>/artifacts/`; do not leave the only copy in `/tmp`.
9. Verify that each delivered PNG is actually `1920 x 1080`.
10. Close the browser and the local service after verification.

## Output

Return:

- deployment and startup result
- verified local URL and authenticated route
- login-page and authenticated-page screenshots shown directly in the response
- clickable attachment links for both screenshots using paths supported by the current Work environment
- actual image dimensions
- browser, console, page, and request issues found
- unresolved blockers with the exact error and diagnostics already attempted

Do not report success from terminal output alone. The acceptance evidence is a real Firefox-rendered page plus the delivered screenshots.
