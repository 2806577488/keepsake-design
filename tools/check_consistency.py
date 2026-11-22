#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keepsake 设计一致性校验
========================

用途：确认「设计稿 HTML」和「落地代码里的 token」是同一个值。

起因：v3 第一次交付时，skin_tokens.dart 里 E 的 fsTitle 还是 16，
      但改动说明写的是 15。原因是我改了 HTML 里的值，却没有重新跑生成器。
      这种「改了源头，忘了同步下游」的错，肉眼很难发现，所以做成脚本。

用法
----
    # 默认：读同目录的 reference/full-list.html 和 skin_tokens.dart
    python check_consistency.py

    # 指定路径（工程师在自己仓库里跑）
    python check_consistency.py --ref reference/full-list.html --dart lib/core/skins.dart

    # 同时校验 SPEC.md 的形态表
    python check_consistency.py --spec SPEC.md

退出码
------
    0  全部一致
    1  有不一致，或文件读不到

依赖：Python 3.8+，无第三方库。
"""

import argparse
import io
import os
import re
import sys

# ── 要校验的项：HTML token 名 -> dart 字段名 ──────────────
CHECKS = [
    ('fs-bar',   'fsBar',   '顶栏字号'),
    ('fs-title', 'fsTitle', '列表标题字号'),
    ('fs-body',  'fsBody',  '正文字号'),
    ('fs-sub',   'fsSub',   '元信息字号'),
    ('r-bubble', 'rBubble', '气泡圆角'),
    ('r-card',   'rCard',   '卡片圆角'),
    ('r-chip',   'rChip',   'chip 圆角'),
    ('r-field',  'rField',  '输入框圆角'),
    ('row-h',    'rowHeight', '列表行高'),
]


def read(path):
    if not os.path.exists(path):
        print('ERROR: 读不到文件 %s' % path)
        sys.exit(1)
    return io.open(path, encoding='utf-8').read()


def extract_html(html):
    """从设计稿 HTML 里提取 base / E / H 三套 token"""
    def grab(block):
        return dict(re.findall(r"'--([a-z0-9-]+)'\s*:\s*'([^']*)'", block))

    m = re.search(r'const base = \{([\s\S]*?)\n\};', html)
    if not m:
        print('ERROR: 设计稿里找不到 const base = {...}')
        sys.exit(1)
    base = grab(m.group(1))

    m = re.search(r"icons:'outlined', size:24, v:\{([\s\S]*?)\n  \}\}", html)
    ev = grab(m.group(1)) if m else {}

    i = html.find("h: { name:'H 墨色")
    hv = {}
    if i >= 0:
        seg = html[i:i + 1200]
        j = seg.find('v:{')
        k = seg.find('}}', j)
        hv = grab(seg[j:k])

    return {'A': dict(base), 'E': {**base, **ev}, 'H': {**base, **hv}}


def extract_dart(dart):
    """从 skin_tokens.dart 里提取三套 SkinMorph 的数值字段"""
    out = {}

    # 每套皮肤是一个 `static const SkinMorph x = SkinMorph(...)` 块
    blocks = re.findall(
        r'static const SkinMorph (\w+)\s*=\s*SkinMorph\(([\s\S]*?)\n  \);',
        dart)

    names = {'a': 'A', 'e': 'E', 'h': 'H'}
    for var, body in blocks:
        key = names.get(var.lower(), var.upper())
        d = {}
        # 单行字段： fsBar: 20, fsTitle: 16, ...
        for fm in re.finditer(r'(\w+):\s*(-?[\d.]+)', body):
            d[fm.group(1)] = fm.group(2)
        out[key] = d
    return out


def num(v):
    """把 '15px' / '15' / 15.0 都转成可比较的 float"""
    if v is None:
        return None
    s = str(v).strip().lower().replace('px', '').replace('em', '')
    try:
        return float(s)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description='Keepsake 设计一致性校验')
    ap.add_argument('--ref', default='reference/full-list.html',
                    help='设计稿 HTML 路径')
    ap.add_argument('--dart', default='skin_tokens.dart',
                    help='skin_tokens.dart 路径')
    ap.add_argument('--spec', default=None,
                    help='可选：SPEC.md 路径，一并校验形态表')
    args = ap.parse_args()

    html = read(args.ref)
    dart = read(args.dart)

    ht = extract_html(html)
    dt = extract_dart(dart)

    if not dt:
        print('ERROR: %s 里找不到 static const SkinMorph 常量' % args.dart)
        sys.exit(1)

    print('设计稿: %s' % args.ref)
    print('代码:   %s' % args.dart)
    print('=' * 72)
    print('%-8s %-12s %8s %8s %8s' % ('套', '项', '设计稿', '代码', '结果'))
    print('-' * 72)

    fails = 0
    for skin in ['A', 'E', 'H']:
        if skin not in dt:
            print('WARN: 代码里没有 %s 套' % skin)
            continue
        for hkey, dkey, label in CHECKS:
            hv = num(ht[skin].get(hkey))
            dv = num(dt[skin].get(dkey))
            if hv is None:
                continue
            if dv is None:
                print('%-8s %-12s %8s %8s  MISS'
                      % (skin, label, hv, '—'))
                fails += 1
                continue
            same = abs(hv - dv) < 0.01
            print('%-8s %-12s %8s %8s  %s'
                  % (skin, label, hv, dv, 'ok' if same else 'FAIL'))
            if not same:
                fails += 1

    # ── 可选：SPEC.md 形态表 ─────────────────────
    if args.spec:
        spec = read(args.spec)
        print('-' * 72)
        print('SPEC 形态表交叉检查:')
        m = re.search(
            r'\| 列表标题 \(`--fs-title`\) \| ([\d.]+)px \| \**([\d.]+)px\** \| ([\d.]+)px \|',
            spec)
        if m:
            spec_vals = [float(m.group(1)), float(m.group(2)), float(m.group(3))]
            html_vals = [num(ht[s].get('fs-title')) for s in ['A', 'E', 'H']]
            if spec_vals == html_vals:
                print('  SPEC fs-title 与设计稿一致: %s' % html_vals)
            else:
                print('  FAIL SPEC fs-title: SPEC=%s 设计稿=%s'
                      % (spec_vals, html_vals))
                fails += 1
        else:
            print('  WARN: SPEC 里没解析到 fs-title 行')

        m = re.search(
            r'\| 列表行高 \(`--row-h`\) \| ([\d.]+)px \| ([\d.]+)px \| ([\d.]+)px \|',
            spec)
        if m:
            spec_vals = [float(m.group(1)), float(m.group(2)), float(m.group(3))]
            html_vals = [num(ht[s].get('row-h')) for s in ['A', 'E', 'H']]
            if spec_vals == html_vals:
                print('  SPEC row-h 与设计稿一致: %s' % html_vals)
            else:
                print('  FAIL SPEC row-h: SPEC=%s 设计稿=%s'
                      % (spec_vals, html_vals))
                fails += 1

    print('=' * 72)
    if fails:
        print('结果: %d 项不一致' % fails)
        sys.exit(1)
    else:
        print('结果: 全部一致')


if __name__ == '__main__':
    main()
