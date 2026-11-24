// Keepsake 皮肤 Token · 自动生成于设计稿（full-list.html），勿手改数值
// 三套皮肤共用一份 UI 代码，切皮肤只换这里的常量。

import 'package:flutter/material.dart';

enum Skin { a, e, h }
enum IconMood { filled, outlined }

@immutable
class SkinColors {
  final Color surface;
  final Color low;
  final Color high;
  final Color highest;
  final Color usage;
  final Color ov;
  final Color outline;
  final Color onS;
  final Color onV;
  final Color codeBg;
  final Color codeHead;
  final Color codeDiv;
  final Color codeFg;
  final Color pC;
  final Color onPC;
  final Color sendBg;
  final Color sendFg;
  final Color aiBg;
  final Color aiFg;
  final Color avBg;
  final Color avFg;
  final Color errC;
  final Color errBg;
  final Color onErrBg;
  final Color iconC;
  final Color selBg;
  final Color selBar;
  final Color fabLine;

  const SkinColors({
    required this.surface,
    required this.low,
    required this.high,
    required this.highest,
    required this.usage,
    required this.ov,
    required this.outline,
    required this.onS,
    required this.onV,
    required this.codeBg,
    required this.codeHead,
    required this.codeDiv,
    required this.codeFg,
    required this.pC,
    required this.onPC,
    required this.sendBg,
    required this.sendFg,
    required this.aiBg,
    required this.aiFg,
    required this.avBg,
    required this.avFg,
    required this.errC,
    required this.errBg,
    required this.onErrBg,
    required this.iconC,
    required this.selBg,
    required this.selBar,
    required this.fabLine,
  });

  /// A 清透
  static const SkinColors a = SkinColors(
    surface: Color(0xFFF5FBF7),
    low: Color(0xFFEFF5F2),
    high: Color(0xFFE3EAE6),
    highest: Color(0xFFDEE4E1),
    usage: Color(0xFFE9EFEC),
    ov: Color(0xFFCAD1CD),
    outline: Color(0xFF7C8B86),
    onS: Color(0xFF191C1B),
    onV: Color(0xFF496F66),
    codeBg: Color(0xFFFFFFFF),
    codeHead: Color(0xFFE7F3EF),
    codeDiv: Color(0xFFD5EAE3),
    codeFg: Color(0xFF161B1A),
    pC: Color(0xFFA0F2DF),
    onPC: Color(0xFF005045),
    sendBg: Color(0xFFA0F2DF),
    sendFg: Color(0xFF005045),
    aiBg: Color(0xFFA0F2DF),
    aiFg: Color(0xFF005045),
    avBg: Color(0xFFDEE4E1),
    avFg: Color(0xFF496F66),
    errC: Color(0xFFBA1A1A),
    errBg: Color(0xFFFFDAD6),
    onErrBg: Color(0xFF410002),
    iconC: Color(0xFF191C1B),
    selBg: Color(0xFFD9F6EC),
    selBar: Color(0xFF046B5C),
    fabLine: Color(0xFF8CCDBB),
  );

  /// E 纸感
  static const SkinColors e = SkinColors(
    surface: Color(0xFFFDFCF9),
    low: Color(0xFFF1EDE4),
    high: Color(0xFFE8E2D6),
    highest: Color(0xFFDEE4E1),
    usage: Color(0xFFE9EFEC),
    ov: Color(0xFFD8D4CC),
    outline: Color(0xFF7C8B86),
    onS: Color(0xFF1A1A18),
    onV: Color(0xFF5C5A54),
    codeBg: Color(0xFFFFFFFF),
    codeHead: Color(0xFFE7F3EF),
    codeDiv: Color(0xFFD5EAE3),
    codeFg: Color(0xFF161B1A),
    pC: Color(0xFFF2D9C4),
    onPC: Color(0xFF5A2E14),
    sendBg: Color(0xFFB4481B),
    sendFg: Color(0xFFFFFFFF),
    aiBg: Color(0xFFA0F2DF),
    aiFg: Color(0xFF005045),
    avBg: Color(0xFFDEE4E1),
    avFg: Color(0xFF496F66),
    errC: Color(0xFFBA1A1A),
    errBg: Color(0xFFFFDAD6),
    onErrBg: Color(0xFF410002),
    iconC: Color(0xFF191C1B),
    selBg: Color(0xFFF0E4D6),
    selBar: Color(0xFFB4481B),
    fabLine: Color(0xFF8CCDBB),
  );

