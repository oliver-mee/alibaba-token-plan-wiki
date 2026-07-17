---
title: Model Studio per-model pricing + specs (console model-details pages)
region: global
source: https://modelstudio.console.alibabacloud.com/ — per-model details page
source_type: console UI (JS-rendered, not in public docs; captured by screenshot)
pricing_basis: Model Studio standard pay-as-you-go, USD per 1M tokens
relation_to_token_plan: >
  ⚠️ SUPERSEDED AS THE COSTING BASIS. Measurement on 2026-07-16 (see
  credit-rate-experiment.md) proved the Token Plan meters against the CHINESE
  MAINLAND price sheet, not this International one, despite serving inference
  from Singapore. Under mainland rates, credits-per-dollar is constant across
  models to within 0.4%; under these international rates it varies by 13-27%,
  so it is not the billing basis. The bundled-PAYG model itself was CONFIRMED
  (identical work on deepseek-v4-pro cost exactly 12x deepseek-v4-flash, matching
  their 12x price ratio) — only the price sheet was wrong.
  This file remains the authoritative INTERNATIONAL datasheet and the source of
  record for capabilities, limits, modalities and tool pricing, none of which
  the finding affects. For cost comparison use the mainland sheet.
purpose: >
  Originally: feed the intelligence-vs-cost comparison page. Now: the
  International reference datasheet + the record of capability/limit
  discrepancies against our shipped metadata. Costing moved to the mainland sheet.
supersedes_note: cost tables below are International rates — NOT what the plan bills.
status: complete — all 14 chat models captured, all tiers.
pricing_complications:
  - Qwen models use TIERED pricing by input length (<=256k, 256k<input<=1m).
    Tier 2 is 2.4x-4x tier 1. DeepSeek models are flat.
  - Some models carry LIMITED-TIME discounts (qwen3.7-plus 20% off,
    qwen3.7-max 50% off) that will expire. Both original and effective
    rates are recorded per model.
  - Qwen models expose EXPLICIT cache (creation + read) as well as implicit;
    DeepSeek exposes implicit only. Not a like-for-like cache comparison.
updated: 2026-07-16
related: [token-plan-reference.md, global-models.md]
---

# Model Studio per-model pricing + specs (INTERNATIONAL)

Captured from each model's console details page. The console is the only place
these values exist: the public `/help/en/model-studio/models` page carries
availability and API-compatibility only, and the token-plan overview page
carries seat tiers only. Both were checked 2026-07-16.

> ## 🚨 Read this before using the prices below
>
> **These International rates are NOT what the Token Plan bills against.**
> Measurement on 2026-07-16 proved the plan meters at **Chinese Mainland** rates
> despite Singapore inference. See `credit-rate-experiment.md` for the evidence
> and `model-studio-pricing-cn.md` for the sheet that actually applies.
>
> What survives unchanged: **capabilities, limits, modalities, tool pricing, the
> `deepseek-v3.2` retirement, and every discrepancy against our shipped
> metadata.** Those are the load-bearing parts of this file and none of them
> depend on the price sheet.
>
> What does not: the cost tables, and every dominance verdict derived from them.
>
> ## 🚨 Four rows in this file are MISLABELLED — they are mainland, not international
>
> `glm-5`, `MiniMax-M2.5`, `kimi-k2.6` and `kimi-k2.5` **are not offered in the
> Singapore region at all** (established 2026-07-16). They have no international
> price. The figures recorded for them below were captured from the mainland
> sheet without that being noticed, so they are **correct numbers under the wrong
> label**. Their authoritative home is `model-studio-pricing-cn.md`.
>
> Of the 14 Token Plan chat models, only 10 exist on the international sheet.
> `kimi-k2.7-code` is the sole Kimi available there.

## Why this matters

our internal model-metadata reference models cost as **0** everywhere downstream (models.dev,
openclaw, hermes) because the plan is prepaid — correct for those catalogs, since
there is no incremental per-token charge to surface. But it means nothing in our
data tells us which token-plan model burns credits fastest.

The original finding still holds in shape: `deepseek-v4-pro` is **not cheap on
Alibaba**. Artificial Analysis has it at $0.048/task because DeepSeek's own API is
dirt cheap; on Alibaba it is a mid-to-premium model ($1.65/$3.301 mainland,
$2.4/$4.8 international). Any "DeepSeek Pro is the value pick" intuition carried
over from AA does not survive the token plan. The magnitude changes with the
sheet; the conclusion does not.

## Price summary (USD per 1M tokens)

**Effective rates** (after any limited-time discount) at the **tier-1 input band**
(`input <= 256k`) where tiered. This is the basis for the comparison chart:
tier 1 covers the overwhelming majority of real calls.

