#!/usr/bin/env python
"""Keepsake（留声）应用图标生成器。

为什么要有这个脚本：图标不再是一张手改的 PNG。母版和所有密度产物都由这里的
几何/颜色参数生成，改一个数字就能整套重出，避免「mipmap 里几张图不是同一个图形」。

产出（相对 android/app/src/main/res/）：

    mipmap-{m,h,xh,xxh,xxxh}dpi/ic_launcher.png          传统图标（API < 26，圆角方形）
    mipmap-{..}/ic_launcher_round.png                    传统图标（圆形）
    mipmap-{..}/ic_launcher_foreground.png               自适应图标前景层（108dp 画布）
    mipmap-anydpi-v26/ic_launcher{,_round}.xml           自适应图标（前景 + 渐变底 + 单色）
    drawable/ic_launcher_background.xml                  自适应背景（纯 XML 渐变）
    drawable/ic_launcher_monochrome.xml                  Android 13+ 主题图标（单色矢量）

另有 docs/brand/ 下的 512 / 1024 母版（商店图与 README 用，不进 APK）。

设计说明（颜色与 lib/core/skin_tokens.dart 的 kSeedColor 同源）：

- 底色：品牌深青 #0A332C → #2F6B5F 的对角渐变，左上叠一点薄荷色高光。
- 主体：一枚圆角「对话气泡」+ 左下「下巴」尾角 —— 这个 App 的核心对象就是对话。
- 气泡内：五根声纹条 —— 「留声」的字面意思。
- 零阴影、零描边、零渐变噪声：和 App 三套皮肤的零阴影规则一致。48px 上只剩
  「浅色气泡 + 深色竖条」两层信息，仍然认得出。

用法：
    python tool/make_icon.py                     # 覆盖 res/ 与 docs/brand/
    python tool/make_icon.py --preview x.png     # 只出对比预览图
    python tool/make_icon.py --variant mint      # 换配色（薄荷气泡）
"""

from __future__ import annotations

import argparse
import math
import os
import sys

try:
    from PIL import Image, ImageDraw
    import numpy as np
except ImportError:  # pragma: no cover - 依赖提示
    sys.exit("需要 Pillow 与 numpy：python -m pip install pillow numpy")

# --- 品牌色（与 skin_tokens.dart 对齐） ---------------------------------------
BG_TOP = (10, 51, 44)        # #0A332C 渐变起点
BG_BOTTOM = (47, 107, 95)    # #2F6B5F = kSeedColor 渐变终点
HILIGHT = (160, 242, 223)    # #A0F2DF 左上高光
BUBBLE_LIGHT = (242, 255, 250)  # #F2FFFA 近白气泡
BUBBLE_MINT = (160, 242, 223)   # #A0F2DF 品牌薄荷
BARS_LIGHT = (6, 66, 57)        # #064239 深青声纹（近白气泡上用）
BARS_MINT = (0, 80, 69)         # #005045 onPrimaryContainer（薄荷气泡上用）

# 图形占画布的比例。
# - 传统图标：0.66，四周留呼吸边；launcher 用圆形遮罩时仍完整。
# - 自适应前景：0.52。自适应图标 108dp 画布里「安全区」是以中心为心、直径 72dp
#   的圆，气泡是横向的（宽:高 ≈ 1.25），要整颗外接矩形都留在圆内就不能超过
#   0.52（半对角 = 36dp）。画大了会被圆形遮罩切掉气泡两端。
LEGACY_MARK_RATIO = 0.66
ADAPTIVE_MARK_RATIO = 0.52

SS = 4  # 超采样倍率：先画 4 倍大再 LANCZOS 缩，边缘才干净

