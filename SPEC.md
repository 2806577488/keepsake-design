# Keepsake 皮肤系统 · 工程师落地规格 v2

> 配套：`icons.md`（图标对照）、`CHECKLIST.md`（验收清单）、`reference/`（可直接对照的 HTML 实现）、`screens/`（1360px 静态图）
>
> 设计稿尺寸：411dp × 892dp，1dp = 1px。文档里所有数字都是 dp。

---

## 0. 先理解这件事

**三套不是三个配色，是三套皮肤。**

同一个组件，A / E / H 在**形态**上就不一样：

| 维度 | A 清透 | E 纸感 | H 墨色 |
|---|---|---|---|
| 圆角性格 | 大圆角 + 胶囊 | 小圆角（8/6/4） | 中圆角，偏方 |
| 字体 | 系统无衬线 | **元信息用等宽** | 系统无衬线，字号 +1 |
| 字重 | 600 | 700 + 紧字距 | 700 |
| 图标 | 实心 24 | **描边 24** | 实心 26 |
| 行高 | 1.6 | 1.5 | 1.55 |
| 卡片 | 无边框，靠底色 | **1px 描边**，底色同页面 | 无边框，靠深色块面 |

所以**不是**把 `ColorScheme` 换一遍就完事。颜色只占工作量的三分之一。

---

## 1. 架构（照这个结构写，别在页面里散写常量）

```
SkinTokens        // 颜色 + 圆角 + 字号 + 行高 + 图标风格，纯数据
  ├─ ColorTokens
  └─ MorphTokens
SkinScope         // InheritedWidget，向下提供当前 SkinTokens
```

页面里只允许出现 `SkinScope.of(context).xxx`，不允许出现 `Color(0xFF...)` 或 `BorderRadius.circular(8)` 这种字面量。

**验收方式**：全项目 grep `0xFF` 和 `circular(`，除了 token 文件，其余出现都算不合格。

---

## 2. 颜色与形态 Token

下面两张表**从设计稿自动生成**，就是三套真实值。改设计就重新生成，不要手抄。

| 变量 | Flutter | A 清透 | E 纸感 | H 墨色 |
|---|---|---|---|---|
| `--surface` | `surface` | `#F5FBF7` | `#FDFCF9` | `#F5FBF7` |
| `--low` | `low` | `#EFF5F2` | `#F1EDE4` | `#EFF5F2` |
| `--high` | `high` | `#E3EAE6` | `#E8E2D6` | `#E3EAE6` |
| `--highest` | `highest` | `#DEE4E1` | `#DEE4E1` | `#DEE4E1` |
| `--ov` | `ov` | `#CAD1CD` | `#D8D4CC` | `#CAD1CD` |
| `--outline` | `outline` | `#7C8B86` | `#7C8B86` | `#7C8B86` |
| `--on-s` | `onS` | `#191C1B` | `#1A1A18` | `#191C1B` |
| `--on-v` | `onV` | `#496F66` | `#5C5A54` | `#496F66` |
| `--p-c` | `pC` | `#A0F2DF` | `#F2D9C4` | `#A0F2DF` |
| `--on-p-c` | `onPC` | `#005045` | `#5A2E14` | `#005045` |
| `--send-bg` | `sendBg` | `#A0F2DF` | `#B4481B` | `#1F4A42` |
| `--send-fg` | `sendFg` | `#005045` | `#FFFFFF` | `#A7E6D5` |
| `--ai-bg` | `aiBg` | `#EFF5F2`（=low） | `#F1EDE4`（=low） | `#EFF5F2`（=low） |
| `--ai-fg` | `aiFg` | `#191C1B`（=on-s） | `#1A1A18`（=on-s） | `#191C1B`（=on-s） |
| `--av-bg` | `avBg` | `#DEE4E1` | `#DEE4E1` | `#1F4A42` |
| `--av-fg` | `avFg` | `#496F66` | `#496F66` | `#A7E6D5` |
| `--err-c` | `errC` | `#BA1A1A` | `#BA1A1A` | `#BA1A1A` |
| `--err-bg` | `errBg` | `#FFDAD6` | `#FFDAD6` | `#FFDAD6` |
| `--on-err-bg` | `onErrBg` | `#410002` | `#410002` | `#410002` |
| `--icon-c` | `iconC` | `#191C1B` | `#191C1B` | `#1F4A42` |
| `--sel-bg` | `selBg` | `#D9F6EC` | `#F0E4D6` | `#D9F6EC` |
| `--sel-bar` | `selBar` | `#046B5C` | `#B4481B` | `#046B5C` |

