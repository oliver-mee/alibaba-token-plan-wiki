---
title: Credit-rate experiment — how Token Plan credits convert to money
status: SOLVED — 1 credit = 0.01 RMB (one fen), confirmed against the RMB price sheet
date: 2026-07-16
method: controlled API calls on the live Global token-plan gateway + the official
  docs worked example, fitted against both regional price sheets
key_finding: >
  1 CREDIT = 0.01 RMB (one fen). The Chinese site prices models in round RMB per
  1M tokens; credits are RMB price x 100. Confirmed 2026-07-17 against the actual
  RMB sheet, and measured independently: 727.0 credits per USD (= 100 fen / 0.1375
  USD per RMB), 0.02% spread across 4 models. PURCHASE: 833/1000/1250 credits per
  USD for Standard/Pro/Max seats. The gap is the plan's real discount (1.15x /
  1.38x / 1.72x). The plan bills against the CHINESE MAINLAND sheet despite
  serving inference from Singapore. The Chinese site prices in RMB; the
  international site's "Chinese Mainland" toggle shows the SAME prices converted
  to USD at ~7.27 (1 RMB = $0.1375) — one sheet, two currencies. Advertised
  limited-time discounts are
  honoured INCONSISTENTLY: qwen3.7-max's 50% off IS applied (600 cr/1M),
  qwen3.7-plus's 20% off is NOT (200 cr/1M = list). Same vendor, opposite
  behaviour — must be measured per model. Tokenisers differ hugely (Qwen +62% vs
  DeepSeek on identical text), so per-token prices are not comparable across
  vendors, and tier thresholds are counted in the vendor's own tokens.
credited: >
  Oliver spotted the mainland hypothesis from the deepseek-v4-pro anomaly, found
  the docs Credits example that pinned the burn rate, caught the unevidenced CNY
  claim (later vindicated by evidence he found), supplied the seat pricing that
  revealed the purchase-side rate, asked for the qwen3.7-max test that reversed
  the discount finding, and located the RMB sheet that closed the whole chain.
related: [model-studio-pricing-cn.md, model-studio-pricing.md, ../probe-credit-rate.py]
---

# Credit-rate experiment

## ⭐ THE ANSWER

> ### 1 credit = 0.01 RMB. One fen.
>
> The Chinese Alibaba site prices models in **round RMB per 1M tokens** (1, 2, 6,
> 8, 12, 24, 36…). **A model's credit price is its RMB price × 100.**
> `deepseek-v4-flash` is 1 RMB in / 2 RMB out → **100 / 200 credits**.
> `deepseek-v4-pro` is 12 / 24 RMB → **1,200 / 2,400 credits**.
>
> Confirmed 2026-07-17 against the RMB sheet, and measured independently on the
> live gateway: **727.0 credits per USD** (= 100 fen ÷ $0.1375 per RMB), four
> models agreeing to **0.02%**.
>
> **PURCHASE side: 833 / 1,000 / 1,250 credits per USD** for Standard / Pro / Max
> seats. The gap between buying and burning is the plan's real discount:
> **Standard 1.15x, Pro 1.38x, Max 1.72x** the list value of what you paid.
>
> ⚠️ **Advertised discounts are honoured inconsistently** — `qwen3.7-max`'s 50%
> off IS applied, `qwen3.7-plus`'s 20% off is NOT. Measure per model.

The full chain: **the Token Plan is a Chinese product billed in fen**, sold
internationally in USD, with inference served from Singapore. The international
console's "Chinese Mainland" toggle shows the RMB sheet converted at ~7.27, which
is why its USD figures are odd (1.65, 3.301, 0.138) while the credit figures are
round.

### The calibration run — 2026-07-16 19:06 HKT

Method: ~178k-288k input tokens per model, `enable_thinking:false`, salted padding
to defeat the prefix cache, `max_tokens:1`. Cost is then ~99.9% input, so
`credits ÷ input_tokens` gives the input rate directly. Credits read per call from
the console Usage Details table.