| Model | Input | Output | Implicit cache | Notes |
|---|---:|---:|---:|---|
| `deepseek-v4-pro` | 2.40 | 4.80 | 0.20 | flat |
| `deepseek-v4-flash` | 0.20 | 0.40 | 0.04 | flat; 12x cheaper than v4-pro, both sides |
| `deepseek-v3.2` | 0.57 | 1.71 | 0.114 | flat; **⚠️ retires 10 Oct** |
| `qwen3.7-max` | 1.25 | 3.75 | 0.25 | flat; **50% off, limited-time** (orig 2.50 / 7.50 / 0.50) |
| `qwen3.7-plus` | 0.32 | 1.28 | 0.064 | tiered; **20% off, limited-time** (orig 0.40 / 1.60 / 0.08) |
| `qwen3.6-plus` | 0.50 | 3.00 | n/a | tiered; no discount; no implicit cache |
| `qwen3.6-flash` | 0.25 | 1.50 | n/a | tiered; no discount; explicit cache only |
| `kimi-k2.7-code` | 0.95 | 4.00 | 0.19 | flat |
| `kimi-k2.6` | 0.8939 | 3.7131 | 0.1788 | ⚠️ **MAINLAND** — no INTL price exists |
| `kimi-k2.5` | 0.574 | 3.011 | 0.115 | ⚠️ **MAINLAND** — no INTL price exists |
| `glm-5.2` | 1.40 | 4.40 | 0.28 | flat; ~~cheaper than `deepseek-v4-pro` on both sides~~ **withdrawn — see CN sheet** |
| `glm-5.1` | 1.40 | 4.40 | 0.26 | flat; ~~dominated by `glm-5.2`~~ **withdrawn — CN tiers it, cheaper below 32k** |
| `glm-5` | 0.573 | 2.58 | 0.115 | ⚠️ **MAINLAND** — no INTL price exists; tiered at 32k, tier 2 = 0.86 / 3.154 |
| `MiniMax-M2.5` | 0.304 | 1.213 | 0.061 | ⚠️ **MAINLAND** — no INTL price exists |

## Spec summary

| Model | Max input | Max output | Context | RPM | TPM |
|---|---:|---:|---:|---:|---:|
| `deepseek-v4-pro` | 1M | 384K | 1M | 10,000 | 1,200,000 |
| `deepseek-v4-flash` | 1M | 384K | 1M | 10,000 | 1,200,000 |
| `qwen3.7-max` | — | 64K | 1M | **600** | 1,000,000 |
| `qwen3.7-plus` | — | 64K | 1M | 15,000 | 5,000,000 |
| `qwen3.6-plus` | — | 64K | 1M | 15,000 | 5,000,000 |
| `qwen3.6-flash` | 991K | 64K | 1M | 15,000 | 5,000,000 |
| `deepseek-v3.2` | 96K | 64K | 128K | 10,000 | 1,200,000 |
| `kimi-k2.7-code` | 224K | **16K** | 256K | **500** | 1,000,000 |
| `glm-5.2` | 1M | 128K | 1M | **500** | 1,000,000 |
| `glm-5.1` | 202K | 128K | 202K | **500** | 1,000,000 |
| `MiniMax-M2.5` | 192K | 128K | 200K | **500** | 1,000,000 |
| `kimi-k2.6` | 224K | 16K | 256K | **500** | 1,000,000 |
| `glm-5` | 166K | 16K | 198K | **500** | 1,000,000 |
| `kimi-k2.5` | 224K | 16K | 256K | **500** | 1,000,000 |

The Qwen comparison view shows context + max output but no separate "maximum
input" row. `qwen3.7-max`'s **600 RPM / 1M TPM** is a 25x / 5x lower ceiling than
its Plus siblings and is a real constraint for agent workloads, not a footnote.

---

## `deepseek-v4-pro`

**Captured:** 2026-07-16 · **Vendor:** DeepSeek

### Price (USD per 1M tokens)
| Component | Rate |
|---|---:|
| Input | $2.40 |
| Input (implicit cache) | $0.20 |
| Output | $4.80 |

Implicit cache at 12x discount off input. No explicit cache-write charge shown.

### Overview
Tags: `Text Generation`, `Deep Thinking`

> A flagship MoE large model with 1.6 trillion parameters and 49 billion
> activated parameters, natively supporting context lengths of up to one million
> tokens. Trained on a vast corpus of high-quality data, it excels in advanced
> mathematical reasoning, complex logical inference, specialized coding, and deep
> analysis of long-form text, making it well-suited for demanding applications
> such as cutting-edge research, sophisticated office workflows, and advanced AI
> agents.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

(Console shows image / video / audio icons greyed out on both sides.)

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✓ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 1M |
| Maximum Output | 384K |
| Context Window | 1M |
| RPM | 10,000 |
| TPM | 1,200,000 |

