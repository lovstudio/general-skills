---
name: lovstudio:write-professional-book
description: Write multi-chapter books (technical, tutorial, monograph, etc.) end-to-end. Handles outline planning, per-chapter drafting that stays coherent across long manuscripts, chapter review, and final HTML/PDF build. Trigger when user mentions "写书", "写一本书", "出书", "技术书", "book writing", "逐章写作", "O'Reilly", "mdbook", or wants to author a multi-chapter book.
version: 0.1.1
---

# write-professional-book (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
uvx lovstudio-skill-helper decrypt write-professional-book
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for write-professional-book. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated` or `error: not logged in`, tell the user:
   > This is a paid Lovstudio skill. Activate it first (the CLI will open a browser to sign you in, then bind your license key):
   > ```
   > uvx lovstudio-skill-helper activate <your-license-key>
   > ```
   > No license key yet? Buy one at https://lovstudio.ai (or follow the 手工川 / ShougongChuan WeChat OA).
4. If the command prints `error: not entitled`, the helper will interactively prompt the user to (a) enter a license key, (b) open the purchase page, or (c) cancel. Just let the user pick.
5. If the command prints `error: skill 'write-professional-book' not installed`, the encrypted bundle isn't on disk yet. Tell the user one of:
   > ```
   > npx skills add lovstudio/skills --skill write-professional-book   # just this one
   > npx skills add lovstudio/skills                 # full marketplace
   > ```
6. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in one of:
- `~/.claude/skills/write-professional-book/`
- `~/.claude/skills/lovstudio-write-professional-book/`
You don't need to touch it directly — just call `uvx lovstudio-skill-helper decrypt write-professional-book`.