| Model | In tokens | Credits (console) | ⇒ cr/1M in | List $/1M | ⇒ **cr per USD** |
|---|---:|---:|---:|---:|---:|
| `deepseek-v4-flash` | 177,685 | 17.83 | 100.3 | 0.138 | **727.15** |
| `deepseek-v4-pro` | 177,685 | 213.14 | 1,199.5 | 1.65 | **726.99** |
| `qwen3.7-plus` | 287,680 | 172.75 | 600.5 | 0.826 | **726.99** |
| `glm-5.2` | 201,921 | 161.48 | 799.7 | 1.10 | **727.02** |

Four independent models, **mean 727.04, spread 0.02%**. The residual (100.3 not
100) is the console's 3dp USD display, not measurement error.

Solving `deepseek-v4-pro` across both phases (phase B: 49 in / 8,000 out → 19.20
credits) gives **1,199.5 in / 2,392.7 out** — i.e. **1,200 / 2,400**. Round on both
sides, confirming credits are the native unit.

### 🚨 Discounts are honoured INCONSISTENTLY — measured per model

Two Qwen models advertise limited-time discounts. **The plan honours one and
ignores the other.** Three measurements, all decisive:

| Model | Tokens | Credits | List predicts | Disc predicts | Verdict |
|---|---:|---:|---:|---:|---|
| `qwen3.7-max` (50% off) | 254,344 | **152.55** | 305.10 | **152.55** | ✅ **discount applied** |
| `qwen3.7-plus` T2 (20% off) | 287,680 | **172.75** | **172.82** | 138.25 | ❌ **list** |
| `qwen3.7-plus` T1 (20% off) | 132,732 | **26.63** | **26.64** | 21.30 | ❌ **list** |

Same vendor, same console, same "Limited-time" badge, opposite behaviour. **There
is no rule to infer — it must be measured per model.**

Rates actually charged:

| Model | Credits/1M in | Credits/1M out | = console |
|---|---:|---:|---|
| `qwen3.7-max` | **600** | 1,800¹ | discounted |
| `qwen3.7-plus` T1 | **200** | 800¹ | list |
| `qwen3.7-plus` T2 | **600** | 2,400¹ | list |

¹ Output rates inferred by symmetry from the measured input rate (the same
list-or-discount basis). Not independently measured — forcing long output proved
unreliable (see below). Low risk, but unverified.

### The "flat 600" hypothesis — tested and killed

Both 3.7 models charge ~600 cr/1M, but by different routes (Max via its discount,
Plus via its tier-2 list). That raised a real alternative: perhaps the plan simply
has **its own price list** and the console's list/discount is irrelevant.

The tier-1 test separated them cleanly. At 132,732 tokens `qwen3.7-plus` would cost:

| Hypothesis | Predicts | Observed |
|---|---:|---:|
| tier-1 list (200 cr/1M) | **26.64** | **26.63** ✅ |
| tier-1 discounted (160 cr/1M) | 21.30 | ✗ |
| flat 600 for all 3.7 models | 79.64 | ✗ |

**The plan follows the console's tiers exactly.** The 600 coincidence was just a
coincidence. What varies is only whether a given discount reaches the bill.

### ⚠️ Process note — this is the fifth over-generalisation of the session

After measuring `qwen3.7-plus` at list, the conclusion "the discounts do not
apply" was written into the datasheet and the published page, and
`qwen3.7-max` was moved off the frontier on that basis. It was wrong:
`qwen3.7-max` was never tested. Oliver asked for it to be tested, and it reversed
the finding.

The pattern across this session: **plus → max, k2.6 → k2.7, one sheet → another,
credits → CNY, three models → four.** Every one of these looked like a safe
generalisation from a solid measurement, and every one was wrong. The rule this
project should adopt: **on this plan, per-model facts are per-model. Measure each
one.**

### Superseded estimates

| Estimate | Value | Why it was wrong |
|---|---:|---|
| Our first API fit | 744 | Fitted against **international** prices, and assumed the qwen discount applied. |
| Alibaba docs example | 724 | Internally consistent but ~0.4% off the measured rate. Stale, or rounded for publication. |
| Price-roundness hint | ~727 | **Correct.** Prices are round in credits; the roundness pointed at the true rate all along. |

### 🔬 Tokenisers are not comparable across vendors

The **identical text** tokenised to:

| Vendor | Tokens | vs DeepSeek |
|---|---:|---:|
| DeepSeek | 177,685 | — |
| GLM (Zhipu) | 201,921 | +14% |
| **Qwen** | **287,680** | **+62%** |