### Access
- OpenAI-compatible base URL (workspace-scoped): `https://ws-<your-workspace-id>.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- Auth env: `DASHSCOPE_API_KEY` (Model Studio key, **not** the `sk-sp-` token-plan key)
- DashScope surface also offered.

### ⚠️ Discrepancies vs our shipped metadata
- **Structured output:** console says **✗**; our internal model-metadata reference §4 and the
  models.dev entry both carry **✓** for `deepseek-v4-pro`. One of the two is
  wrong and it affects the upstream PRs. Worth an API probe before the next
  models.dev change.
- **Web search ✓** on the console. our internal model-metadata reference states built-in
  model tools are Qwen-only and Responses-API-only. This flag may refer to a
  Model Studio feature that is not exposed on the token-plan gateway — do not
  assume parity.
- Max input / max output / context all match models.dev (1M / 384K / 1M). Good.

---

## `deepseek-v4-flash`

**Captured:** 2026-07-16 · **Vendor:** DeepSeek

### Price (USD per 1M tokens)
| Component | Rate |
|---|---:|
| Input | $0.20 |
| Input (implicit cache) | $0.04 |
| Output | $0.40 |

Exactly **12x cheaper than `deepseek-v4-pro`** on both input and output. Implicit
cache is 5x off input here, vs 12x on v4-pro.

### Overview
Tags: `Text Generation`, `Deep Thinking`

> A highly efficient, lightweight MoE model with 284 billion parameters in total
> and 13 billion activated parameters, natively supporting context windows of up
> to one million tokens. It offers fast inference speed, low latency, and
> cost-effective invocation, delivering well-balanced overall performance.
> Designed for high-concurrency, lightweight workloads, it is ideally suited for
> common, essential use cases such as everyday dialogue, content creation, basic
> RAG applications, and batch text processing.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
Identical to `deepseek-v4-pro`.

| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✓ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
Identical to `deepseek-v4-pro`.

| | |
|---|---:|
| Maximum Input | 1M |
| Maximum Output | 384K |
| Context Window | 1M |
| RPM | 10,000 |
| TPM | 1,200,000 |

### ⚠️ Discrepancies vs our shipped metadata
- **Structured output:** console **✗**, models.dev **✓**. Same conflict as
  `deepseek-v4-pro` — the two DeepSeek V4 entries share it.
- Limits match models.dev (1M / 384K / 1M).

---

## Qwen models (`qwen3.7-plus`, `qwen3.7-max`, `qwen3.6-plus`)

**Captured:** 2026-07-16 · **Vendor:** Qwen · **Source:** console side-by-side
compare view (not the individual details pages, so the capability matrix —
playground / function calling / structured output / web search / batches /
fine-tuning — is **not shown** for these three and is still outstanding).

All three: **context 1M, max output 64K.**

### `qwen3.7-plus`
**Upgraded to full details-page capture 2026-07-16** — see the dedicated
`qwen3.7-plus` section below. Pricing from the compare view was confirmed exact.

### `qwen3.7-max`
**Upgraded to full details-page capture 2026-07-16** — see the dedicated
`qwen3.7-max` section below. Pricing from the compare view was confirmed exact.

### `qwen3.6-plus`
**Upgraded to full details-page capture 2026-07-16** — see the dedicated
`qwen3.6-plus` section below. Pricing from the compare view was confirmed exact.

---

*All four Qwen models now have full details-page captures. This compare-view
section is retained only as the record of where the pricing was first read.*

---

## `qwen3.6-flash`

**Captured:** 2026-07-16 · **Vendor:** Qwen · **Source:** own details page (full)

### Price (USD per 1M tokens) — tiered, no discount
| Component | Tier 1 (`input<=256k`) | Tier 2 (`256k<input<=1m`) |
|---|---:|---:|
| Input | $0.25 | $1.00 |
| Output | $1.50 | $4.00 |
| Explicit cache creation | $0.3125 | $1.25 |
| Explicit cache read | $0.025 | $0.10 |

No implicit-cache row (explicit cache only), same as `qwen3.6-plus`.

### Overview
Tags: `Qwen3.6`, `Text Generation`, `Visual Understanding`, `Deep Thinking`

> The Qwen3.6 native vision-language Flash model series delivers a significant
> performance boost over the 3.5-Flash version. This model particularly excels in
> agentic coding capabilities, substantially outperforming its predecessor on
> multiple code-agent benchmarks, as well as in mathematical and code reasoning.
> In terms of vision, it features markedly improved spatial intelligence, with
> especially notable enhancements in object localization and object detection.

### Modalities
| | Supported |
|---|---|
| Input | **Image, Text, Video** (labelled explicitly on this page) |
| Output | Text |

Matches our internal model-metadata reference (text, image, video). ✓

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| **Structured Output** | **✓** |
| Web Search | ✓ |
| **Prefix Continuation** | **✓** |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

The only model captured so far with **structured output** or **prefix
continuation**. Both match models.dev, which also flags `qwen3.6-flash` as the
one Qwen with `attachment` + `structured_output`. ✓

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 991K |
| Maximum Output | 64K |
| **Max Input (Thinking Mode)** | **983K** |
| **Maximum Output (Thinking Mode)** | 64K |
| Context Window | 1M |
| RPM | 15,000 |
| TPM | 5,000,000 |

First model to expose separate **thinking-mode** limits. Max input drops 991K →
983K when thinking is on (reasoning tokens eat the window). Output cap unchanged.

### 🆕 Tool Calling Price (Responses API) — per 1K calls
| Tool | Price |
|---|---|
| `web_search` | **$10** / 1K calls |
| `t2i_search` | $8 / 1K calls |
| `i2i_search` | $8 / 1K calls |
| `web_extractor` | **Limited Time Free** |
| `code_interpreter` | **Limited Time Free** |

All tagged `Responses API`, confirming our internal model-metadata reference §4's
Responses-only finding.

**⚠️ This corrects the reference doc.** It currently says of the built-in tools:
"No extra charge: tool token usage is deducted from the plan credits like any
other call." That is only true for `web_extractor` and `code_interpreter`, and
only while the limited-time free period lasts. `web_search` costs **$0.01 per
call** on top of tokens, and the two image searches $0.008 each. At agent scale
that is not noise: 10k searches = $100. The reference doc's own note ("Per-tool
pricing: console model-details page") pointed here — this is that page.

Tool pricing is **identical on `qwen3.7-plus`**, so it looks like a flat
per-tool rate across the Qwen models rather than a per-model one.

---

## `qwen3.7-plus`

**Captured:** 2026-07-16 · **Vendor:** Qwen · **Source:** own details page (full)
· ⭐ token-plan default model

Functionally equivalent to snapshot `qwen3.7-plus-2026-05-26`.

### Price (USD per 1M tokens) — tiered, limited-time 20% off
Confirms the compare-view capture exactly.

| Component | Tier 1 (`input<=256k`) orig | Tier 1 effective | Tier 2 (`256k<input<=1m`) orig | Tier 2 effective |
|---|---:|---:|---:|---:|
| Input | $0.40 | $0.32 | $1.20 | $0.96 |
| Output | $1.60 | $1.28 | $4.80 | $3.84 |
| Input (implicit cache) | $0.08 | $0.064 | $0.24 | $0.192 |
| Explicit cache creation | $0.50 | $0.40 | $1.50 | $1.20 |
| Explicit cache read | $0.04 | $0.032 | $0.12 | $0.096 |

The only Qwen so far with **both** implicit and explicit cache.

### Overview
Tags: `Qwen3.7`, `Deep Thinking`, `Text Generation`, `Visual Understanding`

> Among the Qwen3.7 series, the cost-effective Plus model builds on its robust
> text capabilities while delivering a comprehensive upgrade to its
> vision-language abilities, all while preserving its full-stack agent-level
> intelligence for coding, tool use, and productivity workflows. Its key
> distinguishing feature is multi-modal interactive hybrid agent capabilities,
> enabling it to perceive real-world scenes, read screens and interact with GUIs,
> generate code based on visual references, and perform end-to-end navigation
> within mobile apps.

### Modalities
| | Supported |
|---|---|
| Input | **Image, Text, Video** (labelled explicitly) |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| **Structured Output** | **✓** |
| Web Search | ✓ |
| **Prefix Continuation** | **✓** |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 991K |
| Maximum Output | 64K |
| Max Input (Thinking Mode) | 983K |
| Maximum Output (Thinking Mode) | 64K |
| **Maximum Chain-of-Thought** | **256K** |
| Context Window | 1M |
| RPM | 15,000 |
| TPM | 5,000,000 |

First model to expose a **Maximum Chain-of-Thought** ceiling (256K) — a cap on
reasoning tokens per call, distinct from the output cap.

### Tool Calling Price (Responses API) — per 1K calls
Identical to `qwen3.6-flash`: `web_search` $10, `t2i_search` $8, `i2i_search` $8,
`web_extractor` Limited Time Free, `code_interpreter` Limited Time Free.

### ⚠️ Discrepancies vs our shipped metadata
Two errors in our internal model-metadata reference §4 for this model, both now confirmed
against its own details page:

- **Video input.** Reference says `text, image`. Console says **image, text,
  video**, labelled in words not icons. The reference is wrong.
- **Structured output.** Reference says **✗**. Console says **✓**.

Both feed the models.dev entry. Worth an API probe before the next PR, since
`qwen3.7-plus` is the token-plan default and the most-used model in the set.

---

## `qwen3.7-max`

**Captured:** 2026-07-16 · **Vendor:** Qwen · **Source:** own details page (full)

Functionally equivalent to snapshot `qwen3.7-max-2026-05-20`.

### Price (USD per 1M tokens) — flat, limited-time 50% off
No `Tiered Pricing` control on this page, confirming Max is **not** input-tiered
(unlike every other Qwen). Compare-view capture confirmed exact.

| Component | Original | Effective (50% off) |
|---|---:|---:|
| Input | $2.50 | $1.25 |
| Output | $7.50 | $3.75 |
| Input (implicit cache) | $0.50 | $0.25 |
| Explicit cache creation | $3.125 | $1.5625 |
| Explicit cache read | $0.25 | $0.125 |

### Overview
Tags: `Qwen3.7`, `Deep Thinking`, `Text Generation`

> The Max model, the largest and most capable in the Qwen3.7 series, currently
> offers a pure-text-only interface for public experimentation. Qwen3.7 is a
> next-generation flagship model designed for the agent-centric era, with its
> core strengths lying in the breadth and depth of its agent-level capabilities:
> it excels at programming, office and productivity tasks, and long-term
> autonomous execution.

"Currently offers a pure-text-only interface **for public experimentation**"
reads like the text-only limit is a staging decision, not a model limit. Worth
re-checking on drift passes.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✓ |
| Prefix Continuation | ✓ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 991K |
| Maximum Output | 64K |
| Max Input (Thinking Mode) | 983K |
| Maximum Output (Thinking Mode) | 64K |
| Context Window | 1M |
| **RPM** | **600** |
| **TPM** | **1,000,000** |

No Maximum Chain-of-Thought row (unlike `qwen3.7-plus`). The **600 RPM / 1M TPM**
ceiling is 25x / 5x below its Plus siblings and is the model's defining practical
constraint.

### Tool Calling Price (Responses API) — per 1K calls
| Tool | Price |
|---|---|
| `web_search` | $10 / 1K calls |
| `web_extractor` | Limited Time Free |
| `code_interpreter` | Limited Time Free |

**Only three tools**, vs five on `qwen3.7-plus` / `qwen3.6-flash`. The two image
searches (`t2i_search`, `i2i_search`) are absent, consistent with a text-only
model. So the per-tool rate is flat across Qwen, but *which* tools exist is not.

### ✅ Consistent with our shipped metadata
No discrepancies. Text-only modality and structured output **✗** both match
our internal model-metadata reference §4.

---

## `qwen3.6-plus`

**Captured:** 2026-07-16 · **Vendor:** Qwen · **Source:** own details page (full)

Functionally equivalent to snapshot `qwen3.6-plus-2026-04-02`.

### Price (USD per 1M tokens) — tiered, no discount
No implicit-cache row (explicit cache only). Compare-view capture confirmed exact.

| Component | Tier 1 (`input<=256k`) | Tier 2 (`256k<input<=1m`) |
|---|---:|---:|
| Input | $0.50 | $2.00 |
| Output | $3.00 | $6.00 |
| Explicit cache creation | $0.625 | $2.50 |
| Explicit cache read | $0.05 | $0.20 |

### Overview
Tags: `Qwen3.6`, `Deep Thinking`, `Visual Understanding`, `Text Generation`

> The Qwen3.6 native vision-language Plus series models demonstrate exceptional
> performance on par with the current state-of-the-art models, with a significant
> improvement in overall results compared to the 3.5 series. The models have been
> markedly enhanced in code-related capabilities such as agentic coding,
> front-end programming, and Vibe coding, as well as in multi-modal general
> object recognition, OCR, and object localization.

### Modalities
| | Supported |
|---|---|
| Input | **Image, Text, Video** (labelled explicitly) |
| Output | Text |

Matches our internal model-metadata reference. ✓

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| **Structured Output** | **✓** |
| Web Search | ✓ |
| Prefix Continuation | ✓ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 991K |
| Maximum Output | 64K |
| Max Input (Thinking Mode) | 983K |
| Maximum Output (Thinking Mode) | 64K |
| Context Window | 1M |
| RPM | 15,000 |
| TPM | 5,000,000 |

No Maximum Chain-of-Thought row — that field remains `qwen3.7-plus`-only.

### Tool Calling Price (Responses API) — per 1K calls
All five: `web_search` $10, `t2i_search` $8, `i2i_search` $8, `web_extractor`
Limited Time Free, `code_interpreter` Limited Time Free.

### ⚠️ Discrepancy vs our shipped metadata
- **Structured output:** console **✓**, our internal model-metadata reference **✗**.
  Same direction as `qwen3.7-plus`.

---

## `deepseek-v3.2`

**Captured:** 2026-07-16 · **Vendor:** DeepSeek · **Source:** own details page (full)

### 🚨 Retirement notice
The console tags this model **"will be retired on Oct 10"** (2026 assumed).
It is the only model in the set carrying a retirement tag. Implications:

- It should be **dropped from the token-plan catalogs** on/before that date —
  models.dev `alibaba-token-plan` + `-cn`, openclaw `QWEN_TOKEN_PLAN_MODEL_CATALOG`,
  hermes `_PROVIDER_MODELS`. This is a scheduled maintenance action, not a drift
  find, and none of the three downstreams currently know about it.
- Do not recommend it to clients or build course material on it.
- Confirm the exact date and year in the console tooltip before acting.

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $0.57 |
| Input (implicit cache) | $0.114 |
| Output | $1.71 |
| Explicit cache creation | $0.713 |
| Explicit cache read | $0.057 |

The only DeepSeek with **explicit** cache as well as implicit, and the only model
in the set with non-round pricing (0.57 / 1.71 — a 3x input:output ratio, and
the numbers look like a currency conversion rather than a set price).

### Overview
Tags: `Deep Thinking`, `Text Generation`, `will be retired on Oct 10`

> DeepSeek-V3.2 is the official release of a model that incorporates DeepSeek
> Sparse Attention, a sparse attention mechanism. It's also the first model
> launched by DeepSeek that integrates reasoning into tool usage, supporting both
> reasoning-enabled and non-reasoning tool calls.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✓ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

Identical to the two DeepSeek V4 models.

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 96K |
| Maximum Output | 64K |
| Context Window | 128K |
| RPM | 10,000 |
| TPM | 1,200,000 |

Max input (96K) + max output (64K) exceed the 128K context window, so the two
caps cannot both be maxed in one call. No thinking-mode rows.

### ⚠️ Discrepancy vs our shipped metadata
- **Structured output:** console **✗**, reference **✓**. Third DeepSeek with the
  same conflict in the same direction — so all three DeepSeek entries are
  affected, which points at a per-vendor error rather than per-model.
- Context (128K = 131,072) and max output (64K = 65,536) both match models.dev. ✓

---

## `kimi-k2.7-code`

**Captured:** 2026-07-16 · **Vendor:** Moonshot · **Source:** own details page (full)

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $0.95 |
| Input (implicit cache) | $0.19 |
| Output | $4.00 |

No explicit-cache rows. A 4.2x input:output ratio, the widest of any flat-priced
model captured.

### Overview
Tags: `Text Generation`, `Visual Understanding`, `Deep Thinking`

> kimi-k2.7-code is Kimi's most intelligent coding model to date. It follows
> instructions more reliably over long contexts and completes programming tasks
> with higher success rates. It supports text, image, and video inputs, along
> with thinking mode, conversation, and agent tasks.

### Modalities
| | Supported |
|---|---|
| Input | **Text, Image, Video** (labelled explicitly) |
| Output | Text |

Matches our internal model-metadata reference. ✓

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| **Structured Output** | **✓** |
| Web Search | ✓ |
| Prefix Continuation | ✓ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

No Tool Calling Price section — consistent with the built-in tools being
Qwen-only.

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 224K |
| **Maximum Output** | **16K** |
| Context Window | 256K |
| **RPM** | **500** |
| TPM | 1,000,000 |

**500 RPM is the lowest ceiling in the set so far** — below even `qwen3.7-max`'s
600. For a model sold on agentic coding, that is a serious practical limit.

### 🚨 Discrepancies vs our shipped metadata — this model is the worst offender

**1. Max output: console 16K vs our shipped 262,144. A 16x error, and ours is
the one that looks wrong.**

our internal model-metadata reference §4 records `kimi-k2.7-code` max output as **262,144**
and calls it "**API-confirmed** via `max_tokens` error", citing the gateway
response `Range of max_tokens should be [1, 262144]`. The models.dev entry
deliberately **omits** the output cap so it inherits the base model's 262,144
(see the TOML in §6).

The console says **16K**, which is exactly `kimi-k2.6`'s documented cap (16,384).

The probable cause is a **flawed inference**: `262144` is also this model's
**context window** (256K). An error saying `max_tokens` must be within
`[1, 262144]` is most likely the gateway range-checking `max_tokens` against the
context window, **not** reporting the model's real output ceiling. The probe
proved an upper bound on the parameter, and it was read as the output cap.

This matters because it shipped: the models.dev TOML's omission of `output` is
load-bearing, and openclaw's catalog carries `maxTokens`.

**Re-probe properly** by requesting a real generation (not just validating the
param): ask for `max_tokens: 100000` and see whether it errors, truncates at 16K,
or actually produces more than 16K of output. The validation error alone cannot
distinguish these.

**2. Structured output:** console **✓**, reference **✗**. The reference's
footnote 1 explains the ✗ as deliberate ("base model declares
`structured_output`, but the Token Plan entry omits it, mirroring the
`kimi-k2.6` sibling") and models.dev ships `base_model_omit =
["structured_output"]`. The console contradicts that, and the base model agrees
with the console. The mirroring of `kimi-k2.6` may have been the wrong call.

**3. Context ✓** — console 256K = 262,144, matches.

---

## `glm-5.2`

**Captured:** 2026-07-16 · **Vendor:** Zhipu · **Source:** own details page (full)

**⭐ The intelligence leader of the token plan** (AA Intelligence Index 51.1, the
highest of any token-plan model) — and cheaper than `deepseek-v4-pro` on both
input and output.

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $1.40 |
| Input (implicit cache) | $0.28 |
| Output | $4.40 |

No explicit-cache rows.

### Overview
Tags: `Text Generation`, `Deep Thinking`

> GLM-5.2 is the latest flagship model from Zhipu AI, designed for long-horizon
> tasks with support for an ultra-long 1M context window. It features powerful
> logical reasoning, long-text comprehension, and code generation capabilities,
> balancing performance with inference efficiency. It excels across multi-task
> benchmarks and is well-suited for intelligent interaction, enterprise
> applications, and development assistance scenarios.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✓ |
| Web Search | ✓ |
| Prefix Continuation | ✓ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 1M |
| Maximum Output | 128K |
| Max Input (Thinking Mode) | 1M |
| Maximum Output (Thinking Mode) | 128K |
| Maximum Chain-of-Thought | 128K |
| Context Window | 1M |
| **RPM** | **500** |
| TPM | 1,000,000 |

Only the second model with a Maximum Chain-of-Thought row (after `qwen3.7-plus`),
and the only one whose thinking-mode input is **not** reduced (stays 1M).
**500 RPM** is a hard constraint for agent loops.

### ✅ Consistent with our shipped metadata
Context (1M), max output (128K = 131,072), text-only modality and structured
output ✓ all match our internal model-metadata reference. No discrepancies.

---

## `glm-5.1`

**Captured:** 2026-07-16 · **Vendor:** Zhipu · **Source:** own details page (full)

### 🚩 Strictly dominated by `glm-5.2` — same price, worse on everything
| | `glm-5.1` | `glm-5.2` |
|---|---:|---:|
| Input / Output | **$1.40 / $4.40** | **$1.40 / $4.40** (identical) |
| Implicit cache | $0.26 | $0.28 |
| AA Intelligence | 40.2 | **51.1** |
| Context | 202K | **1M** |
| Web Search | ✗ | ✓ |
| Prefix Continuation | ✗ | ✓ |

Identical headline pricing, 11 points less intelligence, a fifth of the context,
and two fewer capabilities. `glm-5.1` is marginally cheaper on cached input only.
**There is no workload where it is the right pick over `glm-5.2`.**

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $1.40 |
| Input (implicit cache) | $0.26 |
| Output | $4.40 |

### Overview
Tags: `Text Generation`, `Deep Thinking`

> GLM-5.1 is a model developed by Zhipu AI, specifically designed for
> long-horizon tasks. It has 744 billion parameters, supports an ultra-long
> context of 200k tokens, and can generate up to 128k tokens in a single
> response. GLM-5.1 excels in logical reasoning, long-text understanding, and
> code generation, while balancing performance with inference efficiency. It
> delivers outstanding results across multiple multi-task benchmarks and is
> well-suited for applications such as intelligent human-computer interaction,
> enterprise solutions, and developer assistance.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✓ |
| **Web Search** | **✗** |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

**First model in the set with Web Search ✗.**

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 202K |
| Maximum Output | 128K |
| **Max Input (Thinking Mode)** | **166K** |
| Maximum Output (Thinking Mode) | 128K |
| Context Window | 202K |
| **RPM** | **500** |
| TPM | 1,000,000 |

Biggest thinking-mode penalty seen so far: max input drops **202K → 166K** (an
18% cut, vs 1% on the Qwens and 0% on `glm-5.2`).

### ✅ Consistent with our shipped metadata
Context (202K = 202,752), max output (128K = 128,000), text-only and structured
output ✓ all match our internal model-metadata reference. No discrepancies.

---

## `MiniMax-M2.5`

**Captured:** 2026-07-16 · **Vendor:** MiniMax · **Source:** own details page (full)

### 🚩 Dominated by `deepseek-v4-flash`
| | `MiniMax-M2.5` | `deepseek-v4-flash` |
|---|---:|---:|
| Input / Output | $0.304 / $1.213 | **$0.20 / $0.40** |
| AA Intelligence | 33.7 | **40.3** |
| Context | 200K | **1M** |

Cheaper, smarter and 5x the context. `MiniMax-M2.5` is the **lowest-intelligence
model in the token plan** (AA 33.7) and is not the cheapest, so it has no niche.

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $0.304 |
| Input (implicit cache) | $0.061 |
| Output | $1.213 |

Non-round figures like `deepseek-v3.2`'s, again suggesting conversion from RMB
rather than a USD-set price. No explicit-cache rows.

### Overview
Tags: `Deep Thinking`, `Text Generation`

> MiniMax-M2.5 is the flagship open-source large model from MiniMax. Trained
> through large-scale reinforcement learning in hundreds of thousands of
> real-world, complex environments, M2.5 has achieved or set new
> state-of-the-art (SOTA) performance in productivity scenarios such as
> programming, tool invocation and search, and office work.

The only **open-weights** model in the token plan, which is its one genuine
differentiator (portability off the plan) — not something the cost chart shows.

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| **Web Search** | **✗** |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

Tied with `glm-5.1` as the most capability-poor model in the set: only playground,
function calling and cache. Second model with Web Search ✗.

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 192K |
| **Maximum Output** | **128K** |
| Context Window | 200K |
| **RPM** | **500** |
| TPM | 1,000,000 |

No thinking-mode rows despite the `Deep Thinking` tag.

### ⚠️ Discrepancies vs our shipped metadata
- **Max output: console 128K vs reference 24,576 (24K). A 5.2x gap.** Opposite
  direction to the `kimi-k2.7-code` error (where ours was too high). Needs an API
  probe; if the console is right, our shipped `output` limit is badly
  under-reported in models.dev, openclaw and hermes.
- **Context:** console shows Max Input **192K** and Context Window **200K**;
  reference says 196,608 (= exactly 192Ki). The console appears to use 192K for
  the input cap and a rounded 200K for the window, so ours may be conflating the
  two. Low-stakes, but worth resolving while probing the output cap.
- **Structured output ✗** matches. ✓

---

## `kimi-k2.6`

**Captured:** 2026-07-16 · **Vendor:** Moonshot · **Source:** own details page (full)

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $0.8939 |
| Input (implicit cache) | $0.1788 |
| Output | $3.7131 |
| Explicit cache creation | $1.1174 |
| Explicit cache read | $0.0894 |

Non-round again (RMB conversion). Unlike `kimi-k2.7-code`, this one **does** have
explicit-cache rows.

### 🚩 Cheaper *and* smarter than `kimi-k2.7-code`
| | `kimi-k2.6` | `kimi-k2.7-code` |
|---|---:|---:|
| Input / Output | **$0.894 / $3.713** | $0.95 / $4.00 |
| AA Intelligence | **42.8** | 41.9 |
| Structured output / Web search / Prefix | ✗ / ✗ / ✗ | **✓ / ✓ / ✓** |
| Explicit cache | **✓** | ✗ |

Not strict dominance: the newer `k2.7-code` is worse on price *and* AA
intelligence, but wins on three capability flags. So the choice is genuinely
capability-driven, not quality-driven — `k2.7-code` only earns its price if you
need structured output or web search.

### Overview
Tags: `Deep Thinking`, `Visual Understanding`, `Text Generation`

> kimi-k2.6 is Kimi's latest and most intelligent model, featuring enhanced and
> more stable long-context code-generation capabilities. It boasts significantly
> improved instruction following and self-correction abilities, while also
> supporting text, image, and video inputs, as well as both reasoning and
> non-reasoning modes for dialogue and Agent-based tasks.

### Modalities
| | Supported |
|---|---|
| Input | Text, Image, Video |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✗ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 224K |
| **Maximum Output** | **16K** |
| Context Window | 256K |
| RPM | **500** |
| TPM | 1,000,000 |

### ✅ Consistent with our shipped metadata — and it corroborates the k2.7 error
Context (256K = 262,144), max output (**16K** = 16,384), modalities and
structured output ✗ all match our internal model-metadata reference. No discrepancies.

**This strengthens the `kimi-k2.7-code` max-output finding.** `kimi-k2.6` has
identical max input (224K), context (256K), RPM and TPM, and a **16K** output cap
that both we and the console agree on. `kimi-k2.7-code` shares every one of those
limits — so a 16K output cap on it is exactly what the sibling pattern predicts,
and 262,144 is the outlier. The `max_tokens` probe almost certainly measured the
context window, not the output ceiling.

---

## `glm-5`

**Captured:** 2026-07-16 · **Vendor:** Zhipu · **Source:** own details page
(⚠️ **partial** — only the `input<=32k` tier captured)

### Price (USD per 1M tokens) — tiered at **32k**, no discount
| Component | Tier 1 (`input<=32k`) | Tier 2 (`32k<input<=200k`) |
|---|---:|---:|
| Input | $0.573 | $0.86 |
| Input (implicit cache) | $0.115 | $0.172 |
| Output | $2.58 | $3.154 |

Two tiers only — tier 2's ceiling (200k) is the full context window, so there is
nothing above it.

**⚠️ A different tiering threshold from every other model.** The Qwens tier at
**256k**; `glm-5` tiers at **32k**. Its tier 1 therefore covers a far narrower
band of real usage, so a `glm-5` tier-1 price is **not** comparable to a Qwen
tier-1 price: at 50k input, the Qwens are still on tier 1 while `glm-5` has
already stepped up to $0.86 / $3.154. Any chart must resolve the tier from an
assumed input size per model, not by taking "tier 1" for everyone.

The escalation is mild though (+50% input, +22% output), unlike the Qwens' tier-2
jump (+200% / +200%). So `glm-5` stays cheap across its whole range.

### 🚩 Makes `glm-5.1` look indefensible
`glm-5` and `glm-5.2` are flat-priced; only `glm-5` is tiered, so the comparison
holds at both of its tiers:

| | `glm-5` T1 (<=32k) | `glm-5` T2 (32k-200k) | `glm-5.1` | `glm-5.2` |
|---|---:|---:|---:|---:|
| Input / Output | $0.573 / $2.58 | $0.86 / $3.154 | $1.40 / $4.40 | $1.40 / $4.40 |
| AA Intelligence | 39.5 | 39.5 | 40.2 | **51.1** |

Even at `glm-5`'s **most expensive** tier, `glm-5.1` costs **63% more input /
40% more output** for **0.7** more intelligence points — and the same price as
`glm-5.2` for 11 fewer. There is no input size at which `glm-5.1` makes sense.

### Overview
Tags: `Text Generation`, `Deep Thinking`

> GLM-5 is a next-generation large model designed for coding and agent
> applications, achieving state-of-the-art open-source performance in complex
> systems engineering and long-horizon tasks, with a real-world programming
> experience approaching the level of Claude Opus. Built on a new 744B foundation
> model, asynchronous reinforcement learning, and sparse attention, it delivers a
> comprehensive upgrade from "writing code" to "writing full-fledged software
> systems."

### Modalities
| | Supported |
|---|---|
| Input | Text |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✗ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 166K |
| Maximum Output | 16K |
| Max Input (Thinking Mode) | 166K |
| Maximum Output (Thinking Mode) | 16K |
| **Maximum Chain-of-Thought** | **32K** |
| Context Window | 198K |
| RPM | **500** |
| TPM | 1,000,000 |

Third model with a Maximum Chain-of-Thought row (32K, the smallest seen).

### ✅ Consistent with our shipped metadata
Context (198K = 202,752), max output (16K = 16,384), text-only and structured
output ✗ all match our internal model-metadata reference. No discrepancies.

---

## `kimi-k2.5`

**Captured:** 2026-07-16 · **Vendor:** Moonshot · **Source:** own details page (full)

### Price (USD per 1M tokens) — flat, no discount
| Component | Rate |
|---|---:|
| Input | $0.574 |
| Input (implicit cache) | $0.115 |
| Output | $3.011 |
| Explicit cache creation | $0.718 |
| Explicit cache read | $0.057 |

Cheapest Kimi. The `k2.5` → `k2.6` step costs +56% input / +23% output for +4.7
AA intelligence points (38.1 → 42.8), which is a defensible trade, unlike the
`k2.6` → `k2.7-code` step.

### Overview
Tags: `Deep Thinking`, `Visual Understanding`, `Text Generation`

> The kimi-k2.5 model is Moonshot AI's most versatile model to date, featuring a
> native multimodal architecture that supports both visual and text inputs, as
> well as both reasoning and non-reasoning modes, and can handle both dialogue
> and Agent tasks.

### Modalities
| | Supported |
|---|---|
| Input | Text, Image, Video |
| Output | Text |

### Capabilities
| Capability | |
|---|:--:|
| Playground | ✓ |
| Function calling | ✓ |
| Structured Output | ✗ |
| Web Search | ✗ |
| Prefix Continuation | ✗ |
| Cache | ✓ |
| Batches | ✗ |
| Model Fine-tuning | ✗ |

Identical to `kimi-k2.6`.

### Rate Limit & Context
| | |
|---|---:|
| Maximum Input | 224K |
| **Maximum Output** | **16K** |
| Context Window | 256K |
| RPM | **500** |
| TPM | 1,000,000 |

### ⚠️ Discrepancy vs our shipped metadata
- **Max output: console 16K vs reference 32,768 (32K). 2x.**

---

## 🚨 Cross-model finding: the Kimi max-output column is wrong across the board

With all three Kimis captured, the pattern is unambiguous. **Every Kimi model has
identical limits on the console** — max input 224K, context 256K, max output
**16K**, 500 RPM, 1M TPM — yet our reference doc gives each a different output cap:

| Model | Reference doc | Console | Verdict |
|---|---:|---:|---|
| `kimi-k2.7-code` | 262,144 | **16K** | ours 16x too high |
| `kimi-k2.6` | 16,384 | **16K** | ✅ correct |
| `kimi-k2.5` | 32,768 | **16K** | ours 2x too high |

Two of three are wrong, and the one that is right is the one the console agrees
with. The console shows a **uniform 16K output cap across the whole Kimi family**,
which is far more plausible than three different caps on three models that are
otherwise identical in every limit.

This also closes the `kimi-k2.7-code` question raised above. Its 262,144 came
from reading `Range of max_tokens should be [1, 262144]` as the output ceiling —
but 262,144 is exactly the **context window** shared by all three Kimis, and
`kimi-k2.6` proves a model with that same 262,144 context has a 16K output cap.
The probe measured the parameter's validation range against context, not the
output limit.

**Action:** re-probe with a real generation (request `max_tokens: 100000` and see
whether it truncates at ~16K), then fix `output` for `kimi-k2.7-code` and
`kimi-k2.5` in models.dev, openclaw (`maxTokens`) and the reference doc.
