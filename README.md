# Alibaba Token Plan — what your credits actually buy

Alibaba Cloud's **Model Studio Token Plan** sells you a prepaid pool of "Credits" and never tells you
what a credit is worth. The docs say only that credits consumed "depend on the model, token count,
thinking mode, and tool calls. Check your bill for exact charges."

This repo works it out by measurement, and prices all 14 models against each other.

**→ [Interactive chart](https://oliver-mee.github.io/alibaba-token-plan-pricing/)** *(if Pages is enabled)*
· [`index.html`](index.html) is self-contained, so you can just open it.

---

## The answer

> ### 1 credit = 0.01 RMB. One fen.
>
> **Credits per 1M tokens = the model's Chinese RMB price × 100.**
> `deepseek-v4-flash` is 1 RMB in / 2 RMB out → **100 / 200 credits**.
> `deepseek-v4-pro` is 12 / 24 RMB → **1,200 / 2,400 credits**.

Measured on the live gateway across four models: **727.15 / 726.99 / 726.99 / 727.02 credits per USD**,
agreeing to **0.02%**. That is exactly 100 fen ÷ $0.1375, the fixed rate Alibaba converts RMB at.

### Where the dollars are

Two currencies are in play and they never meet:

| | |
|---|---|
| **You buy** | $200 → 250,000 credits. Alibaba's price list, not an exchange rate. |
| **You're charged** | tokens → RMB price → credits. **No dollars anywhere.** A credit *is* a fen, so it isn't even a conversion. |
| **The console shows** | 12 RMB ÷ 7.27 = $1.65. Display only. Never touches your bill. |

This is why the dollar prices are odd numbers (1.65, 3.301, 0.138) while the credit prices are round.
The odd ones are the derived ones.

---

## Findings

**It bills at Chinese Mainland prices, not international** — despite serving inference from Singapore.
Fit the observed charges against each sheet and ask whether credits-per-dollar is one constant:
mainland gives 727 across four models (0.03% spread), international gives 501/500/571/500 (13.8%).
Four of the fourteen models have no international price at all, so it could not bill that way even in
principle. The Token Plan is a Chinese product sold internationally.

**Nine of the twelve scoreable models are never the right answer.** Another model on the same plan is
cheaper *and* more intelligent — at every input size and every input:output mix. The frontier is
`deepseek-v4-flash` → `qwen3.7-max` → `glm-5.2`.

**Advertised discounts are honoured inconsistently.** `qwen3.7-max`'s 50% off **is** applied (measured
600 cr/1M). `qwen3.7-plus`'s 20% off is **not** (measured 200 cr/1M = its list rate). Same vendor, same
console, same "limited-time" badge, opposite behaviour. There is no rule — it must be measured per model.

**Max seats are the only good value.** Standard returns 1.15x the list value of what you paid, Pro 1.38x,
**Max 1.72x**. That is a bigger lever than model choice, and it needs no benchmark to believe.

**A token is not a token.** Identical text tokenised to 177,685 tokens on DeepSeek, 201,921 on GLM and
**287,680 on Qwen** — 62% more for the same content. Per-token prices are not comparable across vendors,
and tier thresholds are counted in the vendor's own tokens: the same text DeepSeek saw as a 178k prompt
pushed Qwen past its 256k boundary into tier-2 pricing.

**`max_tokens` does not cap reasoning tokens.** `max_tokens: 1` on `deepseek-v4-flash` returned **127**
completion tokens, 122 of them reasoning. Reasoning bills as output. Send `enable_thinking: false` if you
want to control spend.

**Built-in tools cost extra.** `web_search` is **$10 per 1,000 calls** on top of tokens, `t2i_search` and
`i2i_search` $8. Only `web_extractor` and `code_interpreter` are free, and both are marked limited-time.
Qwen models only, Responses API only.

**`deepseek-v3.2` retires 10 October 2026.** It is the only model carrying a retirement tag.

### ⚠️ This plan is not for backends

> "Scope of Use: For interactive use with compatible AI tools only. **Not permitted for automated
> scripts or application backends.** Violations may result in subscription suspension or API Key
> revocation."

