---
name: lovstudio:review-docx
description: >
  Review and annotate Word documents (.docx) with comments and/or tracked changes.
  Primary use case: contract and agreement review — identifying risks, imbalanced
  clauses, vague terms, and missing provisions. Also supports general document review.
  Trigger when: user asks to "审阅", "批注", "review", "annotate" a .docx file,
  or asks to review a contract/agreement/合同/协议 that is in Word format.
license: MIT
compatibility: >
  Requires Python 3.8+ and python-docx (`pip install python-docx`).
  Cross-platform: macOS, Windows, Linux.
metadata:
  author: lovstudio
  version: "0.1.0"
  tags: docx, review, annotate, contract, legal
---

# review-docx — 审阅并批注 Word 文档

读取 Word 文档，AI 进行审查分析，将审查意见以批注（comment）或修订模式
（track changes）写回原文档，输出带批注的 docx。

## When to Use

- 用户提供 .docx 文件要求审阅、审查、批注
- 合同/协议审查：识别风险条款、权利义务失衡、模糊表述、缺失条款
- 通用文档审阅：语法、逻辑、格式、内容完整性

## Workflow

### Step 1: Extract text

用脚本提取段落文本和索引：

    python3 lovstudio-review-docx/scripts/annotate_docx.py extract --input <path.docx>

输出 JSON 数组，每项含 `index`（段落序号）和 `text`（段落文本）。

### Step 2: Ask the user

**IMPORTANT: Use `AskUserQuestion` BEFORE generating annotations.**

    审阅模式确认 👇

    ━━━ 📋 审阅类型 ━━━
    a) 合同/协议审查 — 风险条款、权利义务、模糊表述、缺失条款
    b) 通用文档审阅 — 语法、逻辑、格式、内容完整性

    ━━━ ✏️ 批注方式 ━━━
    a) 批注模式（默认） — 在原文旁加 comment，不改原文
    b) 修订模式 — 用 track changes 直接改原文，对方可逐条接受/拒绝
    c) 批注 + 修订 — 批注写分析意见，修订写建议改法

    ━━━ 👤 批注者署名 ━━━
    默认 "手工川"，可自定义

### Step 3: AI Review

根据提取的文本进行审查。对于合同审查，重点关注：

1. **风险条款** — 单方权利过大、免责条款、不可抗力滥用
2. **权利义务失衡** — 一方义务过重、对价不充分
3. **模糊表述** — "合理"、"适当"等无客观标准的词语
4. **缺失条款** — 争议解决、终止后义务、知识产权归属
5. **期限与金额** — 过短/过长期限、不合理金额
6. **法律合规** — 管辖法律、仲裁条款

生成 annotations JSON，格式：

    {
      "comments": [
        {
          "paragraph": 18,
          "text": "【风险】Sourced Deal 认定...",
          "author": "手工川"
        }
      ],
      "revisions": [
        {
          "paragraph": 12,
          "old": "terminates automatically",
          "new": "terminates automatically, provided that...",
          "author": "手工川"
        }
      ]
    }

批注文本格式规范：
- 以标签开头：`【风险】`、`【建议】`、`【缺失】`、`【模糊】`、`【注意】`
- 简明扼要，每条批注控制在 1-3 句话
- 有建议时给出具体修改方向

### Step 4: Apply annotations

将 JSON 写入临时文件，调用脚本：

    python3 lovstudio-review-docx/scripts/annotate_docx.py annotate \
      --input <原文.docx> \
      --annotations <annotations.json> \
      --output <输出路径.docx>

### Step 5: Output naming

输出文件名规范：`手工川-{原文件名}-审阅-{YYYY-MM-DD}-v0.1.docx`

放在原文件同目录下。

## CLI Reference

    python3 annotate_docx.py extract --input <path.docx>
    python3 annotate_docx.py annotate --input <path.docx> --annotations <json> --output <path.docx>

| Subcommand | Argument | Description |
|------------|----------|-------------|
| `extract` | `--input` | 输入 docx 路径 |
| `annotate` | `--input` | 输入 docx 路径 |
| `annotate` | `--annotations` | JSON 批注文件路径 |
| `annotate` | `--output` | 输出 docx 路径 |

## Comment JSON Fields

| Field | Required | Description |
|-------|----------|-------------|
| `paragraph` | Yes | 0-based 段落索引 |
| `text` | Yes | 批注内容 |
| `author` | No | 批注者署名（默认 "Reviewer"） |
| `start` | No | 字符偏移起始位置（精确高亮） |
| `end` | No | 字符偏移结束位置 |

## Revision JSON Fields

| Field | Required | Description |
|-------|----------|-------------|
| `paragraph` | Yes | 0-based 段落索引 |
| `old` | Yes | 要替换的原文 |
| `new` | Yes | 修改后的文本 |
| `author` | No | 修订者署名 |

## Dependencies

    pip install python-docx --break-system-packages
