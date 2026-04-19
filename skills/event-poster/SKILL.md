---
name: lovstudio:event-poster
description: 'Create event posters and promotional graphics from a brief. Outputs print-ready high-resolution PNG. Trigger words: 海报, poster, event poster, 活动海报, 宣传图, promotional, banner, flyer'
version: 0.3.1
---

# event-poster (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
lovstudio-activate decrypt event-poster
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for event-poster. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated`, tell the user:
   > This is a paid Lovstudio skill. You need to activate it first:
   > ```
   > lovstudio-activate activate <your-license-key>
   > ```
   > Buy a license key at https://lovstudio.ai (or follow the 手工川 / ShougongChuan WeChat OA).
4. If the command prints `error: skill 'event-poster' not installed`, the encrypted bundle isn't on disk yet. Tell the user one of:
   > ```
   > npx skills add lovstudio/skills              # full marketplace
   > npx skills add lovstudio/event-poster-skill   # just this one
   > ```
   and to install the activate CLI: `pipx install lovstudio-activate`.
5. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in one of:
- `~/.claude/skills/event-poster/`
- `~/.claude/skills/lovstudio-event-poster/`
You don't need to touch it directly — just call `lovstudio-activate decrypt event-poster`.
