# design_audit.py — 出稿前必跑的设计量化检查
# 用法: python design_audit.py <css文件或html文件...>
# 退出码 0 = 全过；1 = 有 FAIL
import io
import os
import re
import sys

M3_RADII = {0, 4, 8, 12, 16, 28}
PILL = 999


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexstr):
    h = hexstr.lstrip('#')
    if len(h) == 8:
        h = h[2:]  # 忽略 alpha
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def contrast(fg, bg):
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def parse_vars(text):
    """从 CSS 或 JS 对象里抓 --name:'#RRGGBB' 形式的变量"""
    out = {}
    for m in re.finditer(r"""(?:--([a-z0-9-]+)|'--([a-z0-9-]+)')\s*:\s*['"]?(#[0-9A-Fa-f]{6,8})""", text):
        name = m.group(1) or m.group(2)
        out[name] = m.group(3).upper()
    return out


fail = []
warn = []
ok = []


def check(label, cond, detail=''):
    (ok if cond else fail).append('%s %s' % (label, detail))


def run(path):
    src = io.open(path, encoding='utf-8', errors='replace').read()
    v = parse_vars(src)
    # .css 文件里没有 token 定义是正常的，不能因此跳过硬编码扫描
    if not v and not path.endswith('.css'):
        return
    name = os.path.basename(path)

    # 1) 对比度（WCAG AA：正文 4.5，大字号/图形 3.0）
    pairs = [
        ('on-s', 'surface', 4.5, '正文'),
        ('on-v', 'surface', 4.5, '次要文字'),
        ('on-p-c', 'p-c', 4.5, '主色块上的文字'),
        ('ai-fg', 'ai-bg', 4.5, 'AI 气泡文字'),
        ('on-err-bg', 'err-bg', 4.5, '错误条文字'),
        ('send-fg', 'send-bg', 3.0, '发送键图标'),
        ('av-fg', 'av-bg', 3.0, '头像图标'),
    ]
    for fg, bg, need, label in pairs:
        if fg in v and bg in v:
            ratio = contrast(v[fg], v[bg])
            tag = '[%s] %s on %s = %.2f (需 %.1f)' % (name, label, label, ratio, need)
            check(tag, ratio >= need, '' if ratio >= need else '  ← 偏低')

    # 2) 圆角是否在 M3 尺度上
    for m in re.finditer(r"--r-([a-z]+)\s*:\s*'?(\d+)px", src):
        key, px = m.group(1), int(m.group(2))
        if px in M3_RADII or px == PILL:
            continue
        warn.append('[%s] --r-%s = %dpx 不在 M3 尺度 %s 上' % (name, key, px, sorted(M3_RADII)))

    # 3) 字号阶梯（相邻档至少差 2，且不出现 11 以下）
    sizes = sorted({int(x) for x in re.findall(r"--fs-[a-z]+\s*:\s*'?(\d+)px", src)})
    for i in range(len(sizes) - 1):
        if sizes[i + 1] - sizes[i] < 2:
            warn.append('[%s] 字号 %d 和 %d 过于接近，层级分不开' % (name, sizes[i], sizes[i + 1]))
    for s in sizes:
        if s < 12:
            warn.append('[%s] 字号 %dpx 偏小，中文会有笔画粘连' % (name, s))

    # 4) 行高
    for m in re.finditer(r"--lh\s*:\s*'?([\d.]+)", src):
        lh = float(m.group(1))
        check('[%s] 行高 %.2f ≥ 1.5' % (name, lh), lh >= 1.5,
              '' if lh >= 1.5 else '  ← 正文会挤')

    # 5) 零阴影
    shadows = len(re.findall(r'box-shadow\s*:\s*(?!none)', src)) + len(re.findall(r"elevation\s*:\s*(?!0)", src))
    check('[%s] 零阴影' % name, shadows == 0, '' if shadows == 0 else '  ← %d 处' % shadows)

    # 6) CSS 里绕过 token 的硬编码颜色（audit:chrome-start/end 之间豁免）
    if path.endswith('.css'):
        in_chrome = False
        for i, line in enumerate(src.splitlines(), 1):
            if 'audit:chrome-start' in line:
                in_chrome = True
                continue
            if 'audit:chrome-end' in line:
                in_chrome = False
                continue
            if in_chrome:
                continue
            if re.match(r'\s*--', line) or 'currentColor' in line or line.strip().startswith('/*'):
                continue
            for h in re.findall(r'#[0-9A-Fa-f]{6}\b', line):
                fail.append('[%s:%d] 硬编码颜色 %s，应该走 token' % (name, i, h))

    # 6b) 硬编码颜色 vs token（同一文件内）
    hexes = re.findall(r'#[0-9A-Fa-f]{6}\b', src)
    if len(hexes) > 0 and len(v) > 0:
        pass  # 变量定义本身就有颜色，不做硬编码判定

    # 7) 间距是否 4 的倍数
    for m in re.finditer(r"--gap\s*:\s*'?(\d+)px", src):
        g = int(m.group(1))
        if g % 4 != 0:
            warn.append('[%s] --gap = %dpx 不是 4 的倍数' % (name, g))


for p in sys.argv[1:]:
    run(p)

print('=' * 62)
for line in ok:
    print('  PASS', line)
for line in warn:
    print('  WARN', line)
for line in fail:
    print('  FAIL', line)
print('=' * 62)
print('通过 %d · 警告 %d · 失败 %d' % (len(ok), len(warn), len(fail)))
sys.exit(1 if fail else 0)
