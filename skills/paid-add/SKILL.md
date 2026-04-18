---
name: paid-add
description: Compute the sum of two numbers. The simplest possible skill, used as an end-to-end test for the paid-skill encryption + activation protocol. Trigger when the user says "paid add", "/paid-add", "用 paid-add 算", or asks to use the paid-add skill.
version: 0.1.0
---

# paid-add (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
lovstudio-activate decrypt paid-add
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for paid-add. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated`, tell the user:
   > This is a paid Lovstudio skill. You need to activate it first:
   > ```
   > lovstudio-activate activate <your-license-key>
   > ```
   > If you don't have a license key, follow the 手工川 (ShougongChuan) WeChat official account to purchase one.
4. If the command prints `error: skill 'paid-add' not installed`, it means `~/.lovstudio/brand_skills/paid-add/` is empty. Tell the user to re-run `npx skills add lovstudio/skills` or to install the `lovstudio-activate` CLI (`pipx install lovstudio-activate`).
5. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in `~/.lovstudio/brand_skills/paid-add/` (or alongside this file, whichever the CLI finds). You don't need to touch it directly — just call `lovstudio-activate decrypt paid-add`.