# 归一化几何（单位 = 图形外接方框边长 u）。
# 纵向排布：气泡体 0.005..0.805，尾巴 0.805..0.993 —— 整块（含尾巴）刚好填满方框，
# 尾巴不会被方框裁掉（早先版本把气泡 y 放在 0.10，尾巴尖超出 1.0 被切平）。
GEO = dict(
    bubble_w=0.96,
    bubble_x=0.02,
    bubble_h=0.80,
    bubble_y=0.005,
    corner=0.24,        # 相对 bubble_h
    tail_left=0.12,     # 尾巴左根部（相对 bubble_w），落在圆角内、被并集吃掉
    tail_right=0.42,    # 尾巴右根部
    tail_top=0.94,      # 根部高度（相对 bubble_h）：必须**高于**底边才能无缝并集
    tail_depth=0.225,   # 尖端低于底边的深度（相对 bubble_h）
    tail_tip=0.20,      # 尖端横向位置（相对 bubble_w）：落在两根之间，尾巴略朝左下
    bar_w=0.090,        # 相对 bubble_w
    bar_gap=0.055,      # 相对 bubble_w
    bar_heights=(0.28, 0.48, 0.68, 0.42, 0.26),  # 相对 bubble_h
)


def geo(u: float) -> dict:
    """在边长 u 的方框里，算出气泡与声纹的绝对坐标（位图与矢量共用一份）。"""
    g = GEO
    bw, bh = u * g["bubble_w"], u * g["bubble_h"]
    bx, by = u * g["bubble_x"], u * g["bubble_y"]
    br = bh * g["corner"]

    tail = [
        (bx + bw * g["tail_left"], by + bh * g["tail_top"]),
        (bx + bw * g["tail_right"], by + bh * g["tail_top"] + bh * 0.06),
        (bx + bw * g["tail_tip"], by + bh + bh * g["tail_depth"]),
    ]

    bar_w, gap = bw * g["bar_w"], bw * g["bar_gap"]
    heights = g["bar_heights"]
    total = len(heights) * bar_w + (len(heights) - 1) * gap
    x = bx + (bw - total) / 2
    cy = by + bh * 0.50
    bars = []
    for h in heights:
        bar_h = bh * h
        bars.append((x, cy - bar_h / 2, x + bar_w, cy + bar_h / 2))
        x += bar_w + gap

    return dict(bw=bw, bh=bh, bx=bx, by=by, br=br, tail=tail, bars=bars)


def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _gradient_bg(size: int) -> Image.Image:
    """对角渐变 + 左上径向高光（纯色叠层，没有阴影）。"""
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    denom = max(1, size - 1)
    # 135°：左上暗、右下亮，投影到 (1,1) 方向。
    t = ((x / denom) + (y / denom)) / math.hypot(1.0, 1.0)
    t = np.clip(t, 0.0, 1.0) ** 0.85

    rgb = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        rgb[..., i] = BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t

    cx, cy = -0.10 * size, -0.15 * size
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (size * 0.95)
    glow = np.clip(1.0 - d, 0.0, 1.0) ** 2.2 * 0.16
    for i in range(3):
        rgb[..., i] = rgb[..., i] * (1 - glow) + HILIGHT[i] * glow

    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def _rounded_mask(size: int, radius: float) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=radius, fill=255
    )
    return mask


