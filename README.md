<h1 align="center">Lovstudio Skills</h1>

<p align="center">
  <strong>Central index of all Lovstudio AI coding skills for Claude Code.</strong><br>
  <sub>By <a href="https://lovstudio.ai">Lovstudio</a> · <a href="https://agentskills.io">agentskills.io</a></sub>
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="#skills">Skills</a> ·
  <a href="#install">Install</a> ·
  <a href="#how-it-works">How It Works</a> ·
  <a href="#contributing">Contributing</a> ·
  <a href="#license">License</a>
</p>

---

## What Is This

This repo is the **central index** for Lovstudio skills. Each skill lives in its own repo at `github.com/lovstudio/{name}-skill`. This repo contains:

- [`skills.yaml`](skills.yaml) — machine-readable manifest of all skills (name, repo, `paid`, category, description)
- [`README.md`](README.md) — this human-readable list
- No code. Skill code and history live in their individual repos.

Skills marked ![Free](https://img.shields.io/badge/Free-green) are open source (MIT). Skills marked ![Paid](https://img.shields.io/badge/Paid-blueviolet) are commercial — private repo, purchase required.

## Skills

<!-- COUNT:START -->
> **32 skills** — 28 Free + 4 Paid.
<!-- COUNT:END -->

<!-- SKILLS:START -->
| | Skill | Description |
|---|---|---|
| **Document Conversion** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`any2deck`](https://github.com/lovstudio/any2deck-skill) | Content → slide deck images with 16 visual styles, PPTX/PDF export, branding overlay. |
| ![Free](https://img.shields.io/badge/Free-green) | [`any2docx`](https://github.com/lovstudio/any2docx-skill) | Convert Markdown documents to professionally styled DOCX (Word) files with python-docx. |
| ![Free](https://img.shields.io/badge/Free-green) | [`any2pdf`](https://github.com/lovstudio/any2pdf-skill) | Markdown → professionally typeset PDF. CJK/Latin mixed text, code blocks, tables, 14 themes. |
| ![Free](https://img.shields.io/badge/Free-green) | [`pdf2png`](https://github.com/lovstudio/pdf2png-skill) | PDF → single vertically concatenated PNG. Uses macOS CoreGraphics, ~20x faster than pdftoppm. |
| ![Free](https://img.shields.io/badge/Free-green) | [`png2svg`](https://github.com/lovstudio/png2svg-skill) | PNG → high-quality SVG conversion with background removal and spline curves. |
| **Content Processing** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`anti-wechat-ai-check`](https://github.com/lovstudio/anti-wechat-ai-check-skill) | 检测文章 AI 痕迹 + 人性化润色，通过微信 3.27 条款检测。 |
| ![Free](https://img.shields.io/badge/Free-green) | [`document-illustrator`](https://github.com/lovstudio/document-illustrator-skill) | 为文档原地插入 AI 配图。全局规划插入点，并行生成，异步插回原文。 |
| ![Paid](https://img.shields.io/badge/Paid-blueviolet) | [`write-professional-book`](https://github.com/lovstudio/write-professional-book-skill) | Write multi-chapter books (technical, tutorial, monograph) / 逐章写书，支持多种风格 |
| ![Paid](https://img.shields.io/badge/Paid-blueviolet) | [`wxmp-cracker`](https://github.com/lovstudio/wxmp-cracker-skill) | 微信公众号文章抓取。agent-browser 自动取 token+cookie（首次扫码，之后免扫），失效自动重抿。 |
| **Image & Design** | | |
| ![Paid](https://img.shields.io/badge/Paid-blueviolet) | [`event-poster`](https://github.com/lovstudio/event-poster-skill) | Generate event posters via HTML + Playwright / 活动海报生成 |
| ![Free](https://img.shields.io/badge/Free-green) | [`image-creator`](https://github.com/lovstudio/image-creator-skill) | Multi-mechanism image generation: end-to-end AI, code rendering, or prompt engineering |
| ![Free](https://img.shields.io/badge/Free-green) | [`visual-clone`](https://github.com/lovstudio/visual-clone-skill) | Extract design DNA from reference images / 提取设计要素生成复刻指令 |
| **Academic** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`thesis-polish`](https://github.com/lovstudio/thesis-polish-skill) | MBA 论文全面润色，对标全国优秀论文标准。语言+结构+论证+创新四维提升。 |
| ![Free](https://img.shields.io/badge/Free-green) | [`translation-review`](https://github.com/lovstudio/translation-review-skill) | Chinese-to-English translation review. Compares source & translation across 6 dimensions. |
| **xBTI** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`xbti-creator`](https://github.com/lovstudio/xbti-creator-skill) | Create custom BTI personality tests (LBTI, FBTI, etc.) with AI-generated content + avatars. |
| ![Free](https://img.shields.io/badge/Free-green) | [`xbti-gallery`](https://github.com/lovstudio/xbti-gallery-skill) | Browse all community-created BTI personality tests at xbti.lovstudio.ai. |
| **Finance** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`expense-report`](https://github.com/lovstudio/expense-report-skill) | 发票图片/文字 → 分类报销 Excel。自动归类：业务招待、差旅、办公用品等。 |
| **Office Automation** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`fill-form`](https://github.com/lovstudio/fill-form-skill) | Fill Word form templates (.docx). Auto-detects table fields, CJK font support. |
| ![Free](https://img.shields.io/badge/Free-green) | [`fill-web-form`](https://github.com/lovstudio/fill-web-form-skill) | Fill web forms from local knowledge base. Fetch URL → deep-search KB → generate markdown doc. |
| ![Paid](https://img.shields.io/badge/Paid-blueviolet) | [`proposal`](https://github.com/lovstudio/proposal-skill) | Business proposal with architecture, budget & PDF / 完整商业提案 |
| ![Free](https://img.shields.io/badge/Free-green) | [`review-doc`](https://github.com/lovstudio/review-doc-skill) | Review and annotate documents/contracts — output annotated docx with comments |
| **Meta Skills** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-creator`](https://github.com/lovstudio/skill-creator-skill) | Scaffold new lovstudio skills with proper structure, SKILL.md + README.md. |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-optimizer`](https://github.com/lovstudio/skill-optimizer-skill) | Audit + auto-fix an existing skill, bump semver, and append a CHANGELOG entry. |
| **Dev Tools** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`auto-context`](https://github.com/lovstudio/auto-context-skill) | Context hygiene checker. Suggests /fork or /btw when context is polluted. |
| ![Free](https://img.shields.io/badge/Free-green) | [`cc-migrate-session`](https://github.com/lovstudio/cc-migrate-session) | Migrate Claude Code session history when a project folder moves. Rewrites ~/.claude/projects/<slug>/*.jsonl cwd fields so `claude --resume` keeps working. |
| ![Free](https://img.shields.io/badge/Free-green) | [`deploy-to-vercel`](https://github.com/lovstudio/deploy-to-vercel-skill) | Deploy frontend to Vercel with auto Cloudflare DNS + custom domain setup. |
| ![Free](https://img.shields.io/badge/Free-green) | [`finder-action`](https://github.com/lovstudio/finder-action-skill) | Generate Mac Finder right-click menu actions. Quick Action or Finder Sync Extension. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-access`](https://github.com/lovstudio/gh-access-skill) | Grant / revoke / list collaborator access on private GitHub repos by username or email. Read-only by default. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-contribute`](https://github.com/lovstudio/gh-contribute-skill) | Contribute clean, professional PRs to upstream GitHub repos — fork, branch, commit, push, open PR, with smart splitting. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-tidy`](https://github.com/lovstudio/gh-tidy-skill) | Triage & clean up GitHub issues, PRs, branches, and labels in one pass. |
| ![Free](https://img.shields.io/badge/Free-green) | [`obsidian-reset-cache`](https://github.com/lovstudio/obsidian-reset-cache-skill) | 重置 Obsidian 缓存，解决卡在 Loading cache 的问题。 |
| ![Free](https://img.shields.io/badge/Free-green) | [`project-port`](https://github.com/lovstudio/project-port-skill) | Generate stable unique dev port (3000–8999) from project name. |
<!-- SKILLS:END -->

<sub>The table above is auto-generated from [`skills.yaml`](skills.yaml) by [`scripts/render-readme.py`](scripts/render-readme.py). Edit `skills.yaml`, not this table.</sub>

## Install

Each skill installs independently via its own repo. Example:

```bash
# Free skill
git clone https://github.com/lovstudio/any2pdf-skill ~/.claude/skills/lovstudio-any2pdf

# Paid skill (after purchase — use SSH with your authorized key)
git clone git@github.com:lovstudio/write-professional-book-skill ~/.claude/skills/lovstudio-write-professional-book
```

Browse and install via [agentskills.io](https://agentskills.io) for a one-click experience.

## How It Works

```
lovstudio/skills (this repo)         ← you are here
├── README.md                        ← human-readable index (English)
├── README.zh-CN.md                  ← 中文版
├── skills.yaml                      ← machine-readable manifest
└── .github/workflows/               ← CI: renders READMEs, syncs descriptions

lovstudio/<name>-skill (27 repos)    ← each skill, independent repo
├── SKILL.md                         ← skill definition (frontmatter + docs)
├── scripts/                         ← implementation (Python/Shell/Node)
├── README.md                        ← per-skill install & usage
└── examples/ · references/          ← optional assets
```

The **`paid` field** lives in `skills.yaml` (this repo), not in each SKILL.md — it's a business categorization, not a skill property. Paid skill code is private; public trigger info (name, tagline, category) is still indexed here so agentskills.io can display and prompt purchase.

## Contributing

- **New skill**: use [`skill-creator`](https://github.com/lovstudio/skill-creator-skill) to scaffold. Then create a repo at `lovstudio/{name}-skill` and open a PR here adding it to `skills.yaml`.
- **Existing skill**: file issues / PRs in the skill's own repo.
- **Index fixes** (categorization, descriptions, links): PR against this repo's `skills.yaml`. **Don't touch the README table** — CI regenerates it.

## License

- **This index repo**: MIT
- **Free skills**: MIT (see each repo's LICENSE)
- **Paid skills**: commercial license — see the skill's purchase page

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=lovstudio/skills&type=Date)](https://star-history.com/#lovstudio/skills&Date)

---

<p align="center">
  <sub>Built with <a href="https://claude.com/claude-code">Claude Code</a> · by <a href="https://lovstudio.ai">Lovstudio</a></sub>
</p>