| 形态 | A 清透 | E 纸感 | H 墨色 |
|---|---|---|---|
| 气泡圆角 (`--r-bubble`) | 16px | 8px | 14px |
| 卡片圆角 (`--r-card`) | 14px | 6px | 12px |
| chip 圆角 (`--r-chip`) | 999px | 3px | 8px |
| 输入框圆角 (`--r-field`) | 999px | 6px | 12px |
| 顶栏字号 (`--fs-bar`) | 20px | 20px | 22px |
| 列表标题 (`--fs-title`) | 16px | **15px** | 16px |
| 正文字号 (`--fs-body`) | 15px | 16px | 16px |
| 元信息 (`--fs-sub`) | 13px | 12.5px | 13px |
| 行高倍数 (`--lh`) | 1.6 | 1.7 | 1.55 |
| 列表行高 (`--row-h`) | 68px | 68px | 68px |
| 行内间距 (`--gap`) | 12px | 10px | 12px |
| 卡片描边 (`--card-bd`) | 0px | 1px | 0px |
| 标题字重 (`--title-w`) | 600 | 700 | 700 |
| 元信息字体 (`--meta-font`) | 系统无衬线 | 系统无衬线 | 系统无衬线 |

### 硬性约束

1. `primaryContainer` 与 `surfaceContainerLow` 的明度差 ≥ 8%，否则 chip 和选中态会糊在一起。
2. 错误条和停止按钮用 **`errorContainer` + `onErrorContainer`**，不是 `error` 铺满。
3. 全局**零阴影**：不用 elevation、boxShadow。层次靠 surface → low → high → highest 四档底色。
4. 零阴影下 FAB 靠 **1px `#8CCDBB` 描边 + `primaryContainer` 底** 浮出（v3.5 定稿：底色按 `full.css` 的 `--p-c`，描边用 `--fab-line`；此前"surface 底"的写法作废）。
5. **E 是衬线皮肤**，主字体必须换成宋体/明朝体（`Songti SC` / `Noto Serif CJK SC` / `SimSun`）。这是三套皮肤气质拉开的关键——三套如果都用黑体，换了等于没换。
6. **H 的列表行高是 78**，因为字号最大；A 和 E 是 68。
7. **交互态只允许用底色档位表达**（v3.1）：所有可点元素（chip / 行 / 按钮）的按下反馈只能改「`surface` → `low` → `high` 的档位」或透明度，**禁止** Material 默认的 `highlightColor` 与 `InkSparkle/InkRipple` 水波纹 —— Ink 按**触摸框**画（48dp），而视觉本体只有 32dp，多出来的那一圈深色矩形在浅色皮肤上就是「点一下闪一块灰」。规格见 §4.8。

## 4. 组件规格

### 4.1 顶栏

| 项 | 值 |
|---|---|
| 高度 | 56 |
| 水平内边距 | 左右各 4（图标本身 48 触摸区） |
| 图标 | 24，`iconColor` |
| 标题 | `fs-bar`，`title-w`，`onSurface` |
| 底 | 无边线、无阴影 |

### 4.2 会话列表行

| 项 | 值 |
|---|---|
| 行高 | 68（三套一致） |
| 左右内边距 | 16 |
| 头像 | 见 `--av-r`（三套统一 17 = 34 的一半，**圆形**；v3.5 前 E 写成 6 会做成圆角方块，已修） |
| 标题 ↔ 元信息 | 间距 5 |
| 元信息 | `fs-sub`，`onSurfaceVariant`，E 走等宽 |
| 分割线 | 1px `outlineVariant`，左缩进 62 |
| 当前行高亮 | 左边 3dp 竖条 `sel-bar`，**不改变任何布局尺寸** |

