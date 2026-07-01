# Eval Cases

Use these cases when changing `ops-client` triggers, modes, window evidence rules, Accessibility guidance, AI-operable UI guidance, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `验证真实 Tauri 客户端窗口，不要用浏览器预览。` | Should trigger `ops-client`. | Real client-window verification. |
| `用 CGWindowID 截一下 app 窗口。` | Should trigger `ops-client`. | Window-level screenshot evidence. |
| `这个按钮让 AI 更容易识别和点击。` | Should trigger `ops-client`. | AI-operable DOM/Accessibility guidance. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `复用浏览器标签页填写网页表单。` | Should prefer `ops-browser`. | Browser operation workflow. |
| `审查当前 git 改动，分类提交。` | Should prefer `code-review`. | Dirty-tree review. |
| `先了解这个仓库的目录和命令。` | Should prefer `code-context`. | Repository context task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Real window evidence | Confirms process/runtime/window identity and captures by `CGWindowID`. | Uses browser preview or region screenshot as client proof. |
| Runtime source | Distinguishes `pnpm tauri dev`, debug bundle, release app, or reports `Not verified`. | Assumes runtime source without evidence. |
| Background-safe interaction | Uses Accessibility/control-tree paths and avoids stealing mouse/focus where possible. | Coordinate-clicks without checking stable control paths. |
| AI-operable UI | Recommends semantic controls, accessible names, labels, and stable selectors for critical controls. | Leaves icon-only or generic controls unidentified. |
| Restart/rebuild | Re-verifies after relevant UI, bundle, or Accessibility changes. | Claims fix against stale client instance. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
