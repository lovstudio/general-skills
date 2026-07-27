---
name: lovstudio-video-chapter
description: >
  Turn timestamped subtitle files into a clear 3–5 chapter video structure with
  natural cut points, concise titles, summaries, and copy-ready chapter lists.
  Use for SRT/VTT chaptering, long-form video segmentation, progress-bar labels,
  or when the user asks "基于字幕进行视频分段", "给视频分章节", "生成章节时间点",
  "split this video from subtitles", or "create video chapters".
license: MIT
compatibility: >
  Portable Agent Skills format. Requires Python 3.8+ only; the helper CLI uses
  the standard library and reads explicit SRT/VTT input paths.
metadata:
  author: lovstudio
  version: "0.1.0"
  tags: video subtitle srt vtt chapters segmentation editing
---

# Video Chapter — 基于字幕进行视频分段

Read an SRT or VTT subtitle file, identify genuine topic changes, and return a
small set of useful video chapters. The helper CLI handles deterministic
parsing; the agent performs the semantic judgment.

## When to Use

- The user supplies an `.srt` or `.vtt` and wants the video divided into 3–5 parts.
- A long tutorial, interview, podcast, or presentation needs chapter markers.
- The user needs copy-ready labels for Chapter Bar, YouTube, Bilibili, or an editor.
- The user wants natural editorial cut points rather than equal-length slices.

Do not use this skill merely to split a media file at already-known timestamps.

## User Configuration

No user profile is required. Read only the explicit subtitle path and write only
to an explicit output path or a temporary working file. Never assume a personal
workspace or fixed installation directory.

## Workflow (MANDATORY)

Follow these steps in order.

### Step 0: Resolve known inputs

Use conversation context before asking anything:

1. Resolve the subtitle path.
2. Resolve the desired chapter count. Accept only 3, 4, or 5.
3. Resolve the intended output:
   - editorial chapter table;
   - platform timestamp list;
   - Chapter Bar paste block;
   - or all three.

If the user says “3–5 段为佳” without a stronger preference, use **5** for
videos longer than 20 minutes, **4** for 8–20 minutes, and **3** for shorter
videos. Do not ask a redundant question when the context already answers it.

If a required choice is genuinely missing, use the host's user-question tool
before running the conversion. Ask one short question at a time.

### Step 1: Build the analysis pack

Resolve the installed skill root from the active skill context. For manual use:

```bash
export SKILL_DIR="/path/to/lovstudio-video-chapter"
```

Run:

```bash
python3 "$SKILL_DIR/scripts/subtitle_chapters.py" \
  --input "/path/to/subtitles.srt" \
  --segments 5 \
  --output "/tmp/video-chapter-analysis.md"
```

Read the generated analysis pack completely. It contains duration, cue count,
chronological transcript windows, and meaningful subtitle gaps. Transcript
windows are reading aids, **not proposed chapters**.

### Step 2: Find semantic boundaries

Select chapter boundaries using this priority order:

1. A clear topic, task, speaker question, or workflow-stage transition.
2. A completed sentence near that transition.
3. A subtitle gap or visual pause that supports the transition.
4. Reasonably balanced duration as a soft constraint.

Rules:

- Use 3–5 chapters, matching the requested count.
- Start the first chapter at `00:00`.
- Place later cuts on the start time of an actual subtitle cue.
- Never cut in the middle of a sentence or example.
- Prefer a slightly uneven but coherent structure over equal-length slicing.
- Keep every chapter independently understandable.
- Treat loading failures, dead air, repeated takes, and troubleshooting detours
  as optional trimming notes, not as chapters.
- Do not invent content that is absent from the subtitles.
- If subtitles are too sparse or corrupted for semantic segmentation, say so
  and return only defensible boundaries.

### Step 3: Name and summarize

For every chapter:

- Use a concrete, content-bearing title.
- Chinese titles should usually be 8–18 characters.
- Avoid generic labels such as “第一部分”, “继续讲解”, or “其他”.
- Write a one-sentence summary grounded in the corresponding subtitle range.

### Step 4: Validate

Before responding, verify:

- timestamps are strictly increasing;
- no timestamp exceeds the subtitle duration;
- every range closes where the next one begins;
- the requested number of chapters is present;
- titles match the content following their timestamps;
- optional trims are clearly separated from chapter boundaries.

### Step 5: Deliver

Default to a compact table:

| 段落 | 时间范围 | 标题 | 内容 |
|---|---|---|---|
| 1 | `00:00–04:16` | … | … |

Then include a copy-ready timestamp block:

```text
00:00 第一章标题
04:16 第二章标题
```

When the target is Chapter Bar, also state the total video duration separately;
do not add a zero-length “结束” chapter. For YouTube/Bilibili, use chapter start
times only.

## CLI Reference

```bash
python3 "$SKILL_DIR/scripts/subtitle_chapters.py" --help
```

| Argument | Default | Description |
|---|---:|---|
| `--input` | required | Input `.srt` or `.vtt` subtitle file |
| `--segments` | `5` | Requested chapter count: 3, 4, or 5 |
| `--chunk-seconds` | `60` | Transcript analysis-window size |
| `--gap-threshold` | `1.5` | Minimum subtitle gap, in seconds, to report |
| `--max-gaps` | `20` | Maximum number of meaningful gaps to include |
| `--format` | `markdown` | Analysis-pack format: `markdown` or `json` |
| `--output` | `-` | Output path, or `-` for stdout |

## Failure Handling

- Missing/unreadable file: report the exact path and stop.
- Unsupported format: ask for SRT or VTT.
- No valid cues: explain that the subtitle timing could not be parsed.
- Non-monotonic cues: keep parsing, surface warnings, and avoid invalid cuts.
- Extremely long transcript: increase `--chunk-seconds`; never silently omit
  the ending.

## Dependencies

Python 3.8+ standard library only.
