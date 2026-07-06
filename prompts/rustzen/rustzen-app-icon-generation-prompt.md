# Rustzen App Icon Generation Prompt

Use this prompt when generating or regenerating Rustzen desktop client app icons that should stay visually aligned with the approved `rustzen-clear` icon direction.

## Reference Audit

Primary visual reference:

- `rustzen-clear/zen-gui/src-tauri/icons/icon-1024.png`
- PNG, `1024 x 1024`, RGBA, 4 channels, real alpha
- measured alpha bounds:
  - weak shadow, `alpha >= 1`: `x=79 y=101 w=861 h=862`
  - visible shape, `alpha >= 5`: `x=99 y=101 w=827 h=858`
  - solid body, `alpha >= 250`: `x=105 y=105 w=815 h=812`

Current related project icons reviewed:

- `rustzen-zipper/apps/macos/assets/brand/app-icon.svg`
  - already uses the shared white-blue rounded card system
  - still reads too much like a standalone zipper utility because the puller and zipper teeth are visually dominant
  - should move closer to a soft embossed Rustzen family icon: abstract `Z`, restrained seam, fewer rounded teeth, weak or absent puller, right-top bubbles
- `rustzen-clipboard/zen-gui/assets/brand/app-icon.svg`
  - already uses the shared white-blue rounded card system
  - clipboard object is acceptable but should be slightly quieter and smaller
  - current 1024 raster has a larger full alpha footprint than `rustzen-clear`; keep the main card closer to the clear reference
  - should add the right-top bubbles used as a shared Rustzen client recognition element

## Unified Icon Standard

```text
Canvas: 1024 x 1024
Format: PNG / RGBA / 4 channels / Alpha
Background: real transparent background
No checkerboard, no simulated transparency, no white or gray canvas fill

Main card: close to the rustzen-clear rounded card footprint
Card geometry target: about x=104 y=104 w=816 h=816
Solid body target: close to x=105 y=105 w=815 h=812
Weak bottom shadow: allowed to extend below the card, roughly toward y=960
Corner radius: large macOS-style rounded rectangle, close to rx=168

Style: white-blue soft emboss with light glass
Not full transparent glass
Not multi-layer glossy UI chrome
Not metallic
Not deep saturated blue

Theme colors: white, ice blue, pale blue, low-saturation sky blue
Shared mark: 2 to 3 small right-top bubbles
Lighting: soft top-left highlight, restrained bottom shadow
```

## Fixed Base Prompt

```text
生成单个 1024×1024 Rustzen App Icon。

参考 rustzen-clear 的图标风格：白蓝软浮雕、轻玻璃、低饱和、圆角大卡片、右上角 2 到 3 个小气泡。

画布必须是真实透明 PNG，RGBA / 4 通道 / Alpha。
只有图标物体、气泡和弱阴影可以有像素；主卡片外侧必须是 alpha=0 的透明区域。
不要棋盘格背景，不要模拟透明，不要白底，不要灰色背景，不要整张浅色方形底。

主卡片接近占满画布，边界和 rustzen-clear 一致：
主卡片约为 x=104 y=104 w=816 h=816，圆角接近 rx=168。
弱阴影可以向下轻微扩展到 y=960 左右，但不要形成厚重投影。
不要让主卡片扩大到 x<90、y<90、w>845 或 h>845。

整体材质为冰蓝与白色渐变，低对比、柔和、干净。
图标主体居中，留出足够白蓝呼吸空间。
主体符号应明显小于主卡片，最大宽高控制在主卡片的 55% 到 68%。
右上角气泡必须在主卡片内部，不要贴边，不要漂到卡片外。
不要强烈深蓝，不要金属质感，不要过度玻璃化，不要多层透明边框，不要强光泽 UI。
```

## Clear Variant Prompt

```text
基于固定 Rustzen App Icon 提示词生成 rustzen-clear 图标。

主体是一个抽象清理 / 清空符号，接近 rustzen-clear 已批准方向：
居中的软浮雕圆环、旋涡或留白开口形，不要做扫帚、喷壶、垃圾桶、盾牌、云朵或浏览器图标。

主体使用白色、冰蓝、浅蓝软浮雕材质。
圆环或旋涡应安静、厚度均匀、边缘柔和，避免过强的内部阴影。
右上角保留 2 到 3 个小气泡。
整体应该像 Rustzen 客户端家族基础图标，而不是具体工具软件图标。
```

## Zipper Variant Prompt

```text
基于固定 Rustzen App Icon 提示词生成 rustzen-zipper 图标。

主体是一个抽象压缩 / 解压符号，可以有 Z 形动势，但不要做字体字母 Z，也不要做真实五金拉链。
Z 字使用冰蓝与白色软浮雕材质，和 rustzen-clear 的圆环属于同一系列。

中间保留一条轻微“解压缝隙”，但不要画成复杂机械结构。
只使用 5 到 8 个小型圆角齿块，齿块要轻、软、低对比。
拉头弱化或取消；如果保留，只能是非常轻的几何暗示，不能成为视觉中心。
主体整体宽高控制在主卡片的 60% 到 68%，不要横向撑满卡片。

右上角保留 2 到 3 个小气泡。
整体应该像 rustzen-clear 同系列客户端图标，而不是单独的压缩软件图标。
```

## Clipboard Variant Prompt

```text
基于固定 Rustzen App Icon 提示词生成 rustzen-clipboard 图标。

可以保留剪贴板主体，但内部剪贴板不要过大，主体应该比当前版本更轻、更安静。
主卡片尺寸和边界贴近 rustzen-clear，不要让透明外扩或阴影范围显得过满。
剪贴板使用白色、冰蓝、浅蓝软浮雕材质，蓝色不要太重。
剪贴板主体宽度控制在主卡片的 36% 到 46%，高度控制在主卡片的 42% 到 54%。
夹子只能是轻微顶部暗示，不要金属夹，不要深色描边，不要文字、勾选项或文档内容。

右上角保留 2 到 3 个小气泡，作为 Rustzen 客户端统一识别元素。
底部轻阴影保留，但背景必须是真实透明。
```

## Negative Prompt

```text
不要棋盘格背景。
不要白底。
不要灰色背景。
不要模拟透明。
不要强烈深蓝。
不要高饱和蓝紫渐变。
不要金属拉链。
不要写实五金。
不要复杂机械结构。
不要厚重投影。
不要过度玻璃化。
不要多层透明边框。
不要强光泽 UI。
不要让主体顶到边缘。
不要缺少 Alpha 通道。
不要整张浅色方形底。
不要让主卡片外侧有任何非透明背景像素。
不要做字体字母 Z。
不要使用深色描边。
不要在剪贴板里添加文字、列表或勾选符号。
```
