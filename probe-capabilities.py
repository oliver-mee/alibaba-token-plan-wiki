#!/usr/bin/env python3
"""
Probe the Token Plan gateway for what models ACTUALLY do.

Why this exists: Alibaba's console and models.dev both publish capability flags,
and both are wrong. Probed 2026-07-17, the console was wrong for 6 of 9 models on
structured_output and models.dev for 3 of 9 — in BOTH directions, so neither can
be corrected from the other. The gateway is the only authority.

Usage:
  export ALIBABA_TOKEN_PLAN_API_KEY=sk-sp-...
  python3 probe-capabilities.py
"""
import json, os, sys, urllib.request, urllib.error

BASE = "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
# CN region: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1

MODELS = ["deepseek-v4-pro", "deepseek-v4-flash", "deepseek-v3.2",
          "qwen3.7-max", "qwen3.7-plus", "qwen3.6-plus", "qwen3.6-flash",
          "kimi-k2.7-code", "kimi-k2.6", "kimi-k2.5",
          "glm-5.2", "glm-5.1", "glm-5", "MiniMax-M2.5"]

SCHEMA = {"type": "json_schema", "json_schema": {"name": "reading", "strict": True, "schema": {
    "type": "object",
    "properties": {"sensor_id": {"type": "string"}, "celsius": {"type": "number"},
                   "stable": {"type": "boolean"}},
    "required": ["sensor_id", "celsius", "stable"], "additionalProperties": False}}}

# Deliberately does NOT mention JSON. Only a working schema-constrained decoder
# produces conforming JSON from this. The no-schema control returns prose.
BARE = [{"role": "user", "content":
         "Sensor A7 is reading 21.5 degrees and has been steady all morning. Report it."}]


def key():
    k = os.environ.get("ALIBABA_TOKEN_PLAN_API_KEY")
    if not k:
        sys.exit("set ALIBABA_TOKEN_PLAN_API_KEY (your sk-sp-... Token Plan key)")
    return k


def call(k, model, body_extra, msg=BARE, max_tokens=200):
    body = {"model": model, "messages": msg, "max_tokens": max_tokens, "temperature": 0}
    body.update(body_extra)
    req = urllib.request.Request(f"{BASE}/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {k}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return "ok", json.loads(r.read())
    except urllib.error.HTTPError as e:
        return "err", json.loads(e.read()).get("error", {}).get("message", "")


def shape(d):
    txt = (d["choices"][0]["message"].get("content") or "").strip()
    try:
        o = json.loads(txt)
        return "CONFORMS" if set(o) == {"sensor_id", "celsius", "stable"} else "json/wrong-shape"
    except json.JSONDecodeError:
        return "prose"


def main():
    k = key()
    print(f"{'model':19s} {'no-thinking':12s} {'schema':16s} {'control':8s} -> verdict")
    for m in MODELS:
        # can thinking be disabled? (MiniMax-M2.5 cannot — it 400s)
        st, d = call(k, m, {"enable_thinking": False}, max_tokens=5)
        nothink = "yes" if st == "ok" else "NO (forced)"
        base = {"enable_thinking": False} if st == "ok" else {}

        st, d = call(k, m, dict(base, response_format=SCHEMA))
        with_schema = shape(d) if st == "ok" else "HTTP400"
        st, d = call(k, m, base)
        control = shape(d) if st == "ok" else "err"

        verdict = ("json_schema ✓" if with_schema == "CONFORMS"
                   else "json_object only" if with_schema == "json/wrong-shape"
                   else "none")
        if control != "prose":
            verdict += "  (!! control not prose — result unsafe)"
        print(f"{m:19s} {nothink:12s} {with_schema:16s} {control:8s} -> {verdict}")


if __name__ == "__main__":
    main()