It is a seat subscription for interactive coding tools (Claude Code, OpenClaw, Cursor, Hermes), not cheap
inference to build a product on. Every cost figure here is bounded by that.

---

## What to use

| Use | Model | Why |
|---|---|---|
| **Default** | `deepseek-v4-flash` | 100/200 credits per 1M — cheapest by 4x. 1M context, 384K output, 15k RPM. Beats six models outright. |
| **Hard problems** | `glm-5.2` | Highest intelligence on the plan (AA 51.1). 800/2,800 credits. Capped at 500 RPM, so not for fan-out. |
| **Middle** | `qwen3.7-max` | 600/1,800 credits at its (honoured) 50% discount. |
| **Multimodal / tools** | `qwen3.7-plus` | Image + video in, the Responses-API tools, 15k RPM. Beaten on price-vs-intelligence, but capabilities aren't on the chart. |
| **Avoid** | `deepseek-v4-pro` | Looks like the value pick on public leaderboards because DeepSeek's own API is cheap. Here it's 12x V4 Flash for four intelligence points. |

---

## Repo

| Path | What |
|---|---|
| [`index.html`](index.html) | The interactive chart. Self-contained, no build, no dependencies. |
| [`data/credit-rate-experiment.md`](data/credit-rate-experiment.md) | How the credit rate was measured, raw numbers, and every hypothesis that died on the way. |
| [`data/model-studio-pricing-cn.md`](data/model-studio-pricing-cn.md) | Chinese Mainland datasheet — **the sheet the plan bills against**. All 14 models. |
| [`data/model-studio-pricing.md`](data/model-studio-pricing.md) | International datasheet. Capabilities, limits, tool pricing, and discrepancies against published model metadata. |
| [`data/probes/`](data/probes) | Raw probe results with exact token counts. |
| [`probe-credit-rate.py`](probe-credit-rate.py) | Reproduce the measurement. |

### Reproducing

```bash
export ALIBABA_TOKEN_PLAN_API_KEY=sk-sp-...      # your Token Plan key
python3 probe-credit-rate.py --dry-run           # verify token control, ~free
python3 probe-credit-rate.py --phase a           # input-heavy, ~$0.60 of credits
```

Then read the per-call charges from the console's Usage Details table and divide by the token counts the
script printed. Billing is **per call**, not per minute, so calls match their rows directly.

The method: fire a known number of input tokens with `enable_thinking: false` (reasoning tokens ignore
`max_tokens` and would corrupt the count) and salted padding (a longer pad shares its prefix with a
shorter one and would hit the cache). Cost is then ~99.9% input, so `credits ÷ input_tokens` gives the
input rate directly.

---

## Caveats

- **Intelligence scores** are the Artificial Analysis Intelligence Index (19 June 2026), measured against
  each vendor's own API. They describe the model, not this gateway. `qwen3.6-flash` and `deepseek-v3.2`
  have no score and are listed but not plotted.
- **Throughput is deliberately absent.** AA's tokens/sec is measured elsewhere and would say nothing true
  about Model Studio.
- **Output rates are inferred, not measured** — only input rates were measured directly; outputs are
  derived by assuming the same list-or-discount basis. Three of four models refused to generate long
  output on demand, which made the output measurement unreliable.
- **Prices captured 16 July 2026** and Alibaba changes them often. Re-run the probe before trusting them.
- Credits also depend on thinking mode and tool calls, neither of which is modelled in the chart.

---

## Corrections

Findings here were wrong several times before they were right, mostly by generalising a solid measurement
one model too far — from `qwen3.7-plus` to all discounts, from `kimi-k2.6` to `k2.7-code`, from one price
sheet to another. Each is recorded in `data/credit-rate-experiment.md` rather than quietly fixed, because
the near-misses are instructive: the international sheet gives ~500 credits/dollar for three of four
models and only breaks on the fourth.

The rule this project settled on: **on this plan, per-model facts are per-model. Measure each one.**

Corrections welcome — open an issue with the model, the token counts, and the credit charge.
