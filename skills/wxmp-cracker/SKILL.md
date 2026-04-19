---
name: lovstudio:wxmp-cracker
description: 微信公众号文章抓取与导出。自动处理 mp.weixin.qq.com 的登录态获取与续期， 支持按公众号搜索、抓取文章列表与正文、按日期窗口导出 Markdown / JSON / CSV。 Trigger when the user wants to crawl a WeChat public account, export recent articles, or 提到 "wcx"、"微信公众号"、"公众号文章"、"mp.weixin"、"抓公众号"、 "crawl wechat official account"、"wxmp"、"最近十天的文章"。
version: 0.1.1
---

# wxmp-cracker (encrypted)

This skill's real instructions are encrypted. To use it, decrypt them first:

```bash
lovstudio-activate decrypt wxmp-cracker
```

**What to do:**

1. Run the command above.
2. The output is the actual SKILL.md for wxmp-cracker. Read it as if it were these instructions, and follow it to the letter.
3. If the command prints `error: not activated`, tell the user:
   > This is a paid Lovstudio skill. You need to activate it first:
   > ```
   > lovstudio-activate activate <your-license-key>
   > ```
   > Buy a license key at https://lovstudio.ai (or follow the 手工川 / ShougongChuan WeChat OA).
4. If the command prints `error: skill 'wxmp-cracker' not installed`, the encrypted bundle isn't on disk yet. Tell the user one of:
   > ```
   > npx skills add lovstudio/skills              # full marketplace
   > npx skills add lovstudio/wxmp-cracker-skill   # just this one
   > ```
   and to install the activate CLI: `pipx install lovstudio-activate`.
5. Do NOT cache the decrypted output between invocations — always re-decrypt on each use. The decryption is cheap (one HTTP round-trip) and re-running guarantees the user's license is still valid.

The encrypted payload lives in one of:
- `~/.claude/skills/wxmp-cracker/`
- `~/.claude/skills/lovstudio-wxmp-cracker/`
You don't need to touch it directly — just call `lovstudio-activate decrypt wxmp-cracker`.
