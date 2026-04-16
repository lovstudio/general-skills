# CLAUDE.md

Guidance for Claude Code when working in this repo.

## What This Is

The **central index** for Lovstudio skills. **No skill code lives here** — each skill is its own repo at `github.com/lovstudio/{name}-skill`. Locally, skills are developed under `~/lovstudio/coding/skills/{name}-skill/`.

## Repo Layout

```
.
├── README.md          # Human-readable skill catalog
├── skills.yaml        # Machine-readable manifest (source of truth for `paid` field)
├── CHANGELOG.md       # Index repo history (not per-skill)
├── LICENSE            # MIT (for this index; each skill has its own LICENSE)
└── .github/           # CI workflows (e.g. sync manifest from skill repos)
```

## skills.yaml Schema

```yaml
version: 1
skills:
  - name: any2pdf                       # skill short name (no prefix)
    repo: lovstudio/any2pdf-skill       # GitHub repo (always lovstudio/{name}-skill)
    paid: false                         # true = private repo + purchase required
    category: "Document Conversion"     # display category
    version: "0.7.1"                    # from SKILL.md (optional, CI-synced)
    description: "Markdown → …"         # from SKILL.md tagline
```

## Key Conventions

- **`paid` field is only here**, not in individual SKILL.md files. It's business classification, not skill metadata.
- **24 Free + 3 Paid = 27 skills total**. Paid: `event-poster`, `proposal`, `write-book`.
- **Naming**: GitHub repo = `lovstudio/{name}-skill`; local path = `~/lovstudio/coding/skills/{name}-skill/`. No `lovstudio-` prefix in the name.
- Skill short name (`any2pdf`) is what users invoke via `lovstudio:any2pdf` in Claude Code.

## Adding a New Skill

1. In `~/lovstudio/coding/skills/`: run the [`skill-creator`](https://github.com/lovstudio/skill-creator-skill) skill to scaffold `{name}-skill/`.
2. `cd {name}-skill && git init && git add -A && git commit && gh repo create lovstudio/{name}-skill --public --source=. --push`
3. Open a PR against this repo appending an entry to `skills.yaml` and a row to `README.md`.

For **paid** skills: pass `--private` to `gh repo create` and set `paid: true`.

## Historical Context

This repo used to be a monorepo containing all skills under `skills/lovstudio-<name>/`. In 2026-04-16 it was refactored into a pure index + 27 independent skill repos. The old `lovstudio/pro-skills` repo (which mirrored free + added 3 paid skills) was archived at the same time. See the 0.8.0 CHANGELOG entry.