Two consequences, both underweighted everywhere:

1. **Per-token prices are not comparable across vendors.** Qwen needs ~60% more
   tokens for the same content, which eats most of its headline price advantage.
   Every price chart (including ours) assumes a token is a constant. It is not.
2. **Tier thresholds are counted in the vendor's own tokens.** The same text that
   DeepSeek saw as a 178k prompt pushed Qwen past its 256k boundary and into
   tier-2 pricing.

### Other findings from the run

- **`max_tokens` does not force long output.** 3 of 4 models stopped at ~300
  tokens against `max_tokens: 8000` despite an explicit "do not stop" instruction.
  Only `deepseek-v4-pro` complied and ran to 8,000. Forcing output for
  measurement is unreliable; input-heavy shapes are the trustworthy ones.
- **Salted padding worked** — `cached_tokens: 0` on all four calls.

### Purchase side (console → Add seats, captured 2026-07-16)

| Seat | Price/mo | Credits/mo | Credits per $ | List value @727 | Effective |
|---|---:|---:|---:|---:|---:|
| Standard | $30 | 25,000 | 833.3 | $34.39 | **1.15x** |
| Pro | $100 | 100,000 | **1,000.0** | $137.55 | **1.38x** |
| Max | $200 | 250,000 | 1,250.0 | $343.88 | **1.72x** |

**Max is materially the best value** — 72% above face, vs Pro's 38% and
Standard's 15%. Ranking is Max > Pro > Standard per dollar, always; there is no
usage pattern where a lower tier wins on rate.

Pro buying credits at **exactly 1,000 per USD** is a useful independent signal:
a round number on the purchase side, which is what you would expect if credits
are the plan's native unit and 727 is a separate burn-side conversion rather
than a purchase rate.

What a seat buys in tokens (75/25 blend, list, uncached):

| Seat | `deepseek-v4-flash` @125 cr/1M | `glm-5.2` @1,300 cr/1M |
|---|---:|---:|
| Standard $30 | 200M | 19M |
| Pro $100 | 800M | 77M |
| Max $200 | 2,000M | 192M |

"Current cycle credits" are prorated (24,194 / 96,775 / 241,936 = 0.9677 of face)
for a subscription expiring 2026-08-15.

### 🚨 Scope of Use restriction — the plan is not for backends

Verbatim from the Add-seats page:

> "**Scope of Use:** For interactive use with compatible AI tools only. **Not
> permitted for automated scripts or application backends.** Violations may
> result in subscription suspension or API Key revocation."
>
> "**Account Policy:** API Keys are for the exclusive use of assigned seat members
> only. Sharing or public disclosure is prohibited."

This is a hard constraint on what the Token Plan is for: it is a **seat-based
subscription for interactive AI coding tools** (Claude Code, OpenClaw, Cursor,
Hermes), not cheap inference for a product. Building an application backend on it
risks key revocation. Must be stated before recommending it to anyone, and it
bounds every cost-per-token conclusion in this project to interactive use.

Also: "Token Plan Team does not use conversation data to train models."

### ✅ CONFIRMED: 1 credit = 0.01 RMB (one fen)

**Resolved 2026-07-17** with the actual RMB price sheet from the Chinese Alibaba
site (aliyun / bailian, 中国内地), which prices natively in **元 per 百万 tokens**.

| Model | RMB / 1M | × 100 | **Measured credits/1M** |
|---|---:|---:|---:|
| `deepseek-v4-flash` | 1 | 100 | **100.3** |
| `qwen3.7-plus` T1 | 2 | 200 | **200.7** |
| `qwen3.7-max` (50% off) | 6 | 600 | **599.8** |
| `glm-5.2` | 8 | 800 | **799.7** |
| `deepseek-v4-pro` in | 12 | 1,200 | **1,199.5** |
| `deepseek-v4-pro` out | 24 | 2,400 | **2,392.7** |

**1 credit = 0.01 RMB, exactly, on every model measured.** The residuals (100.3
not 100) are the console's 3dp USD display, not error.

### The two "mainland" sheets are one sheet in two currencies

The Chinese site's RMB prices and the international site's "Chinese Mainland" USD
prices are **the same prices**, converted at a fixed internal rate:

