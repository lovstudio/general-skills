# lovstudio-business-card

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

Generate a professional, editorial-style business card (2:1) — high-resolution PNG
plus a self-contained interactive HTML with click-to-download.

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) — by [lovstudio.ai](https://lovstudio.ai)

## What it makes

An editorial / luxury-minimal name card: Swiss typographic grid, hairline dividers,
a single accent color, Songti × Didot type pairing, masthead + footer bands, and a
faint watermark glyph. Three themes: `dark-terracotta`, `midnight`, `ivory`.
No avatar? It falls back to a serif monogram of the name.

```
┌──────────────────────────────────────────────────────────┐
│ BRAND.AI                              STUDIO — Nº 2026     │
│ ────────────────────────────────────────────────────────  │
│ ┌────────┐    手工川  Mark Shawn                           │
│ │ avatar │    背包客 ◆ 超级开发者 ◆ AI / OPC 布道师        │
│ │   or   │                                                 │
│ │ 林 mono│    在 Agent 时代，                              │
│ └────────┘    寻找人的意义                                 │
│ ────────────────────────────────────────────────────────  │
│ 旅行 · 羽毛球 · 哲学            ◈ 上海 …   ◈ 北京 …          │
└──────────────────────────────────────────────────────────┘
```

## Install

```bash
git clone https://github.com/lovstudio/business-card-skill "${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-business-card"
```

Requires: Python 3.8+ and Google Chrome / Chromium (for PNG rendering). On macOS,
cropping uses the built-in `sips`; elsewhere `pip install pillow`. Without a
browser the PNG step is skipped — open the HTML and use its download button.

## Usage

```bash
SKILL_DIR="${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-business-card"
python3 "$SKILL_DIR/scripts/render_card.py" \
  --name "手工川" --latin "Mark Shawn" \
  --brand "LOVSTUDIO.AI" --index "STUDIO — Nº 2026" \
  --tags "背包客,超级开发者,AI / OPC 布道师" \
  --tagline "在 **Agent 时代**，|寻找**人**的意义" \
  --pursuits "旅行,羽毛球,计算机科学,心理学,哲学" \
  --bases "上海 陆家嘴数智港,北京 搜狐大厦清智孵化器" \
  --avatar ./me.png --theme dark-terracotta \
  --out ./output --format both
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--name` | (required) | Display name (CJK ok) |
| `--latin` | `""` | Secondary / romanized name (italic) |
| `--brand` | `""` | Top-left brand; a `.` is accent-colored |
| `--index` | `""` | Top-right line, e.g. `STUDIO — Nº 2026` |
| `--tags` | `""` | Comma-separated role tags |
| `--tagline` | `""` | Hero line; `**word**` = accent, `\|` = line break |
| `--pursuits` | `""` | Comma-separated interests (footer left) |
| `--bases` | `""` | Comma-separated locations (footer right) |
| `--avatar` | `""` | Portrait image path; omit → monogram |
| `--caption` | `""` | Portrait caption (optional) |
| `--watermark` | last char of name | Giant background glyph |
| `--theme` | `dark-terracotta` | `dark-terracotta` \| `midnight` \| `ivory` |
| `--out` | `./output` | Output directory |
| `--format` | `both` | `png` \| `html` \| `both` |
| `--scale` | `3` | PNG scale factor (3 → 4800×2400) |

## Output

- `{name}-名片.png` — high-res card (default 4800×2400)
- `{name}-名片.html` + `modern-screenshot.umd.js` — open in a browser, click 下载 for a 3× PNG

## Adding a theme

Add a CSS-variable set to the `THEMES` dict in `scripts/render_card.py` — no template
edits needed.

## License

MIT
