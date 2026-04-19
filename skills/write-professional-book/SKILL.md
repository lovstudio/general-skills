---
name: lovstudio:write-professional-book
description: Write multi-chapter books (technical, tutorial, monograph, etc.) end-to-end. Handles outline planning, per-chapter drafting that stays coherent across long manuscripts, chapter review, and final HTML/PDF build. Trigger when user mentions "写书", "写一本书", "出书", "技术书", "book writing", "逐章写作", "O'Reilly", "mdbook", or wants to author a multi-chapter book.
version: 0.1.1
---

# write-professional-book (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
lovstudio-activate decrypt write-professional-book
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for write-professional-book. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated`, tell the user:
   > This is a paid Lovstudio skill. You need to activate it first:
   > ```
   > lovstudio-activate activate <your-license-key>
   > ```
   > Buy a license key at https://lovstudio.ai (or follow the 手工川 / ShougongChuan WeChat OA).
4. If the command prints `error: skill 'write-professional-book' not installed`, the encrypted bundle isn't on disk yet. Tell the user one of:
   > ```
   > npx skills add lovstudio/skills              # full marketplace
   > npx skills add lovstudio/write-professional-book-skill   # just this one
   > ```
   and to install the activate CLI: `pipx install lovstudio-activate`.
5. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in one of:
- `~/.claude/skills/write-professional-book/`
- `~/.claude/skills/lovstudio-write-professional-book/`
You don't need to touch it directly — just call `lovstudio-activate decrypt write-professional-book`.
