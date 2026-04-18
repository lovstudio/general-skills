---
name: proposal
description: Generate complete business proposals for client projects. Takes client requirement documents (docx/pdf/md) or verbal descriptions as input, outputs a professionally formatted proposal with technical architecture, budget, timeline, risk analysis, and team introduction. Automatically calls illustrate for images and any2pdf for final PDF delivery. Trigger when user mentions "商务方案", "合作评估", "项目评估", "报价方案", "proposal", "需求评估", "给客户出方案", or wants to generate a client-facing project proposal from requirements.
version: 0.1.0
---

# proposal (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
lovstudio-activate decrypt proposal
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for proposal. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated`, tell the user:
   > This is a paid Lovstudio skill. You need to activate it first:
   > ```
   > lovstudio-activate activate <your-license-key>
   > ```
   > If you don't have a license key, follow the 手工川 (ShougongChuan) WeChat official account to purchase one.
4. If the command prints `error: skill 'proposal' not installed`, it means `~/.lovstudio/brand_skills/proposal/` is empty. Tell the user to re-run `npx skills add lovstudio/skills` or to install the `lovstudio-activate` CLI (`pipx install lovstudio-activate`).
5. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in `~/.lovstudio/brand_skills/proposal/` (or alongside this file, whichever the CLI finds). You don't need to touch it directly — just call `lovstudio-activate decrypt proposal`.
