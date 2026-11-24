# Keepsake 图标对照表（设计稿 ↔ Flutter）

设计稿里 21 个图标，全部对应 Material Icons。下面是**唯一权威清单**：
左右两列必须一致，不要在 Flutter 里自己换近似的图标。

尺寸按皮肤：A = 24，E = 24（outlined），H = 26。

---

## 图标表

| # | 用途 | 设计稿名 | Flutter filled（A / H） | Flutter outlined（E） | 尺寸 |
|---|---|---|---|---|---|
| 1 | 返回 | `back` | `Icons.arrow_back` | `Icons.arrow_back` | 24 |
| 2 | 更多（⋮） | `more` | `Icons.more_vert` | `Icons.more_vert` | 24 |
| 3 | 展开 | `down` | `Icons.keyboard_arrow_down` | `Icons.keyboard_arrow_down` | 14 / 15 |
| 4 | 收起 | `up` | `Icons.keyboard_arrow_up` | `Icons.keyboard_arrow_up` | 14 / 15 |
| 5 | 停止生成 | `stop` | `Icons.stop` | `Icons.stop_circle_outlined` | 20 |
| 6 | 置顶 / 星标 | `star` | `Icons.star` | `Icons.star_border` | 14 / 20 |
| 7 | 联网搜索 | `globe` | `Icons.language` | `Icons.language` | 15 |
| 8 | 深度思考 | `bulb` | `Icons.lightbulb` | `Icons.lightbulb_outline` | 15 |
| 9 | 上下文轮数 | `clock` | `Icons.schedule` | `Icons.schedule_outlined` | 15 |
| 10 | 新建对话 | `plus` | `Icons.add` | `Icons.add` | 24 |
| 11 | 语音输入 | `mic` | `Icons.mic` | `Icons.mic_none` | 20 / 24 |
| 12 | 复制 | `copy` | `Icons.content_copy` | `Icons.content_copy_outlined` | 15 / 16 |
| 13 | 朗读 | `speak` | `Icons.volume_up` | `Icons.volume_up_outlined` | 15 / 16 |
| 14 | 重答 | `redo` | `Icons.refresh` | `Icons.refresh` | 15 / 16 |
| 15 | 分支 | `branch` | `Icons.call_split` | `Icons.call_split_outlined` | 15 / 16 |
| 16 | 警告 | `warn` | `Icons.warning_amber_rounded` | `Icons.warning_amber` | 16 / 20 |
| 17 | 关闭 | `close` | `Icons.close` | `Icons.close` | 20 / 24 |
| 18 | 搜索 | `search` | `Icons.search` | `Icons.search` | 24 |
| 19 | 导出 / 打开 | `open` | `Icons.open_in_new` | `Icons.open_in_new` | 18 / 20 |
| 20 | 用量 / 统计 | `eq` | `Icons.graphic_eq` | `Icons.graphic_eq` | 16 |
| 21 | 抽屉 （列表页左上） | — | `Icons.menu` | `Icons.menu` | 24 |

> 规则：E 皮肤凡是表里 outlined 列写成「同左」的，说明 Material 这套图标没有 outlined 变体，
> 直接复用 filled 即可——不是漏了。

---

## 三套皮肤怎么切

| 皮肤 | 图标风格 | 尺寸 | 颜色 |
|---|---|---|---|
| A 清透 | filled | 24 | `onSurface` |
| E 纸感 | outlined | 24 | `onSurfaceVariant` |
| H 墨色 | filled | 26 | `#1F4A42` |

Flutter 里用一个函数收口，不要在页面里散写：

```dart
IconData appIcon(IconData filled, {IconData? outlined, required Skin skin}) {
  switch (skin) {
    case Skin.e: return outlined ?? filled;
    default:     return filled;
  }
}
```

尺寸同理：

```dart
double iconSize(BuildContext c) => switch (skinOf(c)) {
  Skin.a => 24,
  Skin.e => 24,
  Skin.h => 26,
};
```

---

## 两处容易踩的坑

**1. 行内小图标不要用 24。**
chip 里那三个（联网 / 思考 / 上下文）是 **15**（SPEC §4.8 硬性要求，工程 `kChipIconSize = 15`），不是 24、也不是 13–14。
13 及以下 Material 图标会糊——这也是为什么定为 15 而不是更小。

**2. `Icons.stop` 是实心方块。**
停止生成按钮在 E 皮肤里要配 outlined 的圆形版（`stop_circle_outlined`），
否则停止键在纸感皮肤里会显得比发送键还重。

---

## 还没进设计稿的图标

下面这些功能在原稿里没有对应界面，图标先定好，做的时候直接用：

| 用途 | Flutter |
|---|---|
| 设置 | `Icons.settings` / `Icons.settings_outlined` |
| 导出文件 | `Icons.file_download_outlined` |
| 导入 | `Icons.file_upload_outlined` |
| 编辑 | `Icons.edit_outlined` |
| 删除 | `Icons.delete_outline` |
| 多选 | `Icons.checklist` |
| 附件 | `Icons.attach_file` |
| 图片 | `Icons.image_outlined` |
| 深色模式 | `Icons.dark_mode_outlined` |
| 用量详情 | `Icons.insights` |
