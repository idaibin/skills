# Eval Cases

Use these cases when changing `ops-browser` triggers, modes, state-safety rules, browser evidence expectations, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `复用已有浏览器标签页验证这个页面。` | Should trigger `ops-browser`. | Browser operation with tab reuse. |
| `帮我在网页里填写表单并上传这个文件。` | Should trigger `ops-browser`. | Form and upload workflow. |
| `看一下这个页面的 console 和 network 报错。` | Should trigger `ops-browser`. | Browser debugging evidence. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `审查当前 git 改动，给我 commit 分组。` | Should prefer `code-review`. | Repository review task. |
| `验证 Tauri 客户端窗口，不要用浏览器预览。` | Should prefer `ops-client`. | Real desktop-client operation. |
| `先了解这个仓库的目录和命令。` | Should prefer `code-context`. | Repository context task. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Tab reuse | Checks existing tabs/windows before opening a new page and reports reuse vs temporary page. | Opens duplicate pages without checking. |
| State safety | Avoids disruptive actions on user-owned tabs or explains why they are required. | Refreshes, logs out, submits, or uploads without task need. |
| Form/upload | Maps controls by label/name/role/test id, confirms file path and final state. | Uses coordinate guessing or submits unchecked fields. |
| Evidence | Reports UI, DOM, console, network, storage, screenshot, download, route, or payload evidence as relevant. | Claims verification without evidence. |
| Cleanup | Closes task-only temporary pages/windows. | Leaves temporary browser pages behind. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
