---
name: lovstudio:paid-add
description: Compute the sum of two numbers. The simplest possible skill, used as an end-to-end test for the paid-skill encryption + activation protocol. Trigger when the user says "paid add", "/paid-add", "用 paid-add 算", or asks to use the paid-add skill.
version: 0.1.1
---

# paid-add (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
uvx lovstudio-skill-helper decrypt paid-add
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for paid-add. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated` or `error: not logged in`, tell the user:
   > 这是一个 Lovstudio 付费 skill，请先激活（CLI 会打开浏览器让你登录，然后绑定你的 license key）：
   > ```
   > uvx lovstudio-skill-helper activate <your-license-key>
   > ```
   > 还没有 license key？前往 https://lovstudio.ai 购买，或关注 #公众号：手工川 购买。
4. If the command prints `error: not entitled`, the helper will interactively prompt the user to (a) enter a license key, (b) open the purchase page, or (c) cancel. Just let the user pick.
5. If the command prints `error: skill 'paid-add' not installed`, the encrypted bundle isn't on disk yet. Tell the user one of:
   > ```
   > npx skills add lovstudio/skills --skill paid-add   # just this one
   > npx skills add lovstudio/skills                 # full marketplace
   > ```
6. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in one of:
- `~/.claude/skills/paid-add/`
- `~/.claude/skills/lovstudio-paid-add/`
You don't need to touch it directly — just call `uvx lovstudio-skill-helper decrypt paid-add`.
