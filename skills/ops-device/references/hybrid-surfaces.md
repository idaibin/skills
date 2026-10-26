# Mobile Browser and WebView Boundaries

## Choose the acceptance owner

For a page opened in a mobile browser, `ops-browser` owns page content, DOM,
console/network and browser-state claims. `ops-device` owns selecting/starting the
phone or browser app, OS permissions, device capture and guest state. Pass the bound
device ID, browser identity, URL/tab/context, account and allowed actions at a handoff.
If the page is in a native app's embedded WebView, `ops-device` retains app/container
and end-to-end flow ownership; browser methods can provide a bounded Web-content
observation. A desktop client's embedded WebView remains `ops-client` owned.

For installed native-base/resource-bundle drift, plugin availability and platform
logs, read [hybrid runtime debugging](hybrid-mobile-debugging.md). That procedure does
not expand installation, transport or external-write authority.

## Bind and switch context

Record device ID, app package/bundle, current native or WebView context, page URL and
the specific requested postcondition. An Appium-like context API can enumerate and
switch between native and Web contexts only when the current driver exposes them;
verify the active context after switching. A native accessibility tree missing a Web
element does not prove the element is absent. If a Web context is unavailable, keep
DOM-only checks `Not verified` and use authorized native/visual evidence only for
claims it can support. Return to native context and verify the container state when
the flow crosses back; a Web DOM success does not prove the app transition.

For a real phone browser, desktop mobile viewport emulation is a separate browser
result. It cannot substitute for the requested device's OS/browser build, touch,
permissions or network. Conversely a device screenshot cannot establish DOM or
request details. A device tool can help reach the page, but the browser owner must
verify its own target and state before browser control.

## Network evidence

Record request URL/ID, target environment, whether the response came from the real
service, a proxy/interceptor, fixture or mock, and the observed status/payload needed
for the claim. Page rendering and UI success do not prove a real backend call. A
synthetic response can verify the bounded UI behavior but not production integration.
When provenance cannot be distinguished, stop the dependent network acceptance and
retain independent UI evidence.

References: [Appium contexts](https://appium.io/docs/en/latest/guides/context/),
[Playwright network and mocking](https://playwright.dev/docs/network).