**选中态只允许改三样**：容器底色、描边、文字粗细。
**禁止**改 margin / padding / 行高 / 字号 / 头像尺寸——一改文字就会位移。

### 4.3 消息气泡

| 项 | 用户 | AI |
|---|---|---|
| 容器 | `primaryContainer` | `aiBubble` |
| 文字 | `onPrimaryContainer` | `onAiBubble` |
| 圆角 | `r-bubble` | `r-bubble` |
| 最大宽度 | 屏幕宽 − 88 | 屏幕宽 − 56 |
| 内外边距 | 水平 14 / 垂直 10 | 水平 16 / 垂直 14 |
| 正文行高 | `lh` | `lh` |

### 4.4 底部动作条（朗读 / 复制 / 重答 / 分支）

| 项 | 值 |
|---|---|
| 位置 | AI 气泡下方，左缩进 30 |
| 图标 | 15 |
| 文字 | 12，`onSurfaceVariant` |
| 图标↔文字 | 5 |
| 项间距 | 16 |
| 文案 | **必须带文字**，不允许只有图标 |

### 4.5 发送键 / FAB

| 项 | 发送键 | FAB |
|---|---|---|
| 尺寸 | 44 | 56 |
| 圆角 | `r-send` | `r-fab` = 16 |
| 底色 | `send-bg` | **`primaryContainer`（`--p-c`）** |
| 前景 | `send-fg` | `onPrimaryContainer`（`--on-p-c`） |
| 描边 | 无 | **1px `--fab-line`（`#8CCDBB`）** |
| 阴影 | **无** | **无** |

> v3.5 定稿：底色取 `primaryContainer`（与 `full.css` 的 `.fab` 一致）；"surface 底 + 描边"那套旧写法作废。

### 4.6 底部弹层 / 对话框

| 项 | 值 |
|---|---|
| 圆角 | `r-sheet`，只圆上两角 |
| 顶部抓手 | 36 × 4，`outlineVariant`，圆角 999 |
| 内边距 | 20 |
| 标题 | 18，`title-w` |
| 按钮 | 高 38，圆角 `r-card`，左右内边距 16 |
| 遮罩 | `black 50%` |

**危险操作**（删除）按钮：`errorContainer` 底 + `onErrorContainer` 字。

### 4.7 单选 / 复选框

| 项 | 规格 |
|---|---|
| 单选：未选 | 20，2px `outline` 描边 |
| 单选：已选 | **外环 2px `sel-bar` + 中心 8dp 实心点 + 中间留白**，不是整块实心 |
| 复选：未选 | 20，2px `outline` 描边，圆角 `r-cb` |
| 复选：已选 | `sel-bar` 实心 + 白色 ✓，圆角 `r-cb` |

### 4.8 chip（联网 / 思考 / 上下文）

| 项 | 值 |
|---|---|
| 高度 | 32 |
| 左右内边距 | 12 |
| 圆角 | `r-chip` |
| 图标 | **15**（不要 13、14——13 以下 Material 图标会糊） |
| 文字 | 12 |
| 开态 | `primaryContainer` 底 + `onPrimaryContainer` 字 |
| 关态 | 透明底 + `outlineVariant` 描边 + `onSurfaceVariant` 字 |
| 文案格式 | `联网 · 关` / `思考 · 中` / `20 轮`，**用分隔号，别用「思考中」**（会和状态混淆） |
| **触摸框**（v3.1） | 48（上下各 8 留白），**但底色只画在 32 的本体上**，触点框永远不着色 |
| **按压态（关态）**（v3.1） | 本体底 = `high`，过渡 120ms；**不动文字位置、不改字号** |
| **按压态（开态）**（v3.1） | 保持 `primaryContainer`，**不再加深**（再加深就是"整块闪一下"） |
| **反馈方式**（v3.1） | `splash = none`、`highlight = none`：**禁止** Material 默认水波纹/灰色高亮 |

