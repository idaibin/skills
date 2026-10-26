# Mobile Device Handoff

Mobile physical-phone, emulator and simulator operations belong to `ops-device`,
not to desktop-client control. When an older entrypoint reaches this reference,
preserve its exact device/app identity, requested result, existing authorization
and foreground constraints, then hand off to the available device owner. If that
owner is unavailable, stop the dependent device operation rather than substitute
host-window control or claim device acceptance.

A desktop client or app-owned session remains `ops-client` owned. Browser-page
DOM/network observations belong to `ops-browser`; neither handoff transfers
installation, external-write or destructive-cleanup authority.