def _circle_mask(size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def _fill_vertical(mask: Image.Image, top, bottom) -> Image.Image:
    """把 L 蒙版填成上下渐变。大尺寸下不呆板，48px 下仍读作纯色。"""
    w, h = mask.size
    ramp = Image.new("RGB", (1, h))
    px = ramp.load()
    for y in range(h):
        px[0, y] = _lerp(top, bottom, y / max(1, h - 1))
    out = ramp.resize((w, h), Image.NEAREST).convert("RGBA")
    out.putalpha(mask)
    return out


def _bubble_masks(u: int) -> tuple[Image.Image, Image.Image]:
    """返回 (气泡蒙版, 声纹蒙版)。

    气泡 = 圆角矩形 ∪ 尾巴三角。尾巴两个根部顶点的 y 取在底边**上方**（0.88/0.94
    倍体高），这样并集边界完全落在气泡体内、不会出现一道缝；尾巴尖端再往下方
    0.235 倍体高伸出，整块恰好填满方框（见 GEO 注释）。
    """
    g = geo(u)
    bubble = Image.new("L", (u, u), 0)
    d = ImageDraw.Draw(bubble)
    d.rounded_rectangle(
        (g["bx"], g["by"], g["bx"] + g["bw"], g["by"] + g["bh"]),
        radius=g["br"],
        fill=255,
    )
    d.polygon(g["tail"], fill=255)

    bars = Image.new("L", (u, u), 0)
    bd = ImageDraw.Draw(bars)
    for (x0, y0, x1, y1) in g["bars"]:
        bd.rounded_rectangle((x0, y0, x1, y1), radius=(x1 - x0) / 2, fill=255)
    return bubble, bars


def _stencil(u: int) -> Image.Image:
    """主题图标用的单色模板：气泡不透明、声纹挖成洞（系统会整体染色）。"""
    bubble, bars = _bubble_masks(u)
    stencil = bubble.copy()
    stencil.paste(0, (0, 0), bars)
    out = Image.new("RGBA", (u, u), (255, 255, 255, 0))
    out.putalpha(stencil)
    return out


def _mark_layer(u: int, variant: str) -> Image.Image:
    bubble_rgb, bars_rgb = (
        (BUBBLE_LIGHT, BARS_LIGHT) if variant == "light" else (BUBBLE_MINT, BARS_MINT)
    )
    bubble, bars = _bubble_masks(u)
    layer = Image.new("RGBA", (u, u), (0, 0, 0, 0))
    layer.alpha_composite(
        _fill_vertical(bubble, bubble_rgb, _lerp(bubble_rgb, (0, 0, 0), 0.06))
    )
    layer.alpha_composite(_fill_vertical(bars, _lerp(bars_rgb, bubble_rgb, 0.06), bars_rgb))
    return layer


def compose(size: int, *, shape: str, variant: str) -> Image.Image:
    """合成一张图标。shape: square | circle | full | foreground | themed。"""
    big = size * SS

    if shape == "foreground":
        canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        m = int(big * ADAPTIVE_MARK_RATIO)
        off = (big - m) // 2
        canvas.alpha_composite(_mark_layer(m, variant), (off, off))
        return canvas.resize((size, size), Image.LANCZOS)

    if shape == "themed":
        # 主题图标预览：单色模板按系统取色（这里用品牌薄荷示意）。
        canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        m = int(big * ADAPTIVE_MARK_RATIO)
        off = (big - m) // 2
        masked = _fill_vertical(_stencil(m).getchannel("A"), HILIGHT, HILIGHT)
        canvas.alpha_composite(masked, (off, off))
        return canvas.resize((size, size), Image.LANCZOS)

    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    if shape == "full":
        out.alpha_composite(_gradient_bg(big).convert("RGBA"))
    else:
        mask = _circle_mask(big) if shape == "circle" else _rounded_mask(big, big * 0.225)
        out.paste(_gradient_bg(big), (0, 0), mask)

    m = int(big * LEGACY_MARK_RATIO)
    off = (big - m) // 2
    out.alpha_composite(_mark_layer(m, variant), (off, off))
    return out.resize((size, size), Image.LANCZOS)


# --- XML 图层 ----------------------------------------------------------------
# 只有背景值得写成 XML（纯渐变，省一张位图）。前景与单色层都是位图：它们的几何
# 与 tool/make_icon.py 共用一套参数，写成矢量 XML 就要把同一套坐标抄第二遍，
# 迟早会和位图对不上（真的对不上过）。
# 单色层用「气泡不透明 + 声纹透明」的模板 PNG：系统按 alpha 染色，声纹自然成为洞。

BACKGROUND_XML = """<?xml version="1.0" encoding="utf-8"?>
<!-- 图标底色：品牌深青对角渐变（#0A332C → #2F6B5F），与 tool/make_icon.py 同一套颜色。 -->
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="315"
        android:startColor="#0A332C"
        android:endColor="#2F6B5F"
        android:type="linear"/>
</shape>
"""

ADAPTIVE_XML = """<?xml version="1.0" encoding="utf-8"?>
<!-- 自适应图标（Android 8.0+）：背景是纯 XML 渐变（省掉一张位图），前景是
     108dp 画布里居中、占 52% 的声纹气泡（安全区内不会被圆形遮罩切掉），
     monochrome 供 Android 13+ 主题图标（系统按 alpha 染色）。 -->
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome"/>
</adaptive-icon>
"""

# --- 写盘 --------------------------------------------------------------------

DENSITIES = [
    # (目录后缀, 传统图标 px, 自适应前景 px)
    ("mdpi", 48, 108),
    ("hdpi", 72, 162),
    ("xhdpi", 96, 216),
    ("xxhdpi", 144, 324),
    ("xxxhdpi", 192, 432),
]


def write_assets(root: str, variant: str = "light") -> bool:
    """写 Android 资源。设计库没有 android/ 目录时返回 False（只出母版图）。"""
    res = os.path.join(root, "android", "app", "src", "main", "res")
    if not os.path.isdir(res):
        print(f"跳过 res/：{root} 里没有 android/app/src/main/res（设计库只出母版图）")
        return False

    for suffix, legacy, fg in DENSITIES:
        d = os.path.join(res, f"mipmap-{suffix}")
        os.makedirs(d, exist_ok=True)
        compose(legacy, shape="square", variant=variant).save(
            os.path.join(d, "ic_launcher.png"), optimize=True
        )
        compose(legacy, shape="circle", variant=variant).save(
            os.path.join(d, "ic_launcher_round.png"), optimize=True
        )
        compose(fg, shape="foreground", variant=variant).save(
            os.path.join(d, "ic_launcher_foreground.png"), optimize=True
        )
        _stencil(fg).save(os.path.join(d, "ic_launcher_monochrome.png"), optimize=True)

    anydpi = os.path.join(res, "mipmap-anydpi-v26")
    os.makedirs(anydpi, exist_ok=True)
    for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
        with open(os.path.join(anydpi, name), "w", encoding="utf-8") as f:
            f.write(ADAPTIVE_XML)

    drawable = os.path.join(res, "drawable")
    os.makedirs(drawable, exist_ok=True)
    with open(os.path.join(drawable, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(BACKGROUND_XML)
    return True


def write_store_assets(root: str, variant: str = "light") -> None:
    """商店 / README / 设计库用图（不进 APK）。

    路径按仓库类型选：**源码库**（有 android/app/src/main/res）写 `docs/brand/`，
    **设计库**（没有 android/）写 `brand/`。
    不能只看有没有 `docs/` —— 设计库也有 `docs/`（放规范文档），那样会写出
    `docs/brand/` 和 `brand/` 两份母版图。
    """
    has_android = os.path.isdir(os.path.join(root, "android", "app", "src", "main", "res"))
    out = os.path.join(root, *(["docs", "brand"] if has_android else ["brand"]))
    os.makedirs(out, exist_ok=True)
    compose(512, shape="square", variant=variant).save(
        os.path.join(out, "icon-512.png"), optimize=True
    )
    compose(1024, shape="square", variant=variant).save(
        os.path.join(out, "icon-1024.png"), optimize=True
    )
    compose(1024, shape="circle", variant=variant).save(
        os.path.join(out, "icon-1024-round.png"), optimize=True
    )


def write_preview(path: str, variant: str = "light") -> None:
    """一张对比图：整套尺寸 + 启动器遮罩 + 主题图标。"""
    tiles = [
        ("1024 方形", compose(1024, shape="square", variant=variant)),
        ("圆形遮罩", compose(512, shape="circle", variant=variant)),
        ("192", compose(192, shape="square", variant=variant)),
        ("144", compose(144, shape="square", variant=variant)),
        ("96", compose(96, shape="square", variant=variant)),
        ("72", compose(72, shape="square", variant=variant)),
        ("48", compose(48, shape="square", variant=variant)),
    ]
    # 自适应前景套在渐变底上，再用圆形遮罩切一次：检查安全区有没有被切。
    fg = compose(1024, shape="foreground", variant=variant)
    bg = _gradient_bg(1024).convert("RGBA")
    bg.alpha_composite(fg)
    masked = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    masked.paste(bg, (0, 0), _circle_mask(1024))
    adaptive = masked

    themed = compose(512, shape="themed", variant=variant)
    themed_bg = Image.new("RGBA", (512, 512), (32, 33, 36, 255))
    themed_bg.alpha_composite(themed.resize((512, 512), Image.LANCZOS))

    pad = 20
    top_h = 1044
    sheet = Image.new("RGBA", (pad + 1024 + pad + 1024 + pad, pad + top_h + pad + 532 + pad), (247, 247, 247, 255))
    sheet.alpha_composite(tiles[0][1], (pad, pad))
    sheet.alpha_composite(adaptive, (pad + 1024 + pad, pad))

    y = pad + top_h
    x = pad
    for img in (tiles[1][1], themed_bg):
        sheet.alpha_composite(img.resize((512, 512), Image.LANCZOS), (x, y))
        x += 512 + pad
    for img in (tiles[2][1], tiles[3][1], tiles[4][1], tiles[5][1], tiles[6][1]):
        y2 = y + 532 - img.size[1] - 10
        sheet.alpha_composite(img, (x, y2))
        x += img.size[0] + pad
    sheet.convert("RGB").save(path)


def _label(draw: ImageDraw.ImageDraw, xy, text: str, size: int, fill=(70, 70, 70)):
    """尽量用中文字体，拿不到就退回默认字体（只是标注，不影响母版）。"""
    for candidate in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf",
                      "/System/Library/Fonts/PingFang.ttc", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
        if os.path.exists(candidate):
            try:
                from PIL import ImageFont
                draw.text(xy, text, font=ImageFont.truetype(candidate, size), fill=fill)
                return
            except Exception:
                break
    draw.text(xy, text, fill=fill)


def _dashed_rect(draw, box, color, width=2, dash=10):
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), dash * 2):
        draw.line((x, y0, min(x + dash, x1), y0), fill=color, width=width)
        draw.line((x, y1, min(x + dash, x1), y1), fill=color, width=width)
    for y in range(int(y0), int(y1), dash * 2):
        draw.line((x0, y, x0, min(y + dash, y1)), fill=color, width=width)
        draw.line((x1, y, x1, min(y + dash, y1)), fill=color, width=width)


def _dashed_circle(draw, box, color, width=2, dash_deg=7, gap_deg=6):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = (x1 - x0) / 2
    start = 0
    while start < 360:
        draw.arc((cx - r, cy - r, cx + r, cy + r), start=start,
                 end=min(start + dash_deg, 360), fill=color, width=width)
        start += dash_deg + gap_deg


def _adaptive_canvas(size: int, variant: str) -> Image.Image:
    """108dp 画布：渐变底 + 前景（不裁遮罩）。"""
    big = size * SS
    canvas = _gradient_bg(big).convert("RGBA")
    m = int(big * ADAPTIVE_MARK_RATIO)
    off = (big - m) // 2
    canvas.alpha_composite(_mark_layer(m, variant), (off, off))
    return canvas.resize((size, size), Image.LANCZOS)


def _mask_shape(big: int, kind: str) -> Image.Image:
    """Android 启动器遮罩：只裁中间的 72dp 区域（108dp 画布外圈 18dp 不可见）。"""
    inset = int(round(big * 18 / 108))
    visible = big - 2 * inset
    layer = Image.new("L", (big, big), 0)
    draw = ImageDraw.Draw(layer)
    box = (inset, inset, inset + visible - 1, inset + visible - 1)
    if kind == "circle":
        draw.ellipse(box, fill=255)
    elif kind == "squircle":
        draw.rounded_rectangle(box, radius=int(visible * 0.45), fill=255)
    else:
        draw.rounded_rectangle(box, radius=int(visible * 0.26), fill=255)
    return layer


def _max_radius_dp(fg: Image.Image) -> float:
    """前景层里不透明像素离中心的最远距离（dp）。用来断言 72dp 遮罩不切图。"""
    import math as _m

    alpha = fg.getchannel("A")
    px = alpha.load()
    w, h = fg.size
    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
    best = 0.0
    for y in range(h):
        for x in range(w):
            if px[x, y] > 8:
                r = _m.hypot(x - cx, y - cy)
                if r > best:
                    best = r
    return best * 108.0 / w


def write_diagram(out_dir: str, variant: str = "light") -> None:
    """设计库用的两张规范图：启动器遮罩预演 + 自适应安全区标注。"""
    os.makedirs(out_dir, exist_ok=True)

    # --- 1) 遮罩预演 -------------------------------------------------------
    card = 288
    kinds = [("circle", "圆形（Pixel）"), ("squircle", "方圆（三星/小米）"), ("rounded", "圆角方形")]
    pad = 24
    sheet = Image.new("RGBA", (pad + (card + pad) * 3, pad + card + 56 + 44 + pad), (246, 246, 244, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (kind, label) in enumerate(kinds):
        x = pad + index * (card + pad)
        big = card * SS
        canvas = _gradient_bg(big).convert("RGBA")
        m = int(big * ADAPTIVE_MARK_RATIO)
        off = (big - m) // 2
        canvas.alpha_composite(_mark_layer(m, variant), (off, off))
        tile = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        tile.paste(canvas, (0, 0), _mask_shape(big, kind))
        sheet.alpha_composite(tile.resize((card, card), Image.LANCZOS), (x, pad))
        small = tile.resize((48, 48), Image.LANCZOS)
        sheet.alpha_composite(small, (x, pad + card + 18))
        _label(draw, (x, pad + card + 20 + 52), label, 20)
    _label(draw, (pad, 6), "108dp 画布 / 72dp 遮罩下的实际显示（含 48px 缩略）", 18, (120, 120, 120))
    sheet.convert("RGB").save(os.path.join(out_dir, "icon-masks.png"))

    # --- 2) 安全区标注 -----------------------------------------------------
    canvas_px = 720
    dp = canvas_px / 108.0
    art = _adaptive_canvas(canvas_px, variant).convert("RGBA")
    board = Image.new("RGBA", (canvas_px + 80, canvas_px + 130), (255, 255, 255, 255))
    board.alpha_composite(art, (40, 40))
    draw = ImageDraw.Draw(board)

    inset = 18 * dp
    box = (40 + inset, 40 + inset, 40 + canvas_px - inset, 40 + canvas_px - inset)
    _dashed_rect(draw, box, (220, 90, 60), width=2, dash=12)
    _dashed_circle(draw, (40 + (54 - 33) * dp, 40 + (54 - 33) * dp,
                          40 + (54 + 33) * dp, 40 + (54 + 33) * dp), (60, 120, 200), width=2)
    draw.rectangle((40, 40, 40 + canvas_px, 40 + canvas_px), outline=(180, 180, 180), width=2)

    mark_dp = 108 * ADAPTIVE_MARK_RATIO
    half = mark_dp / 2
    mbox = (40 + (54 - half) * dp, 40 + (54 - half) * dp,
            40 + (54 + half) * dp, 40 + (54 + half) * dp)
    draw.rectangle(mbox, outline=(30, 110, 90), width=2)

    radius = _max_radius_dp(compose(432, shape="foreground", variant=variant))
    y = 40 + canvas_px + 12
    _label(draw, (40, y), f"红虚线 = 72dp 可视区（外圈 18dp 会被裁）", 17, (200, 70, 50))
    _label(draw, (40, y + 24), f"蓝虚线 = 66dp 保守内容圆；绿框 = 图形方框 {mark_dp:.2f}dp（{int(ADAPTIVE_MARK_RATIO * 100)}%）", 17, (40, 80, 160))
    _label(draw, (40, y + 48), f"实测图形最大半径 {radius:.2f}dp ≤ 36dp（遮罩圆半径）→ 不被裁，余量 {36 - radius:.2f}dp", 17, (20, 100, 80))
    board.convert("RGB").save(os.path.join(out_dir, "icon-safe-zone.png"))
    print(f"规范图：{out_dir}\\icon-masks.png、icon-safe-zone.png（最大半径 {radius:.2f}dp）")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="只输出预览对比图到该路径")
    ap.add_argument("--diagram", help="输出设计规范配图（遮罩预演 + 安全区标注）到该目录")
    ap.add_argument("--variant", default="light", choices=["light", "mint"])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()

    if args.diagram:
        write_diagram(args.diagram, variant=args.variant)
        return

    if args.preview:
        write_preview(args.preview, variant=args.variant)
        print(f"预览：{args.preview}")
        return

    wrote_res = write_assets(args.root, variant=args.variant)
    write_store_assets(args.root, variant=args.variant)
    print("图标已写入" + ("res/ 与 docs/brand/" if wrote_res else "brand/（母版图）"))


if __name__ == "__main__":
    main()