| Model | Component | RMB | USD (mainland) | implied RMB/USD |
|---|---|---:|---:|---:|
| `deepseek-v4-pro` | input | 12 | 1.650 | 7.2727 |
| `deepseek-v4-pro` | output | 24 | 3.301 | 7.2705 |
| `qwen3.7-max` | input (list) | 12 | 1.650 | 7.2727 |
| `qwen3.7-max` | output (list) | 36 | 4.951 | 7.2713 |
| `qwen3.7-max` | cache hit | 2.4 | 0.330 | 7.2727 |
| `qwen3.7-max` | batch file in | 6 | 0.825 | 7.2727 |
| `qwen3.7-max` | batch file out | 18 | 2.475 | 7.2727 |
| `qwen3.7-max` | explicit cache create | 15 | 2.063 | 7.2710 |
| `qwen3.7-max` | explicit cache hit | 1.2 | 0.165 | 7.2727 |

Ten components, **spread 0.36%**. **1 RMB = $0.1375** (≈ 11/80); 1 USD ≈ 7.2727 RMB.
So `credits per USD = 100 / 0.1375 = 727.3` — matching the measured **727.04** to
0.03%.

### The full chain, finally

> The Chinese Alibaba site prices models in **round RMB** per million tokens
> (1, 2, 6, 8, 12, 24, 36…). **Credits are RMB fen** — one credit is 0.01 RMB, so
> a model's credit price is simply its RMB price × 100. The international site's
> "Chinese Mainland" toggle shows those same RMB prices converted to USD at
> ~7.27, which is why the USD figures are odd (1.65, 3.301, 0.138) and the credit
> figures are round. The Token Plan is a **Chinese product billed in fen**, sold
> internationally in USD, with inference served from Singapore.

This also explains every earlier oddity at once: why credit prices are round, why
USD prices are not, why the international/Singapore sheet could never produce a
constant, and why `deepseek-v3.2`/`kimi-k2.5`/`glm-5`/`MiniMax` have non-round
USD figures (they are round in RMB: 2, 4.17…, etc.).

### ⚠️ Process note — right conclusion, wrong method

**This exact claim was made on 2026-07-16, asserted as fact, and correctly
retracted the same day.** The retraction was right *as process* even though the
conclusion turns out to be right:

- The original reasoning was **circular**: 7.24 was derived by dividing the credit
  rate (724) by 100, and "round CNY" was then offered as the explanation for a
  roundness the derivation had itself produced.
- **No RMB sheet had been seen.** The claim was presented as established fact on a
  page about to be published.
- It was only vindicated because Oliver later found the actual RMB pricing.

Being right by luck is not being right. The retraction stands as correct handling;
what changed is the evidence, not the reasoning. Note also the original claimed
7.24 (from the stale docs example); the true rate is **7.27**.

---

### (historical) the retracted text

The 2026-07-16 retraction read: **"1 credit = 0.01 CNY (one fen); mainland
prices are set in round CNY, converted to USD at ~7.24."** That was **wrong and
unevidenced.**

- **No CNY pricing was ever observed.** The mainland console sheet is denominated
  in **USD**, like the international one. "Chinese Mainland" is a region toggle,
  not a currency toggle.
- The reasoning was circular: 7.24 was derived by dividing the credit rate (724)
  by 100, then "round CNY" was offered as the explanation for a roundness that the
  derivation had itself produced.
- **A simpler explanation fits the same data with no invented currency: prices
  are round in CREDITS.** Credits are the plan's native unit; the console shows
  them converted to USD.

| Model | $/1M in | × 724 | $/1M out | × 724 |
|---|---:|---:|---:|---:|
| `deepseek-v4-flash` | 0.138 | **100** | 0.275 | **200** |
| `deepseek-v4-pro` | 1.65 | **1,200** | 3.301 | **2,400** |
| `glm-5.2` | 1.10 | **800** | 3.851 | **2,800** |
| `qwen3.6-plus` | 0.276 | **200** | 1.651 | **1,200** |
| `qwen3.7-max` | 0.825 | **600** | 2.4755 | **1,800** |

Round credit prices, no currency conversion required. **Nothing else in this file
depended on the CNY claim** — the mainland-billing finding rests on the
credits-per-dollar constancy test, which is currency-agnostic.

