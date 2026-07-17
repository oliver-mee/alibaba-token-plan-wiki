---
title: Model Studio per-model pricing — CHINESE MAINLAND (the Token Plan's billing basis)
region: chinese-mainland
source: Model Studio console, per-model details page, "Chinese Mainland" toggle
source_type: console UI (JS-rendered, not in public docs; captured by screenshot)
pricing_basis: Chinese Mainland pay-as-you-go, USD per 1M tokens
relation_to_token_plan: >
  THIS IS THE SHEET THE TOKEN PLAN METERS AGAINST. Proved by measurement
  2026-07-16 (credit-rate-experiment.md): fitting observed credit charges against
  this sheet makes credits-per-dollar constant across models to within 0.4%; the
  International sheet gives a 13-27% spread and therefore is not the basis.
  The plan serves inference from Singapore (ap-southeast-1) but bills at mainland
  rates — inference region and billing basis are decoupled.
approx_constant: ~745 credits per USD (provisional; from input-dominated readings)
purpose: the costing basis for model-value.html and any credit-burn question
status: COMPLETE — all 14 chat models captured on the mainland sheet
credit_conversion: 1 credit = 0.01 CNY; credits per 1M = CNY price x 100. See credit-rate-experiment.md
updated: 2026-07-16
related: [credit-rate-experiment.md, model-studio-pricing.md, token-plan-reference (not published — internal)]
---

# Model Studio per-model pricing — Chinese Mainland

The price sheet the Token Plan actually bills against. Reached via the **Chinese
Mainland** toggle at the top of the console model-details page (the Global console
defaults to International, which is what `model-studio-pricing.md` captured and
why the error went unnoticed).

**Scope:** prices and rate limits only. Capabilities, modalities, tool pricing and
the metadata discrepancies live in `model-studio-pricing.md` and are not
re-captured here unless the mainland sheet contradicts them.

## Price summary (USD per 1M tokens)

Tiered models show tier 1 (`input<=32k`). CN/INTL = the mainland price as a
fraction of the international one (lower = cheaper on mainland).

| Model | Input | Output | Implicit cache | INTL in / out | CN/INTL in | CN/INTL out |
|---|---:|---:|---:|---|---:|---:|
| `deepseek-v4-pro` | **1.65** | **3.301** | 0.138 | 2.40 / 4.80 | 0.69 | 0.69 |
| `deepseek-v4-flash` | **0.138** | **0.275** | 0.028 | 0.20 / 0.40 | 0.69 | 0.69 |
| `deepseek-v3.2` | **0.287** | **0.431** | 0.058 | 0.57 / 1.71 | 0.50 | **0.25** |
| `qwen3.7-max` | **0.825** | **2.4755** | 0.165 | 1.25 / 3.75 | 0.66 | 0.66 |
| `qwen3.7-plus` | **0.2208** | **0.8808** | 0.0448 | 0.32 / 1.28 | 0.69 | 0.69 |
| `qwen3.6-plus` | **0.276** | **1.651** | n/a | 0.50 / 3.00 | 0.55 | 0.55 |
| `qwen3.6-flash` | **0.165** | **0.99** | n/a | 0.25 / 1.50 | 0.66 | 0.66 |
| `kimi-k2.7-code` | **0.8939** | **3.7131** | 0.1788 | 0.95 / 4.00 | 0.94 | 0.93 |
| `kimi-k2.6` | **0.8939** | **3.7131** | 0.1788 | *(none — CN only)* | — | — |
| `kimi-k2.5` | **0.574** | **3.011** | 0.115 | *(none — CN only)* | — | — |
| `glm-5.2` | **1.10** | **3.851** | 0.275 | 1.40 / 4.40 | 0.79 | **1.12** |
| `glm-5.1` T1 | **0.825** | **3.301** | 0.165 | 1.40 / 4.40 | 0.59 | 0.75 |
| `glm-5.1` T2 | **1.10** | **3.851** | 0.22 | 1.40 / 4.40 | 0.79 | 0.88 |
| `glm-5` T1 | **0.573** | **2.58** | 0.115 | 0.573 / 2.58 | **1.00** | **1.00** |
| `glm-5` T2 | **0.86** | **3.154** | 0.172 | 0.86 / 3.154 | **1.00** | **1.00** |
| `MiniMax-M2.5` | **0.304** | **1.213** | 0.061 | *(none — CN only)* | — | — |

## Rate limits — ⚠️ these differ from International too

| Model | CN RPM | CN TPM | INTL RPM | INTL TPM |
|---|---:|---:|---:|---:|
| `deepseek-v4-pro` | **15,000** | 1,200,000 | 10,000 | 1,200,000 |
| `deepseek-v4-flash` | **15,000** | 1,200,000 | 10,000 | 1,200,000 |
| `deepseek-v3.2` | **15,000** | 1,200,000 | 10,000 | 1,200,000 |
| `glm-5.2` | 500 | **2,000,000** | 500 | 1,000,000 |
| `glm-5.1` | 500 | 1,000,000 | 500 | 1,000,000 |
| `glm-5` | 500 | 1,000,000 | 500 | 1,000,000 |

**All three DeepSeek models get 15,000 RPM on mainland vs 10,000 international**,
a uniform 50% uplift — which would make DeepSeek the throughput leader on the
plan, ahead of Qwen's 15,000 (pending Qwen CN capture) and far ahead of GLM's 500.
Only `glm-5.2` gets the TPM uplift; the other GLMs are identical across sheets.

**Which set the Token Plan enforces is unknown.** It bills on the mainland sheet,
but that does not prove it inherits mainland throughput. Worth probing directly
(hammer RPM until 429). This matters for the recommendation: if `deepseek-v4-flash`
gets 15,000 RPM rather than 10,000, it beats every Qwen on throughput too.

## 🚨 Four Token Plan models do not exist on the Singapore sheet at all

Established by Oliver, 2026-07-16. The Model Studio **Singapore/International**
region does not offer these models, so they have **no international price** —
only a mainland one:

| Model | On Singapore sheet? |
|---|---|
| `glm-5` | ❌ mainland only |
| `MiniMax-M2.5` | ❌ mainland only |
| `kimi-k2.6` | ❌ mainland only |
| `kimi-k2.5` | ❌ mainland only |
| `kimi-k2.7-code` | ✅ (the only Kimi on Singapore) |
| DeepSeek ×3, Qwen ×4, `glm-5.2`, `glm-5.1` | ✅ both sheets |

**Yet the Token Plan serves all 14.** So the plan offers models that the
international region does not sell — which is a much better explanation for the
billing finding than "Alibaba picked the wrong sheet":

> **The Token Plan is a mainland product, bundled and resold internationally,
> with inference relocated to Singapore.** It bills at mainland rates because it
> *is* a mainland catalogue — a third of its models exist nowhere else. The
> mainland sheet is not an alternative view of the plan; it is the plan's native
> sheet, and the international sheet is the foreign one.

This also **retracts a false finding**: `glm-5` was recorded as "identical on both
sheets, a useful control proving the gap is a real pricing decision". It is not.
The earlier `glm-5` capture in `model-studio-pricing.md` was *already* mainland
pricing, because no international price exists to capture. Same capture, twice.
No control, no finding.

## ⚠️ The sheets are unrelated. Nothing can be derived.

For the models that **do** exist on both sheets, the CN/INTL relationship has no
pattern:

| Model | Input CN/INTL | Output CN/INTL | Relationship |
|---|---:|---:|---|
| `deepseek-v4-pro` | 0.69 | 0.69 | uniformly 31% cheaper |
| `deepseek-v4-flash` | 0.69 | 0.69 | uniformly 31% cheaper |
| `deepseek-v3.2` | 0.50 | **0.25** | far cheaper, and asymmetric |
| `glm-5.2` | 0.79 | **1.12** | cheaper in, **dearer out** |
| `glm-5.1` | 0.59 | 0.75 | cheaper, **and tiered on CN but flat on INTL** |

The DeepSeek V4 pair share a clean 0.69 multiplier; `deepseek-v3.2` does not,
despite the same vendor. `glm-5.2` is *more expensive* on mainland output.
`glm-5.1` changes pricing *structure* between sheets. **Every model must be
captured individually; none can be inferred from its sibling, its vendor, or its
international price.**

### The 12x DeepSeek ratio survives the sheet change
| | CN | INTL |
|---|---:|---:|
| `deepseek-v4-pro` / `deepseek-v4-flash`, input | 1.65 / 0.138 = **11.96** | **12.0** |
| same, output | 3.301 / 0.275 = **12.0** | **12.0** |

Both sheets price V4 Pro at exactly 12x V4 Flash. This is why the credit
measurement showed a clean 12x despite being fitted against the wrong sheet — the
ratio is sheet-invariant, so that particular test could not detect the error.
Reassuring for the headline recommendation: **V4 Flash makes credits go 12x
further, on either sheet.**

---

## `deepseek-v4-pro`

**Captured:** 2026-07-16 · **Vendor:** DeepSeek

### Price (USD per 1M tokens)
| Component | CN | (INTL for reference) |
|---|---:|---:|
| Input | **$1.65** | $2.40 |
| Input (implicit cache) | **$0.138** | $0.20 |
| Output | **$3.301** | $4.80 |

Non-round output (3.301) and cache (0.138) suggest conversion from a CNY-set
price — consistent with mainland being the primary sheet and USD the derived view.

### Rate Limit & Context
| | CN | (INTL) |
|---|---:|---:|
| Maximum Input | 1M | 1M |
| Maximum Output | 384K | 384K |
| Context Window | 1M | 1M |
| **RPM** | **15,000** | 10,000 |
| TPM | 1,200,000 | 1,200,000 |

Limits identical except RPM, which is 50% higher on mainland.

### Capabilities
Identical to the International sheet: playground ✓, function calling ✓,
structured output ✗, web search ✓, prefix continuation ✗, cache ✓, batches ✗,
fine-tuning ✗. Modalities text → text. Same overview copy.

**The structured-output ✗ is confirmed on both sheets**, strengthening the case
that our shipped `✓` is wrong for this model.

---

## `glm-5.2`

**Captured:** 2026-07-16 · **Vendor:** Zhipu

### Price (USD per 1M tokens)
| Component | CN | (INTL for reference) |
|---|---:|---:|
| Input | **$1.10** | $1.40 |
| Input (implicit cache) | **$0.275** | $0.28 |
| Output | **$3.851** | $4.40 |

Cache is 25% of input on CN vs 20% on INTL.

### Rate Limit & Context
| | CN | (INTL) |
|---|---:|---:|
| Maximum Input | 1M | 1M |
| Maximum Output | 128K | 128K |
| Max Input (Thinking Mode) | 1M | 1M |
| Maximum Output (Thinking Mode) | 128K | 128K |
| Maximum Chain-of-Thought | 128K | 128K |
| Context Window | 1M | 1M |
| RPM | 500 | 500 |
| **TPM** | **2,000,000** | 1,000,000 |

Double the mainland TPM. RPM still 500.

### Capabilities — ⚠️ one contradiction vs the International sheet
| Capability | CN | INTL |
|---|:--:|:--:|
| Playground | ✓ | ✓ |
| Function calling | ✓ | ✓ |
| Structured Output | ✓ | ✓ |
| **Web Search** | **✗** | **✓** |
| Prefix Continuation | ✗ | ✓ |
| Cache | ✓ | ✓ |
| Batches | ✗ | ✗ |
| Model Fine-tuning | ✗ | ✗ |

**Web search and prefix continuation are ✓ on International and ✗ on Chinese
Mainland for the same model.** So capability flags are region-scoped, not just
prices. Since the plan bills on the mainland sheet but runs in Singapore, which
capability set applies is genuinely unclear and should be probed, not assumed.

This weakens the note in `model-studio-pricing.md` that `glm-5.1` is dominated by
`glm-5.2` partly on web search / prefix continuation — on the mainland sheet
`glm-5.2` may not have them either.

---

---

## `deepseek-v4-flash`

**Captured:** 2026-07-16

| Component | CN | (INTL) |
|---|---:|---:|
| Input | **$0.138** | $0.20 |
| Input (implicit cache) | **$0.028** | $0.04 |
| Output | **$0.275** | $0.40 |

Uniform 0.69x, same as `deepseek-v4-pro`. Limits: 1M in / 384K out / 1M context,
**15,000 RPM** (vs 10,000 INTL), 1.2M TPM. Capabilities identical to INTL
(structured output ✗, web search ✓, prefix ✗, batches ✗).

**Cheapest model captured so far on either sheet**, and at 0.138/0.275 it is
dramatically cheaper than its AA intelligence (40.3) would suggest.

---

## `deepseek-v3.2`

**Captured:** 2026-07-16 · 🚨 still tagged **"will be retired on Oct 10"** on the
mainland sheet too.

### Price — mainland is far cheaper, and asymmetrically so
| Component | CN | (INTL) |
|---|---:|---:|
| Input | **$0.287** | $0.57 |
| Input (implicit cache) | **$0.058** | $0.114 |
| Output | **$0.431** | $1.71 |
| Explicit cache creation | **$0.359** | $0.713 |
| Explicit cache read | **$0.029** | $0.057 |

Output is **4x cheaper** on mainland (0.431 vs 1.71) while input is 2x cheaper.
The only model so far where the two directions move by different multiples in the
same direction.

### 🆕 Batch pricing — exists only on the mainland sheet
| Component | Rate |
|---|---|
| Input (Batch File) | $0.144 |
| Output (Batch File) | $0.216 |
| Input (Batch Chat) | **Limited-time 50% off** (original $0.287) |
| Output (Batch Chat) | **Limited-time 50% off** (original $0.431) |

Batch File pricing is exactly **50% of** the synchronous rate. Batch Chat is
discounted 50% as a limited-time offer, landing at the same effective price.

**Capability contradiction:** `Batches` is **✓ on mainland**, **✗ on
international** for the same model. Combined with the `glm-5.2` web-search flip,
that is two capability flags now proven region-scoped.

### Limits
96K max in / 64K max out / 128K context, **15,000 RPM** (vs 10,000 INTL), 1.2M TPM.
Structured output ✗ (matches INTL, contradicts our shipped ✓).

**Still not worth using** — retiring in under three months, and `deepseek-v4-flash`
at 0.138/0.275 is cheaper on both sides with 8x the context.

---

## `glm-5.1` — ⚠️ tiered on mainland, flat on international

**Captured:** 2026-07-16

| Component | T1 (`input<=32k`) | T2 (`32k<input<=200k`) | (INTL, flat) |
|---|---:|---:|---:|
| Input | **$0.825** | **$1.10** | $1.40 |
| Input (implicit cache) | $0.165 | $0.22 | $0.26 |
| Output | **$3.301** | **$3.851** | $4.40 |
| Explicit cache creation | $1.031 | $1.375 | — |
| Explicit cache read | $0.083 | $0.11 | — |

The pricing **structure** differs between sheets, not just the numbers: mainland
tiers at 32k (matching `glm-5`), international is flat. It also gains explicit
cache rows on mainland.

Limits: 202K in / 128K out / 202K context, 166K thinking-mode input, 500 RPM,
1M TPM — identical to INTL. Capabilities identical to INTL (structured output ✓,
web search ✗, prefix ✗).

### 🔄 REVERSAL: `glm-5.1` is no longer dominated below 32k input
On the international sheet, `glm-5.1` and `glm-5.2` were priced **identically**
($1.40/$4.40), making `glm-5.1` strictly dominated — same price, 11 fewer
intelligence points. That verdict does not survive on mainland:

| | `glm-5.1` T1 | `glm-5.1` T2 | `glm-5.2` (flat) |
|---|---:|---:|---:|
| Input / Output | **$0.825 / $3.301** | $1.10 / $3.851 | $1.10 / $3.851 |
| AA Intelligence | 40.2 | 40.2 | **51.1** |

- **Under 32k input:** `glm-5.1` is genuinely cheaper (25% off input, 14% off
  output). A real cheaper-but-dumber trade-off, **not** dominance.
- **Above 32k input:** tier 2 is **exactly** `glm-5.2`'s flat price, to the cent.
  Dominated again — same price, 11 fewer points.

So `glm-5.1` is dominated **only above 32k input**. The blanket "indefensible"
verdict in `model-studio-pricing.md` was an artefact of the wrong price sheet.

---

## `glm-5` — mainland only (no international price exists)

**Captured:** 2026-07-16 · Not offered in the Singapore region.

| Component | T1 (`input<=32k`) | T2 (`32k<input<=200k`) |
|---|---:|---:|
| Input | $0.573 | $0.86 |
| Input (implicit cache) | $0.115 | $0.172 |
| Output | $2.58 | $3.154 |

Limits: 166K in / 16K out / 198K context, 32K max CoT, 500 RPM, 1M TPM.
Capabilities: structured output ✗, web search ✗, prefix ✗, batches ✗.

**These are the same figures as the "international" capture in
`model-studio-pricing.md` because that capture was already mainland** — there is
no international `glm-5` to capture. That file's `glm-5` row is mislabelled, not
a duplicate finding. See the retraction above.

---

---

## Kimi — `kimi-k2.7-code`, `kimi-k2.6`, `kimi-k2.5`

**Captured:** 2026-07-16. `kimi-k2.7-code` is the only Kimi on the Singapore
sheet; `kimi-k2.6` and `kimi-k2.5` are mainland-only (their figures in
`model-studio-pricing.md` were already mainland, mislabelled).

### 🚨 `kimi-k2.7-code` and `kimi-k2.6` are priced IDENTICALLY on mainland
To four decimal places, every component:

| Component | `kimi-k2.7-code` CN | `kimi-k2.6` CN | `kimi-k2.5` CN |
|---|---:|---:|---:|
| Input | **$0.8939** | **$0.8939** | $0.574 |
| Input (implicit cache) | **$0.1788** | **$0.1788** | $0.115 |
| Output | **$3.7131** | **$3.7131** | $3.011 |
| Explicit cache creation | **$1.1174** | **$1.1174** | $0.718 |
| Explicit cache read | **$0.0894** | **$0.0894** | $0.057 |

`kimi-k2.7-code` international is $0.95 / $4.00 (6-7% dearer than its mainland
price, and with **no explicit-cache rows**).

### 🔄 REVERSAL: `kimi-k2.7-code` is the better pick, not the worse one
`model-studio-pricing.md` concluded `kimi-k2.6` was "cheaper **and** smarter"
than `kimi-k2.7-code`, making the newer model a hard sell. That compared
`kimi-k2.6`'s *mainland* price against `kimi-k2.7-code`'s *international* price —
apples to oranges, and the whole basis of the finding.

On the sheet the plan actually bills against, they cost **exactly the same**:

| | `kimi-k2.6` | `kimi-k2.7-code` |
|---|---:|---:|
| Price | $0.8939 / $3.7131 | **identical** |
| AA Intelligence | 42.8 | 41.9 |
| Structured output | ✗ | **✓** |
| Web search | ✗ | **✓** |
| Prefix continuation | ✗ | **✓** |

Same price. `kimi-k2.7-code` trades **0.9 intelligence points** for **three
capabilities**. That is a clear win, and the opposite of the earlier verdict.
`kimi-k2.6` is now the one with no case.

Also retracted: the note that `kimi-k2.6` has explicit cache "unlike
`kimi-k2.7-code`". On mainland both have it, with identical rates. That gap was
an international-vs-mainland artefact too.

`kimi-k2.5` remains a genuine cheaper-but-dumber option (36% cheaper input, 19%
cheaper output, 38.1 vs 42.8 intelligence).

### Limits — identical across all three Kimis and both sheets
224K max in · **16K max out** · 256K context · **500 RPM** · 1M TPM.

Confirms the max-output finding from the international capture: **the whole Kimi
family is capped at 16K output on both sheets**, so our shipped 262,144 for
`kimi-k2.7-code` and 32,768 for `kimi-k2.5` are wrong on any reading.

### Capabilities
`kimi-k2.7-code` CN: playground ✓, function calling ✓, structured output ✓,
web search ✓, prefix continuation ✓, cache ✓, batches ✗, fine-tuning ✗ —
**identical to its international entry**, so no region-scoping here.
`kimi-k2.6` / `kimi-k2.5`: structured output ✗, web search ✗, prefix ✗.

---

## `MiniMax-M2.5`

**Captured:** 2026-07-16 · Mainland only (not offered in Singapore).

| Component | Rate |
|---|---:|
| Input | $0.304 |
| Input (implicit cache) | $0.061 |
| Output | $1.213 |

192K max in · 128K max out · 200K context · 500 RPM · 1M TPM. Capabilities:
structured output ✗, web search ✗, prefix ✗, batches ✗ — the sparsest in the set.

Figures unchanged from `model-studio-pricing.md`; only the label was wrong.
**Still dominated by `deepseek-v4-flash`** ($0.138 / $0.275 mainland, 40.3 vs 33.7
intelligence, 1M vs 200K context) — and the mainland sheet makes it *worse*, since
V4 Flash drops to 0.138/0.275 while MiniMax stays put. The gap widens from ~1.5x
to ~2.2x on input.

---

---

## Qwen — all four, mainland

**Captured:** 2026-07-16 from the console side-by-side compare view. All four are
**tiered at 256k** (same threshold as international) and all four gained **Batches
✓** on mainland.

### Tier 1 (`input <= 256k`), USD per 1M

| Component | `qwen3.7-max` | `qwen3.7-plus` | `qwen3.6-plus` | `qwen3.6-flash` |
|---|---:|---:|---:|---:|
| Discount | **50% off** | **20% off** | none | none |
| Input (list) | 1.65 | 0.276 | 0.276 | 0.165 |
| **Input (effective)** | **0.825** | **0.2208** | **0.276** | **0.165** |
| Output (list) | 4.951 | 1.101 | 1.651 | 0.99 |
| **Output (effective)** | **2.4755** | **0.8808** | **1.651** | **0.99** |
| Implicit cache (list) | 0.33 | 0.056 | n/a | n/a |
| Explicit cache creation | 2.063 | 0.344 | 0.344 | 0.206 |
| Explicit cache read | 0.165 | 0.028 | 0.028 | 0.017 |
| Input (Batch File) | 0.825 | 0.143 | 0.138 | 0.083 |
| Output (Batch File) | 2.475 | 0.574 | 0.825 | 0.495 |
| Input (Batch Chat) | 1.65 *(50% off)* | 0.287 *(50% off)* | 0.275 | 0.165 |
| Output (Batch Chat) | 4.951 *(50% off)* | 1.147 *(50% off)* | 1.65 | 0.99 |

### Tier 2 (`256k < input <= 1m`), USD per 1M

| Component | `qwen3.7-plus` | `qwen3.6-plus` | `qwen3.6-flash` |
|---|---:|---:|---:|
| Input (list) | 0.826 | 1.101 | 0.66 |
| Output (list) | 3.301 | 6.602 | 3.961 |
| Implicit cache (list) | 0.166 | n/a | n/a |
| Explicit cache creation | 1.032 | 1.376 | 0.825 |
| Explicit cache read | 0.083 | 0.111 | 0.066 |
| Input (Batch File) | 0.43 | 0.55 | 0.33 |
| Output (Batch File) | 1.72 | 3.301 | 1.98 |

`qwen3.7-plus` keeps its 20% discount at tier 2 (and 50% on Batch Chat).
`qwen3.7-max` is **not tiered** (confirmed again on mainland).

**Tier-2 multiplier:** `qwen3.6-plus` and `qwen3.6-flash` step up **exactly 4x**
(0.276→1.101, 0.165→0.66); `qwen3.7-plus` steps up **exactly 3x**
(0.276→0.826). So the Qwen tier-2 penalty is steeper on mainland than the ~3x
seen internationally, and differs by model.

### In round CNY (the actual set prices) — per 1M

| Model | Input | Output | Notes |
|---|---:|---:|---|
| `qwen3.7-max` | **12** → *6 effective* | **36** → *18 effective* | flat, 50% off |
| `qwen3.7-plus` T1 | **2** → *1.6* | **8** → *6.4* | 20% off |
| `qwen3.7-plus` T2 | **6** → *4.8* | **24** → *19.2* | 3x tier 1 |
| `qwen3.6-plus` T1 | **2** | **12** | matches the docs example exactly |
| `qwen3.6-plus` T2 | **8** | **48** | 4x tier 1 |
| `qwen3.6-flash` T1 | **1.2** | **7.2** | |
| `qwen3.6-flash` T2 | **4.8** | **28.8** | 4x tier 1 |

`qwen3.6-plus` at **2 / 12 CNY** is exactly what the docs' Credits example
implies — an independent confirmation of the round-CNY finding from Alibaba's own
worked example.

### Capabilities (mainland) — Batches flips ✓ on all four

| Capability | `qwen3.7-max` | `qwen3.7-plus` | `qwen3.6-plus` | `qwen3.6-flash` |
|---|:--:|:--:|:--:|:--:|
| Playground | ✓ | ✓ | ✓ | ✓ |
| Function calling | ✓ | ✓ | ✓ | ✓ |
| Structured output | **✗** | ✓ | ✓ | ✓ |
| Web search | ✓ | ✓ | ✓ | ✓ |
| Prefix continuation | ✓ | ✓ | ✓ | ✓ |
| Cache | ✓ | ✓ | ✓ | ✓ |
| **Batches** | **✓** | **✓** | **✓** | **✓** |
| Fine-tuning | ✗ | ✗ | ✗ | ✗ |

**Batches is ✓ on all four mainland Qwens and ✗ on all four international ones.**
Together with `deepseek-v3.2`, that is five models where Batches is region-scoped
— it now looks like a blanket regional feature, not a per-model one. Batch pricing
is uniformly **50% of** the synchronous rate.

`qwen3.7-max` structured output **✗** matches both sheets and our shipped
metadata. The other three are ✓ on mainland, matching international, and
contradicting our shipped ✗ for `qwen3.7-plus` and `qwen3.6-plus` — so those
errors are confirmed on both sheets.

---

## Outstanding

- [x] ~~All 14 models on the mainland sheet~~ — **complete 2026-07-16**
- [ ] Rebuild `site/index.html` on mainland effective rates; re-derive every
      dominance verdict from scratch.
- [ ] Resolve the 2.8% credits-per-dollar gap (docs 724 vs measured 744) with the
      high-volume run. Does not affect rankings.
- [ ] Probe which rate limits the plan enforces (CN gives DeepSeek 15,000 RPM).
- [ ] Probe which capability set applies — Batches and Web Search are both proven
      region-scoped, so "does batch/web search work on the plan?" is open.
- [ ] Are the Qwen limited-time discounts present on the mainland sheet?
- [ ] Is the Qwen 256k tiering the same on mainland? (`glm-5.1` gained tiering on
      CN, so structure is not sheet-invariant.)
- [ ] Probe which rate limits the plan enforces (CN 15,000 RPM for DeepSeek would
      change the throughput recommendation).
- [ ] Probe which capability set applies — `Batches` and `Web Search` are both
      proven region-scoped, so "does web search work on the plan?" is now open.
- [ ] Re-derive all dominance verdicts once complete; `glm-5.1` already reversed.
