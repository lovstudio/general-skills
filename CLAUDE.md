# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A multi-skill repo publishing AI coding assistant skills via [agentskills.io](https://agentskills.io). Each skill lives in its own `lovstudio-<name>/` directory with a `SKILL.md` (frontmatter + usage docs) and a `scripts/` folder containing the Python implementation.

## Repo Layout

```
lovstudio-<name>/
  SKILL.md          # Skill definition (frontmatter + instructions for AI assistants)
  scripts/          # Python scripts that do the actual work
  references/       # Optional theme/config docs
  examples/         # Optional example files
dev.sh              # Symlinks source skills into ~/.claude/skills/ for live development
```

## Skills

| Skill | Script | Deps |
|-------|--------|------|
| `any2pdf` | `lovstudio-any2pdf/scripts/md2pdf.py` (reportlab) | `pip install reportlab` |
| `any2docx` | `lovstudio-any2docx/scripts/md2docx.py` (python-docx) | `pip install python-docx` |

Both convert Markdown → styled output with CJK/Latin mixed text support, themes, cover pages, TOC, watermarks.

## Development

```bash
# Live-link all skills for testing in Claude Code sessions
bash dev.sh

# Link a single skill
bash dev.sh lovstudio-any2pdf

# Run a conversion directly
python lovstudio-any2pdf/scripts/md2pdf.py --input foo.md --output foo.pdf --theme warm-academic
python lovstudio-any2docx/scripts/md2docx.py --input foo.md --output foo.docx --theme warm-academic
```

## Adding a New Skill

1. Create `lovstudio-<name>/` with a `SKILL.md` (follow existing frontmatter format: name, description, license, compatibility, metadata)
2. Add scripts in `lovstudio-<name>/scripts/`
3. Update `README.md` table

## Key Conventions

- Skill names use prefix `lovstudio:` (e.g. `lovstudio:any2pdf`)
- Directory names use prefix `lovstudio-` (e.g. `lovstudio-any2pdf`)
- Both skills share the same set of 10+ color themes (warm-academic, nord-frost, github-light, etc.)
- SKILL.md files must use `AskUserQuestion` to prompt users for options before running conversion — never skip this interactive step
- Python scripts are standalone single-file CLIs with `argparse`; no package structure
- CJK text handling is a core concern — font switching, mixed-text rendering, and line wrapping must work correctly