*(Superseded 2026-07-17: the RMB sheet was found and the fen conversion is now
confirmed — see above. Both the "round credits" and "round RMB" readings were
correct; they are the same fact, since credits ARE fen. The retraction remains
correct as process: at the time, the claim had no evidence behind it.)*

Worked from the official docs example (below), confirmed by controlled API calls.

### Proof — the docs' own worked example

Alibaba publishes estimated Credits for **a single `qwen3.6-plus` request**
(`token-plan-overview` → Credits → Billing → Example). Three independent
components, checked against the mainland rates:

| Component | Tokens | Credits (docs) | Mainland $/1M | ⇒ credits/$ | ⇒ implied credits/1M |
|---|---:|---:|---:|---:|---:|
| Input | 8,349 | 1.67 | 0.276 | 724.7 | **200** |
| Cached | 40,794 | 0.82 | 0.028 | 717.9 | **20** |
| Output | 573 | 0.69 | 1.651 | 729.4 | **1,200** |
| **Total** | | **~3.18** | | mean **724.0** | |

Three independent components give the same credits-per-dollar to within 1.6%
(explained by 2dp rounding on the published credit figures). The implied
per-1M credit prices are **exactly round**: 200 / 1,200 / 20.

Running it forwards from `qwen3.6-plus = 200 / 1,200 / 20 credits per 1M`:

| Component | Calculation | Predicted | Docs says |
|---|---|---:|---:|
| Input | 8,349 × 200/1M | 1.6698 | 1.67 ✓ |
| Cached | 40,794 × 20/1M | 0.8159 | 0.82 ✓ |
| Output | 573 × 1,200/1M | 0.6876 | 0.69 ✓ |
| **Total** | | **3.1733** | **~3.18** ✓ |

Every component matches to the published precision. This is an identity, not a
fit — and it needs no currency conversion, only round credit prices.

### Why this also settles the region question

The docs example **only works against the mainland sheet**. Against international
(`qwen3.6-plus` = $0.50 / $3.00) it yields ~400 credits/$, consistent with nothing
else observed. Against mainland it yields 724 — within 0.4% of the measured 727.
Two unrelated methods, same answer.

> **Note:** this section predates the calibration run and derives **724**. The
> measured rate is **727.0**. The docs example is ~0.4% off — close enough to
> confirm the mainland finding, not precise enough to use. Prefer 727.

### Why the DeepSeek 12x ratio was sheet-invariant

Both models sit on round credit prices, exactly 12x apart:

| Model | Credits per 1M in / out |
|---|---|
| `deepseek-v4-flash` | **100 / 200** |
| `deepseek-v4-pro` | **1,200 / 2,400** |

Exactly 12x, by design — and 12x on the international sheet too. That is why the
credit test showed a clean 12x while fitted against the wrong sheet: the ratio
could not have detected the error.

### ⚠️ Open: a 2.8% discrepancy

| Source | credits per USD | Internal consistency |
|---|---:|---|
| Docs worked example | **724.0** | 3 components within 1.6% |
| Our API measurements (phase A) | **744.0** | 2 models within 0.4% |

Both are internally consistent but disagree by **2.8%**. Likeliest causes: the
docs example is stale, or the console's 3dp USD display rounds differently from
the rate actually used to bill. **Does not
affect any relative conclusion** — every model is converted at the same rate, so
rankings and ratios are unaffected. It only matters for absolute
"credits per month" forecasting. The high-volume run would resolve it.

Note the roundness argument cuts slightly toward a higher rate: at 724,
`deepseek-v4-flash` output computes to 199.1 credits rather than a clean 200, and
`glm-5.2` output to 2,788 rather than 2,800. A rate near **727** makes more prices
land exactly round. But the console publishes USD only to 3 decimals, so the true
rate cannot be recovered from it — this needs the high-volume run, not more
arithmetic.

---

# Method and raw data

## Why

our internal model-metadata reference records cost as **0** everywhere downstream, correctly:
the plan is prepaid, so there is no incremental per-token price for models.dev /
openclaw / hermes to surface. But that leaves the practical question unanswered —
**which model burns the credit pool fastest?** Alibaba publishes seat tiers
($30 / $100 / $200 per month for a Credits allowance) and says only that credits
consumed "depend on the model, token count, thinking mode, and tool calls".

