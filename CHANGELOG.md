# 版本历史

## v3.1 — 交互态补齐（按下状态）

起因：聊天页点「联网 / 思考 / 上下文」三个芯片，会有一块**比芯片大一圈的灰色矩形闪一下**。
查下来是**设计缺一个状态 + 工程继承默认行为**两头的问题：

- 规格只定义了「开态 / 关态」两个静态样式，没有「按下」；
- 工程侧于是用了 Material 默认的 `highlightColor` / `InkSparkle` —— 它按**触摸框（48dp）**画，
  而芯片本体只有 **32dp**，多出来的那一圈深色在浅色皮肤上非常显眼。

### 设计侧（本次）

- `SPEC.md` §2 新增硬性约束 7：**交互态只允许用底色档位（surface → low → high）或透明度表达**，
  禁止 Material 默认水波纹 / 灰色高亮。
- `SPEC.md` §4.8 chip 表补三行：触摸框 48 但底色只画本体 32；关态按下 = `high`（120ms）；
  开态按下保持 `primary-container` 不加深；反馈方式 = 无 ripple / 无 highlight。
- `tokens/token-table.md` 新增「交互态」小节：复用 `--high`，**不新增颜色 token**
  （按压是层级档位，不是新颜色）。
- `reference/full.css` 补 `.chip:active` 与 `-webkit-tap-highlight-color: transparent`
  （移动端 WebKit 的灰色点按高亮是同一类问题，HTML 也必须关掉）。
- `CHECKLIST.md` 新增第 24 条：芯片按压态不许出现灰块。

### 工程侧（同步到 keepsake 仓库）

- `_ToolChip` 改 `StatefulWidget`：`splashFactory: NoSplash.splashFactory`、
  `splashColor/highlightColor = transparent`、`onHighlightChanged` 记 `_pressed`，
  背景按 `transparent`（默认）/ `high`（按下）/ `primary-container`（开态）切换。
- 同步改 `docs/design-handoff/ui-logic.md` §2.8 与 `tokens.md` §6（原来还写着 36 高 / 图标 13 的旧值）。

### Token 变化

无。颜色 token 一条没动，形态表一条没动。

---

## v3 — 列表改造

列表从「6 条平铺、没有结构」改成有分组、有落点的样子。

### 列表页

- **新增时间分组**：今天 / 昨天 / 本周 / 本月，11px / 700 / `onSurfaceVariant` / 字距 0.08em
- **时间移到第二行右侧**：副标题只留对话数，时间 11px 靠右，等宽数字
- **新增未读点**：标题后 6×6 圆点，色 `selectionStroke`
- **当前对话强标**：整行 `selectionBg` 底 + 左侧 3px `selectionStroke` 竖条 + 标题 700 + 头像 `primaryContainer`

### 多选态

- 复选框**放回 34×34 槽位**（框本身 20×20），保持占位一致
- 选中行底色 `selectionBg`，**不加左侧竖条**（那是"当前对话"专属）

### 长按菜单

- 背景列表改用新结构
- 被长按那条整行 `surfaceContainerLow`（不是 `--high`，那样太深像禁用）

### Token 变化

| token | v2 | v3 | 原因 |
|---|---|---|---|
| E `fs-title` | 16 | **15** | 宋体在 16px 下比其他两套宽，标题会先截断 |

颜色 token 一条没动。`row-h` 三套仍是 68。

### 工具

- 新增 `tools/check_consistency.py`：对比设计稿与 `skin_tokens.dart` 的 27 个数值，不一致退出非 0
- CHECKLIST 新增第 23 条：改完 token 必须跑校验

### 没动的部分

聊天页 11 屏、设置页 6 屏、空态/加载/失败/导入、搜索页、图标、圆角、字重、行高倍数。

---

## v2 — 三套皮肤形态首次落地

- 三套皮肤从「只有颜色差异」变成**形态也不同**（圆角/字号/字重/图标风格/描边）
- A 清透：大圆角 + 胶囊，实心图标 24
- E 纸感：小圆角，**描边图标 24**，1px 卡片描边
- H 墨色：中圆角，实心图标 26，字重 700，深青块面
- 新增 `skin_tokens.dart`、`icons.md`、`CHECKLIST.md`、`design_audit.py`
- 拍板了五处材料互相矛盾的地方（见 `docs/设计师回应-拍板与token表.md`）
- **E 换宋体**——这是三套皮肤差异的核心

### v2 遗留问题

- 列表页仍是平铺结构，没有分组
- 交付时 `skin_tokens.dart` 与 `SPEC.md` 有值不一致（E 的 `fsTitle`），v3 修复并加了校验工具

---

## v1 — 初版

- 三套皮肤只有颜色差异，形态完全相同
- 411×892 画布，1dp = 1px
- 9 张渲染图
