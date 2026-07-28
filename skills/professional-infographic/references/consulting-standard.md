# Consulting Exhibit standard

“Consulting-grade” means an evidence-led Exhibit, not imitation of or affiliation
with a named firm. The page must make a defensible argument visible.

Read `exhibit-benchmark.md` before authoring or reviewing the first Exhibit in a
session.

## Contents

1. The unit of work is an Exhibit
2. Decision and evidence graph
3. Action titles
4. Evidence ledger
5. Information density
6. Visual variables
7. Copy editing
8. Rejection patterns
9. Quality rubric
10. Definition of done

## 1. The unit of work is an Exhibit

An Exhibit is not a poster decorated with information. It contains:

1. a figure label;
2. an action title that states the answer;
3. one dominant visual relationship;
4. directly attached evidence and annotations;
5. a note/source line;
6. restrained brand ownership.

The visual must prove the title. If the visual only repeats the title in boxes,
the Exhibit has failed.

## 2. Start with a decision and an evidence graph

Before layout, write:

- audience and use moment;
- decision or belief that should change;
- one governing conclusion;
- 3–7 claims, criteria, drivers, stages, or entities needed to prove it;
- exact evidence supporting every visible mark;
- assumptions and material omissions.

Map the argument:

```text
Action title
├── visible claim / decision criterion
│   ├── evidence ID
│   └── visual encoding + direct annotation
├── visible claim / decision criterion
│   ├── evidence ID
│   └── visual encoding + direct annotation
└── implication / decision
```

Do not begin HTML until the map exists in `brief.md`.

## 3. Write an action title

The title must contain a subject, a directional finding, and—when useful—a
business implication.

| Weak | Strong |
|---|---|
| 跨端方案对比 | 四类特殊约束各有优先路线；无特殊约束时 RN + Expo 是均衡默认 |
| AI 市场趋势 | AI 原生公司增长更快，既有 SaaS 必须先守住高渗透工作流 |
| 产品路线图 | 两个能力 Gate 决定规模化时间，功能数量不是关键路径 |

Rules:

- Prefer one line; allow two lines when the conclusion needs a qualification.
- Do not add a separate takeaway band that restates the same sentence.
- Avoid empty claims such as “至关重要”“正在改变一切”“没有绝对答案”.
- Put the most decision-relevant contrast early.
- Use 12–28 semantic units as the normal range and 42 as a hard ceiling.

## 4. Maintain an evidence ledger

For every value, rank, position, causal arrow, decision cell, and named fact,
record:

- evidence ID;
- exact source text or value;
- location / URL;
- unit, denominator, and period;
- fact, estimate, assumption, or interpretation;
- caveat.

In HTML, link visible marks back to the ledger with `data-source-ref="S1"`.

Rules:

- Never invent values to make a chart possible.
- Never turn adjectives into percentages.
- Label qualitative coordinates or strength explicitly as qualitative.
- Do not imply causation from correlation.
- Use a conceptual diagram when comparable evidence is missing.

## 5. Maximize encoded information, not word count

Information density is the ratio of useful distinctions to visual area.

Useful distinctions include:

- comparable values on a shared scale;
- directly labeled differences;
- conditions and branches;
- driver hierarchy;
- axis position and zones;
- milestones and gates;
- actor–capability–flow relationships;
- annotations that explain a discontinuity or decision.

Prose inside a large rectangle is not information density.

Default composition for a 16:9 Exhibit:

| Region | Target |
|---|---:|
| Brand + figure label | 3%–5% of height |
| Action-title region | 8%–15% |
| Main visual | 65%–78% |
| Notes, source, attribution | 5%–8% |

Use the space to enlarge the visual and annotations, not to create empty cards.

## 6. Use visual variables deliberately

Every use of position, length, color, shape, connection, order, or containment
must encode a named meaning.

Priority for quantitative precision:

```text
position on common scale
> length
> position on nonaligned scale
> area
> angle
> decorative color
```

Rules:

- Use color for one semantic distinction, normally decision / exception /
  category. Do not alternate colors for decoration.
- Direct-label values and series whenever space allows.
- Use a legend only when direct labels would make reading slower.
- Annotate the evidence that supports the action title.
- Use one shared scale across a comparison or small-multiple set.

## 7. Edit copy by role

Suggested budgets count one CJK character or one Latin word as one semantic
unit:

| Element | Normal | Hard ceiling |
|---|---:|---:|
| Action title | 12–28 | 42 |
| Deck / reading instruction | 12–32 | 56 |
| Entity or dimension label | 2–12 | 20 |
| Direct annotation | 4–18 | 28 |
| Outcome / implication | 8–28 | 48 |
| Source / note | as required | must remain readable |

Edit in this order:

1. delete repetition;
2. convert sentences into precise labels;
3. attach qualifiers to the relevant mark;
4. move methodology into the note;
5. split the story;
6. reduce font size only as the last resort.

## 8. Reject anti-patterns

Reject:

- a bento grid used because the source is long;
- three to five equal cards under an oversized title;
- a “matrix” that is only prose in aligned columns;
- a “decision tree” without testable conditions and labeled branches;
- a 2×2 with vague axes, unlabeled ends, or decorative coordinates;
- random icons, blobs, rings, gradients, fake UI, 3D, glow, or emoji;
- unsupported scores, market positions, or causal arrows;
- duplicated conclusion bands;
- source notes that cannot be mapped to individual claims.

## 9. Quality rubric

Score 100 points:

| Dimension | Points | Minimum for critical dimensions |
|---|---:|---:|
| Core conclusion | 20 | 16 |
| Evidence quality | 20 | 12 |
| Visual encoding | 20 | 14 |
| Information density | 15 | 10 |
| Copy and annotations | 10 | — |
| Layout and typography | 10 | — |
| Source and brand | 5 | — |

Release threshold: 85/100 and no critical dimension below minimum.

The CLI score is a conservative machine proxy. It can detect missing semantics,
bad area ratios, empty blocks, weak evidence linkage, overflow, and similar
failures. It cannot judge truth, insight, or taste. A human/vision review of the
rendered image is always required.

## 10. Definition of done

The Exhibit is done only when:

- the title is a supported, non-obvious conclusion;
- the visual proves the title in five seconds;
- the reader has one clear entry point and path;
- all marks map to evidence;
- variables and scales are explicit;
- notes and caveats are readable;
- removing any remaining element would weaken meaning or trust;
- the automatic gate passes;
- the rendered image passes full-page and 100% visual inspection.
