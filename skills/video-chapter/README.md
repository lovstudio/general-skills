# lovstudio-video-chapter

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)
![License](https://img.shields.io/badge/license-MIT-green)

基于 SRT/VTT 字幕，把长视频整理成 3–5 个语义完整的章节，并输出自然切点、标题、摘要和可直接粘贴的时间码。

Part of [lovstudio general skills](https://github.com/lovstudio/general-skills) — by [lovstudio.ai](https://lovstudio.ai)

## 它解决什么问题

普通进度条工具只知道时间，不理解内容；简单等分视频又经常把一句话或一个案例从中间切断。这个 skill 把两件事分开处理：

```text
SRT / VTT
   │
   ├─ Python CLI：可靠解析时间码、整理逐分钟文本、发现停顿
   │
   └─ AI Agent：理解主题转折、选择自然切点、命名章节
                    │
                    └─ 章节表 + Chapter Bar / YouTube / Bilibili 时间码
```

## 安装

```bash
git clone https://github.com/lovstudio/video-chapter-skill \
  "${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-video-chapter"
```

也可以使用 LovStudio 技能安装器：

```bash
npx lovstudio skills add video-chapter -g -y
```

依赖：Python 3.8+，无需第三方 Python 包。

## 使用方式

在支持 Agent Skills 的 AI 工具中提供字幕文件，然后说：

```text
基于这个 SRT 把视频分成 3–5 段，给出时间范围、标题和摘要。
```

也支持这些触发方式：

- “给这个教程视频生成 5 个章节”
- “根据字幕找自然切点”
- “输出 Chapter Bar 可以直接粘贴的章节时间”
- “Split this video into chapters from its subtitles”
- “Create YouTube chapters from this VTT”

## CLI

CLI 负责生成给 Agent 阅读的分析包，不会用机械等分代替语义判断。

```bash
SKILL_DIR="${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-video-chapter"

python3 "$SKILL_DIR/scripts/subtitle_chapters.py" \
  --input "/path/to/video.srt" \
  --segments 5 \
  --output "/tmp/video-chapter-analysis.md"
```

输出 JSON：

```bash
python3 "$SKILL_DIR/scripts/subtitle_chapters.py" \
  --input "/path/to/video.vtt" \
  --segments 4 \
  --format json
```

## 参数

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `--input` | 必填 | SRT 或 VTT 字幕文件 |
| `--segments` | `5` | 章节数，只接受 3、4、5 |
| `--chunk-seconds` | `60` | 分析文本窗口长度 |
| `--gap-threshold` | `1.5` | 收录字幕停顿的最短秒数 |
| `--max-gaps` | `20` | 最多展示多少个停顿候选 |
| `--format` | `markdown` | `markdown` 或 `json` |
| `--output` | `-` | 输出文件；`-` 表示标准输出 |

## 默认交付

```markdown
| 段落 | 时间范围 | 标题 | 内容 |
|---|---|---|---|
| 1 | 00:00–04:16 | 从成品开始 | 展示最终效果并介绍制作目标 |
```

以及可直接粘贴到 Chapter Bar、YouTube 或 Bilibili 的文本：

```text
00:00 从成品开始
04:16 挑选并评估 Skill
```

## 隐私

脚本只读取本地字幕文件，不上传视频或字幕，也不要求用户配置文件。

## License

MIT