Working hypothesis (Oliver): the plan is **bundled pay-as-you-go** — a call is
metered at portal API rates, and that cost is converted to credits. If true, one
credits-per-dollar constant should explain every charge.

## What the gateway will and will not tell you

Probed 2026-07-16 on the Global gateway:

- **No credit or balance data in response headers.** Headers are just envoy /
  istio routing plus `req-cost-time`, `req-arrive-time`, `resp-start-time`.
- **No usage endpoints.** `GET {base}/usage`, `/credits`, `/balance`, `/billing`,
  `/quota`, `/me`, `/account` all return **404**.
- **`usage` in the response body is exact and complete**: `prompt_tokens`,
  `completion_tokens`, `prompt_tokens_details.cached_tokens`,
  `completion_tokens_details.reasoning_tokens`.

So the token side is precisely measurable from the API, and the credit side must
be read from the console. **Console → Usage Details table.**

## 🚨 Gotcha 1: `max_tokens` does not cap reasoning tokens

`{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":1}`
returned **127 completion tokens** (122 of them `reasoning_tokens`),
`finish_reason: "length"`.

Reasoning tokens are billed as output but ignore `max_tokens`. Any cost
experiment that assumes `max_tokens` controls spend is wrong, and any cost
estimate for a reasoning model that ignores reasoning tokens is badly low —
"hi" costs 127 output tokens, not 3.

**Fix: `enable_thinking: false`.** Verified working on `deepseek-v4-flash`,
`deepseek-v4-pro`, `qwen3.7-plus` and `glm-5.2` — `completion_tokens: 1`, no
`reasoning_tokens` key. Every measurement call must send it.

## ✅ Gotcha 2 (in our favour): billing is PER CALL, not per minute

The console Usage Details table lists **one row per API call** — timestamp, model,
type (`Pro SeatDeduction`), credits to 2dp. Originally assumed to be per-minute
aggregates, which would have forced time-separated phases. It does not: individual
calls can be matched directly to their charges. Rows are timestamped to the minute,
so several calls in one minute are separate rows but share a timestamp — match by
model + expected magnitude.

`Pro SeatDeduction` = the $100/month Pro tier.

## Experiment design

Two call shapes are needed per model: one credit figure cannot separate the input
rate from the output rate.

| Shape | Input | Output | Isolates |
|---|---|---|---|
| **A** | ~1.6-2.6k padded tokens | 1 | input rate |
| **B** | ~45 tokens | 200 (forced, `finish_reason: length`) | output rate |

Solve per model:
```
credits_A = in_A * C_in + out_A * C_out
credits_B = in_B * C_in + out_B * C_out
```
Input padding uses distinct lines (`Record 000123: reference value ...`) so
implicit caching cannot fire and bill input at the cache rate.

Script: `../probe-credit-rate.py` (`--dry-run`, `--phase a|b`, `--solve`).

## Raw data — 2026-07-16 18:11 HKT

Token counts exact from the API `usage` field; credits exact from the console.

| Model | Shape | in | out | credits |
|---|---|---:|---:|---:|
| `deepseek-v4-pro` | A | 1,632 | 1 | **2.01** |
| `glm-5.2` | A | 1,833 | 1 | **1.50** |
| `qwen3.7-plus` | A | 2,625 | 1 | **0.54** |
| `deepseek-v4-flash` | A | 1,632 | 1 | *(not captured — list truncated)* |
| `deepseek-v4-pro` | B | 43 | 200 | **0.48** |
| `glm-5.2` | B | 45 | 200 | **0.56** |
| `qwen3.7-plus` | B | 51 | 200 | **0.16** |
| `deepseek-v4-flash` | B | 43 | 200 | **0.04** |

Two earlier probe calls also billed (`deepseek-v4-flash`: 5 in / 127 out, and
6 in / 1 out) and are not matched to rows.

## Finding 1 — cross-model proportionality holds

`deepseek-v4-flash` and `deepseek-v4-pro`, **identical shape** (43 in, 200 out):

| Model | Price ratio (INTL) | Credits |
|---|---|---:|
| `deepseek-v4-flash` | 1x | 0.04 |
| `deepseek-v4-pro` | **12x** on both in and out | **0.48** = **12x** |

