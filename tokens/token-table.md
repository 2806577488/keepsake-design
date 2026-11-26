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
| `--ai-bg` | `aiBg` | `#EFF5F2`（= `--low`） | `#F1EDE4`（= `--low`） | `#EFF5F2`（= `--low`） |
| `--ai-fg` | `aiFg` | `#191C1B`（= `--on-s`） | `#1A1A18`（= `--on-s`） | `#191C1B`（= `--on-s`） |
| `--av-bg` | `avBg` | `#DEE4E1` | `#DEE4E1` | `#1F4A42` |
| `--av-fg` | `avFg` | `#496F66` | `#496F66` | `#A7E6D5` |
| `--err-c` | `errC` | `#BA1A1A` | `#BA1A1A` | `#BA1A1A` |
| `--err-bg` | `errBg` | `#FFDAD6` | `#FFDAD6` | `#FFDAD6` |
| `--on-err-bg` | `onErrBg` | `#410002` | `#410002` | `#410002` |
| `--icon-c` | `iconC` | `#191C1B` | `#191C1B` | `#1F4A42` |
| `--sel-bg` | `selBg` | `#D9F6EC` | `#F0E4D6` | `#D9F6EC` |
| `--sel-bar` | `selBar` | `#046B5C` | `#B4481B` | `#046B5C` |
| `--fab-line` | `fabLine` | `#8CCDBB` | `#8CCDBB` | `#8CCDBB` |
| `--av-r` | `avatarRadius` | 17px（圆形） | 17px（圆形） | 17px（圆形） |

| 形态 | A 清透 | E 纸感 | H 墨色 |
|---|---|---|---|
| 气泡圆角 (`--r-bubble`) | 16px | 8px | 14px |
| 卡片圆角 (`--r-card`) | 14px | 6px | 12px |
| chip 圆角 (`--r-chip`) | 999px | 3px | 8px |
| 输入框圆角 (`--r-field`) | 999px | 6px | 12px |
| 顶栏字号 (`--fs-bar`) | 20px | 20px | 22px |
| 列表标题 (`--fs-title`) | 16px | 15px | 16px |
| 正文字号 (`--fs-body`) | 15px | 16px | 16px |
| 元信息 (`--fs-sub`) | 13px | 12.5px | 13px |
| 行高倍数 (`--lh`) | 1.6 | 1.7 | 1.55 |
| 列表行高 (`--row-h`) | 68px | 68px | 68px |
| 行内间距 (`--gap`) | 12px | 10px | 12px |
| 卡片描边 (`--card-bd`) | 0px | 1px | 0px |
| 标题字重 (`--title-w`) |  | 700 | 700 |
| 元信息字体 (`--meta-font`) |  |  |  |

### 交互态（v3.1 新增，不新增颜色 token）

| 状态 | A 清透 | E 纸感 | H 墨色 | 说明 |
|---|---|---|---|---|
| chip 关态默认 | 透明底 + `--ov` 1px 描边 | 同左 | 同左 | 触摸框 48，底色只画 32 的本体 |
| chip 关态**按下** | `--high` | `--high` | `--high` | 120ms，文字位置不动 |
| chip 开态默认 / 按下 | `--p-c` / 保持 `--p-c` | 同左 | 同左 | 开态按下**不加深** |
| 水波纹 / 灰色高亮 | **禁用** | **禁用** | **禁用** | `splashFactory = none`、`highlight = none`；HTML 侧同时关掉 `-webkit-tap-highlight-color` |

> 复用 `--high` 就够，不新增 token：按压态是"层级档位"（surface → low → high），不是一种新颜色。三套皮肤各自的 `--high` 明度差都能表达按下。

### 品牌 / 应用图标（v3.9 新增，**不进三套皮肤**）

图标三套皮肤共用一枚，不随皮肤切换，所以这些值**不写进 `skin_tokens.dart`**，
只在 `tools/make_icon.py` 顶部与 `docs/app-icon.md` 里维护。

| 用途 | 值 | 说明 |
|---|---|---|
| 图标底色渐变起点 | `#0A332C` | 图标专用新色 |
| 图标底色渐变终点 | `#2F6B5F` | = 工程侧 `kSeedColor` |
| 左上高光 | `#A0F2DF` @ 16% | 复用 `--p-c` |
| 气泡 | `#F2FFFA` | 图标专用（近白，比 `--surface` 更亮一档） |
| 声纹 | `#064239` | `--on-p-c`（`#005045`）的加深版，48px 下仍与气泡拉开明度 |

> 界面里**不要**用 `#0A332C` / `#2F6B5F`：它们只出现在图标与品牌物料上。
> 界面主色仍按 §2 的 `pC` / `onPC` / `sendBg`。
