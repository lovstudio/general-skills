---
name: lovstudio:image-creator
category: Content Creation
tagline: "Generate images using Gemini via ZenMux. Supports ASCII art output."
description: Generate images using Gemini via ZenMux
allowed-tools: [Bash, Read]
---

# Usage

```bash
python3 ~/.claude/skills/lovstudio-image-creator/gen_image.py "PROMPT" [-o output.png] [-q low|medium|high] [--ascii]
```

Display result with `Read` tool after generation.