Same work, 12x the price, 12x the credits. Credits scale with model price — the
bundled-PAYG hypothesis survives its first real test. (Caveat: 0.04 carries ±12.5%
rounding at 2dp, so the ratio is 12x ±1.7x.)

## 🚨 Finding 2 — the plan bills at CHINESE MAINLAND prices

The `deepseek-v4-pro` readings sat ~13% below `glm-5.2`'s on the international
sheet. Initially written off as rounding. It was not: **Oliver hypothesised the
plan meters at mainland rates**, and the fit is decisive.

Mainland rates (console, `Chinese Mainland` toggle):

| Model | INTL in / out | **CN in / out** | CN implicit cache |
|---|---|---|---|
| `deepseek-v4-pro` | 2.40 / 4.80 | **1.65 / 3.301** | 0.138 |
| `glm-5.2` | 1.40 / 4.40 | **1.10 / 3.851** | 0.275 |

Fitting the same observed credits against each sheet:

| Test | International | **Chinese Mainland** |
|---|---|---|
| Phase A credits/$ — `v4-pro` vs `glm-5.2` | 512.5 vs 583.5 → **13.0% spread** | 745.5 vs 742.5 → **0.4% spread** |
| Phase B credits/$ — same | 451.5 vs 593.8 → **27.2% spread** | 656.5 vs 683.2 → **4.0% spread** |
| Cross-model ratio, phase A | predicted 1.526 vs observed 1.340 → **-12.2%** | predicted 1.335 → **+0.4%** |
| Cross-model ratio, phase B | predicted 1.127 vs observed 0.857 → **-24.0%** | predicted 0.892 → **-3.9%** |

**Under mainland pricing, credits-per-dollar is a constant across two independent
models to within 0.4%. Under international pricing it is not a constant at all.**
That is not a coincidence.

### Conclusion

> **The Token Plan is a bundle of Chinese-Mainland-priced tokens, served from
> Singapore.** Inference region (`ap-southeast-1`) and billing basis (mainland
> price sheet) are decoupled. The international price sheet — the one the Global
> console shows by default, and the one this project captured first in
> `model-studio-pricing.md` — is **not** the sheet the plan meters against.

Approximate constant: **~745 credits per USD** on the phase-A (input-dominated)
readings, which are the most reliable. Phase B suggests ~657-683 but its figures
are small enough that 2dp rounding dominates. Treat ~745 as provisional until the
high-volume run.

### Consequences

1. **`model-studio-pricing.md` captures the wrong price sheet for this purpose.**
   It stays valid as the international datasheet, but the comparison chart must be
   rebuilt on mainland rates. → CN capture in progress.
2. **`glm-5.2` no longer strictly dominates `deepseek-v4-pro`.** On mainland rates
   GLM is cheaper on input ($1.10 vs $1.65) but **more expensive on output**
   ($3.851 vs $3.301). It still wins on blended cost at any normal ratio and still
   scores 51.1 vs 44.3 on AA — better pick, but a trade-off, not a free lunch. The
   "strictly dominated" verdict on that pair must be withdrawn.
3. **All dominance findings need re-deriving** once the CN sheet is complete.
4. **Rate limits differ between sheets too**, and which set the plan enforces is
   unknown: `deepseek-v4-pro` is 15,000 RPM on CN vs 10,000 on INTL; `glm-5.2` is
   2M TPM on CN vs 1M. Worth probing separately.
5. **Discounts:** on the international sheet, `qwen3.7-plus` only fitted the
   constant at its *discounted* rate. Whether the mainland sheet carries the same
   limited-time discounts is unknown — check when capturing.

## Outstanding

- [ ] Capture Chinese Mainland prices for the other 12 chat models.
- [ ] Rebuild `model-value.html` on mainland rates; re-derive dominance.
- [ ] High-volume run (~200k input) to pin the constant precisely — at 2dp,
      current readings carry up to ±12.5% rounding. Est. ~$0.95 / ~700 credits.
- [x] ~~Establish the purchase-side rate~~ — done: 833 / 1,000 / 1,250 credits
      per USD for Standard / Pro / Max (console → Add seats).
- [ ] Resolve burn rate 724 (docs) vs 744 (measured) vs ~727 (implied by price
      roundness) with the high-volume run.
- [ ] Probe which rate limits the plan actually enforces (CN or INTL).
