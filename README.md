# Alibaba Token Plan Wiki

Public, measured reference data for Alibaba Cloud and Qwen Cloud Token Plan.

This repository covers:

- the Global/Singapore and China/Beijing gateways;
- Personal and Team model entitlements;
- chat, image, video, and audio (TTS/realtime) catalogue data;
- OpenAI-compatible and Anthropic-compatible behaviour;
- model capability probes;
- Token Plan credit pricing.

The data is measured against the live gateways because vendor pages and community
catalogues can lag or disagree with runtime behaviour.

## Start here

| Resource | Purpose |
|---|---|
| [Machine-readable catalogue](data/models.json) | Sanitised current model, tier, modality, limit, and capability data |
| [Interactive pricing chart](https://oliver-mee.github.io/alibaba-token-plan-wiki/) | Compare measured Token Plan credit costs |
| [Credit-rate experiment](data/credit-rate-experiment.md) | Method and raw reasoning behind `1 credit = 0.01 RMB` |
| [Mainland pricing reference](data/model-studio-pricing-cn.md) | Chinese Mainland model pricing |
| [International pricing reference](data/model-studio-pricing.md) | International pricing and capability comparisons |
| [Raw probe results](data/probes/) | Redacted measurements used by the analysis |

## Current catalogue

As of 18 August 2026:

- Team exposes 17 chat models; Personal exposes 8 (a strict subset).
- `/models` lists 22 ids per Team key: 16 chat + 4 image + 1 TTS + 1 realtime
  audio. The 3 video models never appear on `/models` (async endpoint).
- One additional chat model (`deepseek-v4-pro-0813`) is servable by exact id
  but not surfaced on `/models`; it is in the catalogue as `unlisted`.
- The exact counts move as models land. [`data/models.json`](data/models.json)
  carries the current list and its `updated` date; trust it over this prose.
- Both tiers use the same `sk-sp-` key prefix, so the tier cannot be inferred
  from the key.
- Global and China use separate credentials and endpoints.
- A successful `/models` response is catalogue evidence, not proof that a
  subscription can perform inference. A lapsed subscription may still list
  models and then deny calls.

The complete current list and capability matrix live in
[`data/models.json`](data/models.json). Downstream integrations should cite a
tag or commit rather than silently copying an unversioned list.

## Endpoints

| Region | OpenAI-compatible base URL | Anthropic-compatible base URL |
|---|---|---|
| Global | `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |
| China | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

Token Plan keys are separate from DashScope pay-as-you-go and Alibaba Coding
Plan credentials.

## Pricing result

> 1 Token Plan credit = 0.01 RMB.

The gateway burns credits using Chinese Mainland model prices. For example, a
model priced at 1 RMB input and 2 RMB output per million tokens consumes about
100 input credits and 200 output credits per million tokens.

The measured experiment, alternative hypotheses, and raw numbers are in
[`data/credit-rate-experiment.md`](data/credit-rate-experiment.md).

## Reproducing probes

The scripts read credentials only from the environment. They never print the
key.

```bash
export ALIBABA_TOKEN_PLAN_API_KEY=sk-sp-...
python3 probe-credit-rate.py --dry-run
python3 probe-capabilities.py --help
```

Live probes may consume plan credits. Before running one:

1. Read the script and confirm the endpoint, models, call count, and token
   bounds.
2. Obtain the key owner's express permission.
3. Make sure the owner understands the likely credit cost.
4. Start with the smallest targeted probe that can answer the question.

Do not use an AI agent to run a catalogue-wide or token-heavy probe without
that informed permission.

## Evidence rules

- Runtime claims should identify the endpoint, date, model, parameters, and
  observed result.
- A model-generated explanation is not evidence by itself.
- A `200` response does not prove a modality worked. Some text-only models
  silently ignore unsupported media.
- A validation error can reveal accepted parameter values, but it does not
  necessarily reveal the model's real output or context ceiling.
- Missing regional or tier credentials should be reported as untested, not
  guessed.
- Never publish API keys, account identifiers, private paths, workspace IDs,
  or unredacted logs.

## Downstream integrations

- [Hermes Alibaba Token Plan plugin](https://github.com/oliver-mee/hermes-alibaba-token-plan)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [models.dev](https://models.dev/)

The public catalogue is generated from a more detailed working dataset and
then privacy-scanned before publication. Corrections are welcome through a
focused issue with reproducible evidence.

## Scope of use

Token Plan is licensed for interactive use with compatible AI coding and agent
tools. It is not intended as a general application backend, unattended batch
processor, load-testing service, or shared key pool.

## Licence

MIT. See [LICENSE](LICENSE).
