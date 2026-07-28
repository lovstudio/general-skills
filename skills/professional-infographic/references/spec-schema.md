# Project and HTML contract

## Project structure

```text
<project>/
├── source.md
├── brief.md
├── poster.html
├── project.json
├── poster.png
├── audit.json
└── assets/
```

The `scaffold` command creates the first four entries and the asset directory.
Generated files must use UTF-8.

## `brief.md`

Required headings:

```markdown
# Infographic brief

## Audience and decision
## Governing message
## Supporting claims
## Evidence ledger
## Assumptions and gaps
## Visual job
## Deliberate omissions
```

An evidence-ledger item should include:

```markdown
- Claim:
  - Exact source:
  - Location:
  - Type: fact | estimate | assumption | interpretation
  - Unit / period:
  - Caveat:
```

## `project.json`

```json
{
  "schema_version": 1,
  "title": "Working title",
  "aspect": "4:5",
  "canvas": {"width": 1080, "height": 1350},
  "brand_profile": "/resolved/path/brand.json",
  "source": "source.md",
  "brief": "brief.md",
  "poster": "poster.html"
}
```

## Brand profile

```json
{
  "schema_version": 1,
  "name": "LovStudio",
  "site": "https://lovstudio.ai",
  "logo": "/absolute/or/profile-relative/logo.svg",
  "primary": "#1F2937",
  "accent": "#D97757",
  "ink": "#111827",
  "muted": "#64748B",
  "paper": "#F7F4EF",
  "font_family": "Inter, PingFang SC, Microsoft YaHei, sans-serif",
  "copyright": "本信息图由 LovStudio 的「专业信息图」Skill 生成",
  "output_dir": "$HOME/Documents/professional-infographic"
}
```

Logo paths are resolved relative to the profile file, then embedded into the
scaffolded HTML as a data URL. Generated projects do not depend on the original
logo path.

## Auditable HTML

Keep these selectors and attributes:

- `.poster` — fixed canvas and screenshot target;
- `.poster__title[data-audit="title"]` — governing message;
- `[data-region="visual"]` — main visual area;
- `[data-primary-block]` — each main block;
- `[data-audit="label"]` — module labels;
- `[data-audit="description"]` — supporting copy;
- `.source-note[data-audit="source"]` — source and caveats;
- `.brand-lockup img` — embedded brand logo;
- `.generation-note[data-audit="attribution"]` — generation attribution.

`audit` uses these selectors for copy budgets, missing elements, overflow, and
contrast checks. Custom layouts may add selectors but must not remove the
contract.

## Readiness signal

Set:

```html
<script>
  window.__INFOGRAPHIC_READY__ = true;
</script>
```

only after asynchronous charts, fonts, and illustrations have settled.
The renderer waits for this signal. For a fully static poster, set it just
before `</body>`.
