# Ops Client Usage

## Summary

Use `ops-client` for real desktop client operation and verification. It is currently Tauri-focused, but it should also guide other desktop client shells when real app-window evidence matters.

## Trigger Examples

- `验证 Tauri 客户端窗口，不能用浏览器预览。`
- `用 CGWindowID 截真实 app 窗口看一下。`
- `通过 AXPress 点这个客户端按钮，不要抢鼠标。`
- `确认现在跑的是 pnpm tauri dev 还是 release app。`
- `这个控件 AI 不好点，帮我补可识别的 DOM/Accessibility 标识。`

## Non-Triggers

- Browser-only page inspection, form filling, upload/download, or console/network debugging; use `ops-browser`.
- Repository-only context discovery; use `code-context`.
- Dirty-tree review or commit planning; use `code-review`.

## Operation Notes

- Process and runtime source are part of the evidence, not optional setup.
- Prefer `screencapture -x -l<CGWindowID>` over region capture.
- Prefer Accessibility actions on named controls over pointer movement or coordinate clicks.
- Treat multiple app instances and stale bundles as common failure modes.
- For Tauri webviews, make controls semantic and discoverable through DOM and Accessibility surfaces.
