# lovstudio:review-docx

审阅并批注 Word 文档 — 在原 docx 上添加批注或修订，输出带标注的 docx。

Part of [lovstudio/skills](https://github.com/lovstudio/skills) — by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
npx skills add lovstudio/skills --skill lovstudio:review-docx
pip install python-docx --break-system-packages
```

## Usage

```
/review-docx @合同.docx
```

AI 提取段落 → 确认审阅模式 → 逐条分析 → 输出带批注的 docx。

## CLI

```bash
# 提取段落文本（供 AI 分析）
python3 scripts/annotate_docx.py extract --input contract.docx

# 应用批注/修订
python3 scripts/annotate_docx.py annotate \
  --input contract.docx \
  --annotations review.json \
  --output contract-reviewed.docx
```

## Annotations JSON

```json
{
  "comments": [
    {"paragraph": 3, "text": "【风险】此条款...", "author": "手工川"}
  ],
  "revisions": [
    {"paragraph": 5, "old": "原文", "new": "修改后", "author": "手工川"}
  ]
}
```

## License

MIT
