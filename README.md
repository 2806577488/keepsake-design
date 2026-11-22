# Keepsake 设计稿

Keepsake 是一个本地优先的 Android 聊天应用。这份仓库是它的**界面设计稿与落地规格**，不是应用源码。

三套皮肤共用一套 UI 代码，切皮肤只换 token。设计稿用 HTML/CSS 写成可交互原型，1dp = 1px，画布 411×892。

---

## 三套皮肤

不是三个配色，是三种形态。

| | **A 清透** | **E 纸感** | **H 墨色** |
|---|---|---|---|
| 性格 | 干净、轻、有空气感 | 纸、书、慢 | 重、工具、高对比 |
| 字体 | 系统无衬线 | **宋体** | 系统无衬线 |
| 圆角 | 大 + 胶囊（16/14/999） | 小（8/6/3） | 中（14/12） |
| 卡片 | 无边框，靠底色分层 | **1px 描边** | 无边框，靠深色块面 |
| 图标 | 实心 24 | **描边 24** | 实心 26 |
| 字重 | 600 | 700 | 700 |
| 主色块 | 薄荷绿 `#A0F2DF` | 陶土橙 `#B4481B` | 深青 `#1F4A42` |

**E 必须换字体**——三套如果都用黑体，换了等于没换。这是三套皮肤能不能"看起来是三套"的命门。

---

## 目录

```
.
├─ SPEC.md                     完整规格（token、组件、红线）
├─ CHANGELOG.md                版本历史
├─ docs/
│  ├─ v3-改动说明.md            相对 v2 改了什么（先看这个）
│  ├─ 设计师回应-拍板与token表.md  对工程师提出矛盾的逐条拍板
│  ├─ icons.md                 36 个图标映射（Material 官方名）
│  └─ CHECKLIST.md             23 条验收规则
├─ tokens/
│  ├─ skin_tokens.dart         可直接抄进项目的常量
│  └─ token-table.md           三套 token 对照表
├─ reference/                  可交互 HTML 原型
│  ├─ index.html               入口
│  ├─ full-list.html           列表 13 屏
│  ├─ full-chat.html           聊天 11 屏
│  ├─ full-settings.html       设置 6 屏
│  └─ full.css                 样式
├─ screens/                    9 张渲染图（411×892）
└─ tools/
   ├─ check_consistency.py     设计稿 vs 代码 的一致性校验
   └─ design_audit.py          静态审计（对比度、圆角、字号、阴影）
```

---

## 怎么看设计稿

用浏览器直接打开 `reference/index.html`。

**切皮肤**：在任意页面后面加参数。

```
reference/full-list.html?set=a     A 清透
reference/full-list.html?set=e     E 纸感（宋体）
reference/full-list.html?set=h     H 墨色
```

不带参数是 A。

> 改动 HTML 后如果浏览器还显示旧内容，按 `Ctrl+F5` 强刷。

---

## 怎么验

### 1. 一致性校验（必须跑）

```
python tools/check_consistency.py \
  --ref reference/full-list.html \
  --dart tokens/skin_tokens.dart \
  --spec SPEC.md
```

对比设计稿和 dart 里 27 个数值（3 套 × 9 项），不一致就退出非 0。

**这条不是可选的。** v3 第一次交付时 `skin_tokens.dart` 里 E 的 `fsTitle` 还是 16、文档写 15，因为改了 HTML 没重新生成 dart。肉眼几乎发现不了。

### 2. 静态审计

```
python tools/design_audit.py reference/full-list.html reference/full.css
```

查对比度（WCAG）、圆角是否在 M3 刻度上、字号阶梯、行高、零阴影、硬编码颜色。

---

## 设计红线

落地时这些不能破，否则会有 bug 或观感崩坏：

1. **全局零阴影**——不用 elevation、boxShadow。层次靠 surface → low → high 四档底色。
2. **三套行高一致（68）**——切皮肤时列表长度不能跳。E 的紧凑感靠字号和宋体，不靠压行高。
3. **选中态只许改颜色、描边、字重**——不许改 margin / padding / 行高 / 字号。一改文字就跳。
4. **换占位必须保持尺寸**——多选时复选框放在 34×34 槽位里（框本身 20×20），不能拿 20 的框直接顶 34 的头像。
5. **图标用 Material 官方名**——不要 emoji、不要 Unicode 符号。
6. **错误态用 `errorContainer` + `onErrorContainer`**——不是 `error` 铺满。
7. **E 的主字体必须是宋体**——这是三套皮肤的差异核心。

完整 23 条见 `docs/CHECKLIST.md`。

---

## 已知不做的区域

- 深色模式（没有独立设计，代码里只有推导值）
- 横屏 / 平板
- 系统大字号 1.3× / 1.5×
- 无障碍 Semantics
- 离线态、加载骨架
- 搜索命中高亮

这些需要单独设计一轮，不是顺手能做对的。

---

## 版本

当前 **v3**。变化见 `CHANGELOG.md`，相对上一版的细节见 `docs/v3-改动说明.md`。

---

## 设计工具

- 画布 411dp × 892dp，1dp = 1px
- 原型用 HTML/CSS 手写，不依赖 Figma
- 截图用 Edge headless，DPR 1
- 字体：A/H 用系统无衬线，E 用宋体（Songti SC / Noto Serif CJK SC / SimSun）
