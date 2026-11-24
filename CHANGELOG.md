# 版本历史

## v3.5 — 气泡可辨、E 纸色调统一、FAB 描边归位、头像统一圆形

产品裁决（2026-11-24）：**HTML 是审查真值**，设计产出（SPEC / token / dart）跟着 HTML 走。

- **AI 气泡与用户气泡分离**（E-09 / D-17）：三套皮肤的 `--ai-bg` 统一改为 `--low`，
  `--ai-fg` 改为 `--on-s`。原来 A/H 的 `--p-c` 与 `--ai-bg` 同值，真机上用户与 AI 气泡
  完全同色，只能靠左右对齐区分。
- **E 的 AI 气泡改纸色**（D-18）：E 的 `--ai-bg` = `#F1EDE4`（= E 的 `--low`），不再用冷薄荷。
- **FAB 描边归位**（E-12 / D-30）：SPEC §4.5 与硬性约束 4 都改成「`primaryContainer` 底 + 1px
  `--fab-line`（`#8CCDBB`）描边」，与 `full.css` 的 `.fab` 一致；token 表补 `--fab-line`。
- **头像统一圆形**（D-05）：三套 `--av-r` = 17（34 的一半）；HTML 里 E 的 `6px` 改成 `17px`，
  SPEC §4.2 注明"E 写成 6 会做成圆角方块"。
- token 表补 `--ai-bg/--ai-fg/--fab-line/--av-r` 四行；不新增颜色语义。

工程侧同步（keepsake）：`skin_tokens.dart` 六套（含深色）的 `aiBg/aiFg` 改为 low/onS、
E 的 `avatarRadius` 0 → 17、新增 `kFabLineColor` 并在 FAB 上补 1px 描边。

---

## v3.4 — 清单里"不需要裁决"的自错误清掉

- `tokens/skin_tokens.dart`：删掉重复的 `fsBody` 字段与重复构造参数（**这个文件第一次能编译过**，
  用 Flutter 3.50 / Dart 3.14 实测 `flutter analyze` 无 issue）。
- `reference/full.css`：`.chip` 高度 36 → **32**（SPEC §4.8 + 工程 `kChipHeight = 32`）。
- `docs/icons.md`：chip 图标尺寸 13–14 → **15**（SPEC 硬性要求；原文自己也写"13 会糊"）。
- `reference/full-settings.html`：去掉写死的 `v1.1.0`，改为"版本号以工程发行说明为准"。
- `reference/index.html`：写清屏数与尺寸事实 —— 三份参考稿合计 **30 个状态**（13/11/6），
  每状态三套皮肤；`screens/` 9 张 PNG 为 1360 宽（411dp 画布的约 3.3×），高度按状态堆叠
  （列表 4980 / 聊天 3860 / 设置 2200）。

> 不新增 token；不改任何颜色值。

---

## v3.3 — 信息架构收口：全局操作不进单条菜单

起因：审查清单里「会话内 ⋮ 缺 5 项」这条需要澄清。产品确认的口径是：

- **聊天页 ⋮ 只有「设置」一项**（刻意极简，不加按钮）；
- **「补建角色卡」是对全部会话的批量修复**，入口只在「设置 › 数据维护 → 修复会话数据」，
  **不能**放进单条会话/单条列表行的菜单 —— 挂在单条菜单里会被理解成"只补这一条"；
- 列表行 ⋮ 保留：重命名 / 置顶 · 取消置顶 / 删除会话。

本版改动：
- `reference/full-list.html` 的「列表 · ⋮ 菜单」示例屏去掉「为缺少角色卡的会话补建」一行；
- `docs/CHECKLIST.md` 新增第 26 条（全局批量操作不得下放到单条菜单）；
- 与工程侧 `docs/design-handoff/{README,ui-logic}.md` 同步（那两处原本还写着"补建从列表 ⋮ 进"）。

> 这条不是新设计，是把已被 v3.3 实现改掉的旧稿对齐；不新增 token。

---

## v3.2 — 轻提示挪到顶部

起因：聊天页点「思考」芯片，弹出的「思考：开（中）」用 SnackBar 贴在屏幕底部，
正好盖住输入框和工具芯片（用户截图里画了红框）。

### 设计侧（本次）

- `SPEC.md` 新增 §4.9 轻提示（toast）：顶部浮层（状态栏 + 56 + 8）、
  `inverseSurface` 底、`r-card` 圆角、14 号字、2s、120ms 淡入 + 8dp 上浮、
  `IgnorePointer` 不拦手势；**禁止底部 SnackBar**（会压住输入区/工具条）。
- `reference/full.css` 新增 `.toast` / `.toast .tt` / `@keyframes toast-in` 参考实现。
- `CHECKLIST.md` 新增第 25 条：提示不许出现在底部输入区上方。
- 不新增 token（沿用 M3 `inverseSurface` / `onInverseSurface` 与 `--r-card`）。

### 工程侧（同步到 keepsake 仓库）

- 新增 `lib/core/ui/toast.dart`：`showTopToast()` 用根 Overlay 画顶部浮层，
  同屏只留一条、`IgnorePointer`、2s 自动消失、120ms 动画。
- 聊天页 `_toast`、语音控件两处兜底提示、相册页 / 预览页 / 图片编辑器
  的轻提示全部改走 `showTopToast`。
- 同步 `docs/design-handoff/ui-logic.md` §2.14、`tokens.md` §6 动效表。

---

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