  /// H 墨色
  static const SkinColors h = SkinColors(
    surface: Color(0xFFF5FBF7),
    low: Color(0xFFEFF5F2),
    high: Color(0xFFE3EAE6),
    highest: Color(0xFFDEE4E1),
    usage: Color(0xFFE9EFEC),
    ov: Color(0xFFCAD1CD),
    outline: Color(0xFF7C8B86),
    onS: Color(0xFF191C1B),
    onV: Color(0xFF496F66),
    codeBg: Color(0xFFFFFFFF),
    codeHead: Color(0xFFE7F3EF),
    codeDiv: Color(0xFFD5EAE3),
    codeFg: Color(0xFF161B1A),
    pC: Color(0xFFA0F2DF),
    onPC: Color(0xFF005045),
    sendBg: Color(0xFF1F4A42),
    sendFg: Color(0xFFA7E6D5),
    aiBg: Color(0xFF1F4A42),
    aiFg: Color(0xFFA7E6D5),
    avBg: Color(0xFF1F4A42),
    avFg: Color(0xFFA7E6D5),
    errC: Color(0xFFBA1A1A),
    errBg: Color(0xFFFFDAD6),
    onErrBg: Color(0xFF410002),
    iconC: Color(0xFF1F4A42),
    selBg: Color(0xFFD9F6EC),
    selBar: Color(0xFF046B5C),
    fabLine: Color(0xFF8CCDBB),
  );

}

@immutable
class SkinMorph {
  final double rBubble;
  final double rFab;
  final double rCard;
  final double rSheet;
  final double rChip;
  final double rField;
  final double rSend;
  final double rCb;
  final double rRadio;
  final double fsBar, fsTitle, fsBody, fsSub;
  final double lineHeight;
  final double rowHeight, gap, avatarSize, avatarRadius;
  final double cardBorderWidth;
  final FontWeight titleWeight;
  final bool monoForMeta;
  final double iconSize;
  final IconMood iconMood;

  const SkinMorph({
    required this.rBubble,
    required this.rFab,
    required this.rCard,
    required this.rSheet,
    required this.rChip,
    required this.rField,
    required this.rSend,
    required this.rCb,
    required this.rRadio,
    required this.fsBar, required this.fsTitle, required this.fsBody, required this.fsSub,
    required this.lineHeight, required this.rowHeight, required this.gap,
    required this.avatarSize, required this.avatarRadius, required this.cardBorderWidth,
    required this.titleWeight, required this.monoForMeta,
    required this.iconSize, required this.iconMood,
  });

  static const SkinMorph a = SkinMorph(
    rBubble: 16, rFab: 16, rCard: 14, rSheet: 24,
    rChip: 999, rField: 999, rSend: 999, rCb: 6, rRadio: 999,
    fsBar: 20, fsTitle: 16, fsBody: 15, fsSub: 13,
    lineHeight: 1.6, rowHeight: 68, gap: 12,
    avatarSize: 17, avatarRadius: 17, cardBorderWidth: 0,
    titleWeight: FontWeight.w400, monoForMeta: false,
    iconSize: 24, iconMood: IconMood.filled,
  );

  static const SkinMorph e = SkinMorph(
    rBubble: 8, rFab: 6, rCard: 6, rSheet: 14,
    rChip: 3, rField: 6, rSend: 6, rCb: 3, rRadio: 3,
    fsBar: 20, fsTitle: 15, fsBody: 16, fsSub: 12.5,
    lineHeight: 1.7, rowHeight: 68, gap: 10,
    avatarSize: 6, avatarRadius: 6, cardBorderWidth: 1,
    titleWeight: FontWeight.w700, monoForMeta: false,
    iconSize: 24, iconMood: IconMood.outlined,
  );

  static const SkinMorph h = SkinMorph(
    rBubble: 14, rFab: 14, rCard: 12, rSheet: 24,
    rChip: 8, rField: 12, rSend: 12, rCb: 5, rRadio: 6,
    fsBar: 22, fsTitle: 16, fsBody: 16, fsSub: 13,
    lineHeight: 1.55, rowHeight: 68, gap: 12,
    avatarSize: 17, avatarRadius: 17, cardBorderWidth: 0,
    titleWeight: FontWeight.w700, monoForMeta: false,
    iconSize: 26, iconMood: IconMood.filled,
  );

}