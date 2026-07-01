# Ops Browser Usage

## Summary

Use `ops-browser` for browser-based operations where existing tabs, sessions, state, or artifacts matter. It covers inspection, verification, debugging, form filling, upload/download, and browser evidence collection.

## Trigger Examples

- `复用已有页面检查这个问题。`
- `打开后台页面填一下这个表单，但不要影响我现在的标签页。`
- `上传这个文件后确认页面状态。`
- `看一下浏览器 console/network 里为什么失败。`
- `验证这个页面，但结束后关闭临时窗口。`

## Non-Triggers

- Repository-only code review without browser execution.
- Pure API inspection that does not require a browser session.
- Desktop client verification that must inspect a real app window; use `ops-client`.

## Operation Notes

- Start from existing tabs/windows before opening a new page.
- Prefer selectors, roles, labels, DOM state, console, network, and storage evidence.
- Treat form submit, upload, cache clearing, logout, refresh, and destructive navigation as state-changing actions.
- Use temporary pages for account/cache isolation, destructive checks, or when the existing tab is user-owned.
- Close pages/windows opened only for the task.
