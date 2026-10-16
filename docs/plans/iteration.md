# Skills 迭代方案与验收

## 实施原则

复用现有 semantic index、结构 validator、routing eval、context report、live-agent runner 和各包 eval references。优先补实际 consumer/证据缺口，不增加新 registry、统计 schema 或运行时目录镜像。

| 工作 | 允许的最小影响面 | 验证 |
| --- | --- | --- |
| 联合消费核对 | skills-index 与受影响包/standards；下游独立维护自己的约束 | producer/consumer 逐字段、负例和真实有界 handoff；不得删信任要求 |
| 当前质量基线 | docs/quality 与受影响 eval case/runner | 版本、任务、trace、产物、评分 oracle 一致；历史不冒充当前 |
| 实际加载证明 | 宿主提供的实际读取材料；安装指南只在有真实问题时修改 | hash 对照和范围声明；不搜索/复制秘密，不手工改安装缓存 |
| 验证入口 | 现有 scripts/AGENTS 的适用路径 | focused 用例、exact diff 检查；最终 catalog acceptance 按原 full gate |
| 效率与采用 | 既有真实任务上的人工成本记录 | 同类任务、分母、失败、不可比因素；无基线不宣称节省 |

## 代表性 live 验收设计

先挑与本次发现有关的最小能力集合，不要求每轮重验 19 包。固定任务输入、接受结果和允许工具；执行者只能看到任务和相关运行文件，评分者在输出固定后按 oracle 检查。需要独立 reviewer 时由协调者明确授权/安排，不能用同一次作者自检冒充独立性。

每个改变行为的切片覆盖适用的显式/隐式使用、近邻不触发、有效 no-op、critical stop。涉及源码/浏览器/客户端/API 的用例必须实际观察该层；纯“我会如何做”的回答只算 decision evidence。未知完成结果与恢复场景需要原产品 oracle，不能由评估者临时猜测。

包内容 hash、catalog SHA、实际加载文件与 host trace 对齐；执行失败保留，不能把后续重新运行替换为第一次成功。指定模型/provider 的要求如存在必须按原授权执行；没有该证据则 Not verified，而非隐式豁免。

## 运行边界

迭代使用直接覆盖变更的现有验证器/单测。最终 catalog 接受或发布才运行 `bash scripts/check-skills.sh` 的完整门禁；先读脚本和依赖解析，沿用仓库 Homebrew Python/uv 入口。Python 是现有验证器实现，不因本轮文档重写。

外部 consumer 的联合检查需显式输入固定 catalog，不能偷偷选择工作机上“最新”副本。静态 consumer 相容也不代表 adapter 实际执行或目标产品完成。

### 维护检查选择表

以下路径均相对仓库根；具体范围由变更决定，不将整表当作每次必跑清单。完整规范仍由 [包验证规则](../../skills/AGENTS.md#validation) 和 [skill standard](../skills/skill-standard.md) 持有。

| 变化或结论 | 最小直接检查 | 扩大检查的条件与边界 |
| --- | --- | --- |
| 仓库文档、入口或任务账 | 回读改动及本地链接/锚点；`git diff --check -- <实际文件>` | 不涉及包行为时无需 live 或全目录回归 |
| 单包 prose/本地链接/结构 | `python3 scripts/validate-skills.py`；对应 `test_*.py`；精确路径 diff | validator 检查全目录结构，不能证明宿主实际触发 |
| semantic index / routing / stop | `python3 -m unittest discover -s scripts -p 'test_run_skill_routing_evals.py'`，搜索变化补 `test_search_skills.py`；`python3 scripts/run-skill-routing-evals.py --baseline-ref <已解析不可变SHA>` | baseline 必须从 Git 对象读取；省略参数只是 candidate routing，不构成 no-new-regression 验收 |
| validator/schema/package hygiene | `test_validate_skills.py`、`test_public_content_hygiene.py` 中受影响范围和实际 validator | 包增删/改名联动目录、安装说明、语义索引和 routing cases |
| shared protocol | `python3 scripts/sync-shared-protocols.py --check` 与受影响协议的既有回归 | `--check` 为比较；不带该参数会同步写入，不能当只读核验 |
| DESIGN/visual evidence 合同 | `test_design_md_completeness.py` / `test_frontend_visual_evidence.py`；适用时 `bash scripts/test_design_md_contract.sh` | 合成合同通过不代替真实 UI、批准来源或精确产物绑定 |
| live cases、结果 schema、runner | `test_live_agent_evals.py` / `test_run_live_agent_evals.py`；`python3 scripts/validate-live-agent-evals.py --cases <case文件> --results <结果文件>` | 仅校验 cases 或合成回归不算 live；runner 会调用实际 Agent 并写入隔离 fixture/trace，执行前固定模型、范围与授权 |
| 新建/实质改变包行为、修复真实失败、声称改进 | 固定代表性用例运行实际 Agent；用 `run-live-agent-evals.py --case <固定ID>` 仅在其 fixture/oracle 匹配时执行，并回读 trace/产物 | 覆盖适用的显式、隐式、近邻不触发、no-op、critical stop；五维分开；指定 provider 不可被替代；0 用例不得记通过 |
| merge/release/catalog delivery/最终固定 basis 验收/明确全回归 | `bash scripts/check-skills.sh` | 完整门保留；新源码或基线变化后才按影响复验。它不执行真实 live Agent，也不证明当前宿主加载 |

macOS canonical 入口解析并验证 Homebrew Python；设置 `PYTHON_BIN` 时也须满足同一约束。
有 `uv` 时入口使用 `requirements-dev.txt` 的固定依赖和禁止 Python 下载的参数；
focused 命令复用该解释器与依赖环境。无 `uv` 时检查本地 `jsonschema`/`yaml` 导入，
不能仅据导入成功推定依赖精确版本。不要为只读核对安装或升级环境。

完整门按脚本顺序执行 protocol check、structure validator、不可变 routing baseline、
context warning report、visual evidence example、Python 回归、DESIGN shell 合同和 diff check。
`SKILLS_BASE_SHA` 必须解析为 commit；否则使用 `HEAD` 与 `origin/main` 的 merge-base。
无基线权威或对象不含 baseline 时停止该门，不能改用工作区候选 baseline 宣称通过。
uv 的依赖准备可能写缓存或访问网络；完整门不应被误称为纯只读检查。

本轮 S-01 已核对四个 producer 的实际语义；Forgeway 的 [F-01 精确方案](../../../forgeway/product/iteration-plan.md#f-01-精确修复方案) 统一持有联合消费范围，执行终态见本仓任务账。后续能力升级须同步检查 consumer 的 Registry 和实际 typed consumer，不能只更新 catalog 或字符串示例。扫描 runtime 的 local snapshot 相容性需要独立映射/执行证据。

## 收尾

当前质量摘要只记录实际证据范围；未变化有效历史保留且注明 basis。结果写入本仓 [任务账](iteration-tasks.md)，不复制目标项目任务；真实业务证据留原项目。源码/包、安装/分发、Git/发布分别验证，安装副本存在不等于宿主已加载。
