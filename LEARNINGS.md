# Project learnings (public)

What we have learned from keeping this catalogue measured against the live
gateway rather than against vendor pages. Every claim here comes from a
probe or a dated observation recorded in [`data/models.json`](data/models.json).

## Vendor pages disagree with the gateway, in both directions

- Alibaba's own model cards are written for Model Studio (pay-as-you-go), not
  for Token Plan. A feature listed on a card means the model supports it
  somewhere; it does not mean the Token Plan gateway serves it.
- The 2026-07-17 audit found the console wrong on 10 of 14 models and the
  community catalogue models.dev wrong on 6 of 14 for structured output alone.
- Worked example: `deepseek-v4.1-flash`'s card advertises structured outputs,
  but the plan gateway rejects strict `json_schema` with a 400 while
  `json_object` works. The card is true for Model Studio; the catalogue is
  true for the plan.

## The gateway is the only entitlement authority

- A model appearing in the platform changelog is not on the Token Plan until
  `GET /models` lists it. Third-party models typically land on the plan days
  to weeks after their changelog entry.
- `/models` is tier-aware and costs nothing. Personal is a strict subset of
  Team; both tiers use the same `sk-sp-` key prefix, so tier cannot be
  inferred from the key.
- A dated snapshot id (e.g. `qwen3.8-max-0902`) can 404 on the plan even while
  the stable alias (`qwen3.8-max`) serves that exact snapshot. Dated variants
  need their own probe and their own card; never inherit the base model's
  rates or behaviour.

## Promotions are time-sensitive and inconsistently applied

- Advertised discounts are honoured unevenly: one model's 50% off applied to
  billed credits, a sibling's 20% off did not, on the same date, on the same
  tier. Measure per model; a doc claim of a discount is not a billed
  discount.
- Night-window (22:00-08:00) half-price rosters change per model release and
  differ between Personal and Team (e.g. `qwen3.8-max` has the night promo on
  Personal only). Re-verify the roster rather than assuming it follows the
  supported-models table.

## Capability contracts move without notice

- A probe is true on the date it was taken. The same request has returned 400,
  200, and 403 for the same model across weeks as vendor entitlements
  changed (`deepseek-v4-flash` on `/responses`: unsupported 2026-07-24,
  working 2026-08-14, Personal-tier 403 2026-09-16).
- Published ceilings are not always enforced by the gateway (max_tokens and
  thinking_budget both accepted beyond the card numbers). Treat ceilings as
  contract, not as tested boundaries.
- Two OpenAI-compatible surfaces behave differently: the Chat Completions
  surface and the Anthropic-compatible surface (no listing, but every chat
  model callable by id) disagree on forced-tool structured output. Claude
  Code users live on the second surface and need that in mind.

## Catalogue hygiene

- A model that leaves `/models` should be pulled or marked `unlisted` in the
  same pass; a selectable-but-dead row is a worse outcome than a missing row.
- `unlisted` has two distinct meanings in this data: callable by exact id but
  absent from the listing (e.g. `deepseek-v4-pro-0813`), versus async-only
  endpoints that never list (all video models).
- Unknown fields stay labelled unknown. This catalogue prefers an explicit
  gap over a plausible value, and dates its evidence so staleness is visible.
