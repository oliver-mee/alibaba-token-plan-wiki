# Contributing

Corrections are welcome when they are tied to reproducible evidence.

1. Open an issue describing one factual discrepancy.
2. Name the region, endpoint, model, parameters, date, and observed result.
3. State which checks you ran and which you could not run.
4. Redact credentials, account identifiers, workspace IDs, and private paths.
5. Keep pricing, capability, and documentation changes scoped to the evidence.

You do not need credentials for every region or plan tier. Write `Not run` for
missing coverage and explain what maintainer validation remains.

## Live probes

Live inference may consume plan credits. An AI assistant must not retrieve a key
or run a live probe unless the key owner has expressly approved the endpoint,
models, number of calls, token bounds, and expected cost.

Start with the smallest targeted check that can answer the question. Do not run
catalogue-wide sweeps merely because a script supports them.

## Local checks

```bash
python3 -m json.tool data/models.json >/dev/null
python3 -m compileall -q probe-capabilities.py probe-credit-rate.py
git diff --check
```

## AI assistance

Pull requests must state either `Human-only` or the actual model and tools used,
what work they performed, and how a human verified the result. Model output is
not evidence by itself.
