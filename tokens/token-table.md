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
| `--ai-bg` | `aiBg` | `#A0F2DF` | `#A0F2DF` | `#1F4A42` |
| `--ai-fg` | `aiFg` | `#005045` | `#005045` | `#A7E6D5` |
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