> 为什么写这条（v3.1）：上一版规格只定义了「开态 / 关态」两个静态样式，没定义"按下"，工程侧就继承了 Material 默认行为——`highlightColor` 与 `InkSparkle` 铺满 **48dp 触点框**，而芯片本体只有 32dp，于是点「联网 / 思考 / 上下文」时肉眼看到的是**一块比芯片大一圈的灰色矩形闪一下**。设计补规格，工程同步改 `NoSplash` + 自绘按压底。

### 4.9 轻提示（toast）

| 项 | 值 |
|---|---|
| 位置 | 屏幕**顶部**：状态栏 + AppBar(56) + 8；左右 16；水平居中；最大宽度 480 |
| 层级 | Overlay 浮层，**不参与布局**（出现 / 消失时页面不位移） |
| 底色 / 字色 | `inverseSurface` / `onInverseSurface`（浅色皮肤 = 深底浅字，深色皮肤反之） |
| 圆角 | `r-card` |
| 内边距 | 左右 16 / 上下 12 |
| 文字 | 14，单行优先，最多两行 |
| 时长 | 2s 自动消失；出现 120ms 淡入 + 8dp 上移；同屏只留一条（新的顶掉旧的） |
| 交互 | **不拦手势**（`IgnorePointer`）：不挡输入、不挡滚动、不挡点按 |
| 禁止 | ❌ 底部 SnackBar —— 聊天页底部是输入栏 + 工具芯片，相册页底部是「预览 / 发送」，编辑器底部是工具条，弹在底部必然盖住用户正在点的地方 |

> 为什么写这条（v3.2）：旧实现用 `ScaffoldMessenger` 的 SnackBar，只能贴 Scaffold 底部。聊天页里点「思考」芯片弹出的「思考：开（中）」正好糊在输入框上（用户截图里画了红框）。提示属于"看过就该消失"的信息，位置必须避开**输入区 / 主要操作区**，所以统一挪到顶部浮层。

---

## 5. 落地顺序（照这个顺序做，省得返工）

1. **先做 token 层**：`SkinTokens` + `SkinScope`，三套数据填满，写一个隐藏入口能在 App 内切皮肤。
2. **拿一个页面打通**：会话列表。这个页面组件最少，但覆盖了行高、头像、分割线、选中态、空态。
3. **切三套看差异**：同一个列表在三套下必须都成立。E 会发现等宽字体没生效、H 会发现字重不够。
4. **再铺聊天页**：气泡、思考折叠、代码块、动作条。这页最容易漏 `r-bubble` 和 `aiBubble`。
5. **最后设置页和弹层**。设置页注意：**「对话默认」只影响新会话**，当前会话的开关在聊天页 chip 上，这两处不能混。

---

## 6. 已知限制（这版没覆盖，别当成缺陷报）

| 项 | 状态 |
|---|---|
| 深色模式 | 只有推导值，没有采样，暂不交付 |
| 横屏 / 平板 | 未设计 |
| 系统大字号 1.3× / 1.5× | 未验证，E 的 12px 元信息在 1.3× 下可能需要重排 |
| 无障碍 Semantics | 未标注 |
| 离线态 | 未设计 |
| `language` 图标 15px | 经纬线会糊，建议该位置改纯文字或开到 20 |

---

## 7. 交付物清单

```
SPEC.md            本文档
icons.md           21 + 10 个图标 → Flutter Icons 名
CHECKLIST.md       验收清单，逐条勾
reference/
  full-list.html   会话列表 13 屏（含所有状态）
  full-chat.html   聊天页 11 屏
  full-settings.html 设置与弹层 6 屏
  full.css         所有组件的真实 CSS，可直接查尺寸
screens/
  01..09-*.png     三套 × 三个页面的 1360px 静态图
```

**HTML 是唯一真值来源**。文档和 HTML 冲突时以 HTML 为准，然后回来改文档。
