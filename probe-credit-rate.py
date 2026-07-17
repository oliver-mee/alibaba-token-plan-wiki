#!/usr/bin/env python3
"""
Measure the Token Plan's credit <-> dollar conversion.

The gateway reports no credit/balance data (headers, body and /usage,/credits,
/balance,/billing,/quota,/me,/account all checked 2026-07-16 — 404). So credits
must be read from the console. This script controls the *firing* side precisely
and prints exactly what to expect, so the console reading is a comparison rather
than a guess.

METHOD
  The console analysis page breaks cost down PER MODEL, so model is the
  separator, not time. Each phase fires one shape across several models inside a
  short window; you then read each model's cost separately.

  Two shapes are needed because one number cannot separate input from output
  cost:
    Shape A (input-heavy):  ~200k input, 1 output   -> isolates input rate
    Shape B (output-heavy): ~20 input, ~8k output   -> isolates output rate

  Solve per model:
    credits_A ~= in_tok_A * Cin + out_tok_A * Cout
    credits_B ~= in_tok_B * Cin + out_tok_B * Cout

THE TESTS THAT MATTER
  1. Within a model: Cout/Cin should equal the console price ratio
     (deepseek-v4-pro: 4.8/2.4 = 2.0 exactly).
  2. Across models: Cin(v4-pro)/Cin(v4-flash) should equal 2.4/0.2 = 12 exactly.
  If both hold, credits are bundled pay-as-you-go and one credits-per-dollar
  constant explains the plan. If the ratios collapse toward 1, credits are
  per-token regardless of model — and the expensive models are underpriced on
  the plan, which would invert the current recommendation.

CRITICAL GOTCHA (found by probe, 2026-07-16)
  max_tokens does NOT cap reasoning tokens. `max_tokens:1` on deepseek-v4-flash
  returned 127 completion tokens (122 reasoning). Every call here sends
  enable_thinking:false, which was verified to work (completion_tokens:1, no
  reasoning_tokens). Without it, output token counts are uncontrolled and the
  arithmetic is meaningless.

USAGE
  python3 probe-credit-rate.py --dry-run          # verify token control, ~free
  python3 probe-credit-rate.py --phase a          # fire input-heavy
  python3 probe-credit-rate.py --phase b          # fire output-heavy
  python3 probe-credit-rate.py --solve            # after entering console figures
"""
import argparse
import json
import os
import sys
import time
import urllib.request

BASE = "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
# CN region instead: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1

# CHINESE MAINLAND rates, USD per 1M tokens — the sheet the plan actually bills
# against (data/model-studio-pricing-cn.md, 16 Jul 2026). Effective, post-discount.
# All four are flat-priced at 200k input, so no tier resolution needed here.
RATES = {
    "deepseek-v4-flash": (0.138,  0.275),
    "deepseek-v4-pro":   (1.65,   3.301),
    "qwen3.7-plus":      (0.2208, 0.8808),  # 20% off, limited-time; tier 1 (<=256k)
    "glm-5.2":           (1.10,   3.851),
}
# expected credits per USD of list price: 724 (docs example) vs 744 (our phase-A
# measurement). This run exists to separate them.
EXPECT_CR_PER_USD = 724.0
MODELS = list(RATES)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "credit-probe-results.json")


def key():
    """Token Plan API key (starts sk-sp-). Not a DashScope key; not interchangeable."""
    k = os.environ.get("ALIBABA_TOKEN_PLAN_API_KEY")
    if not k:
        sys.exit("set ALIBABA_TOKEN_PLAN_API_KEY (your sk-sp-... Token Plan key)")
    return k


def call(k, model, messages, max_tokens):
    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "enable_thinking": False,   # MUST stay: reasoning tokens ignore max_tokens
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    u = d["usage"]
    reasoning = (u.get("completion_tokens_details") or {}).get("reasoning_tokens", 0)
    return {
        "in": u["prompt_tokens"],
        "out": u["completion_tokens"],
        "cached": (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0),
        "reasoning": reasoning,
        "finish": d["choices"][0].get("finish_reason"),
        "secs": round(time.time() - t0, 1),
    }


def padding(target_tokens, salt="0"):
    """Prompt of ~target_tokens. Distinct lines defeat implicit caching, which
    would otherwise bill input at the cache rate and corrupt the measurement.

    `salt` must differ from any previous run: a longer pad starts with the same
    text as a shorter one, so an unsalted 200k pad would share its opening ~2k
    tokens with an earlier 2k dry-run pad and hit the prefix cache. Cached input
    bills at ~1/5 rate, which would silently skew the fit.
    """
    lines = [f"Dataset {salt}. Do not summarise. Records follow.\n"]
    n, i = 12, 0
    while n < target_tokens:
        lines.append(f"Record {salt}-{i:06d}: reference value {(i*7919) % 100000} status nominal.\n")
        n += 18
        i += 1
    return "".join(lines)


def usd(m, tin, tout):
    ri, ro = RATES[m]
    return (tin * ri + tout * ro) / 1e6


def phase_a(k, models, size, dry):
    print(f"\n{'='*74}\nPHASE A — input-heavy (~{size:,} in, 1 out) — isolates INPUT rate\n{'='*74}")
    pad = padding(size, salt="A200k")
    out = {}
    for m in models:
        if dry:
            m_short = padding(2000, salt="dryA")
            r = call(k, m, [{"role": "user", "content": m_short + "\nReply with just: K"}], 1)
            print(f"  {m:20s} in={r['in']:>7,} out={r['out']:>5,} reasoning={r['reasoning']:<4} "
                  f"finish={r['finish']:<7} {r['secs']}s  [dry run, 2k pad]")
        else:
            r = call(k, m, [{"role": "user", "content": pad + "\nReply with just: K"}], 1)
            c = usd(m, r["in"], r["out"])
            print(f"  {m:20s} in={r['in']:>7,} out={r['out']:>5,} cached={r['cached']:<6,} "
                  f"finish={r['finish']:<7} {r['secs']:>5}s  -> ${c:.5f} = {c*EXPECT_CR_PER_USD:>7.2f} cr @724")
            out[m] = {"in": r["in"], "out": r["out"], "cached": r["cached"], "usd": round(c, 6),
                      "expect_credits_724": round(c*EXPECT_CR_PER_USD, 2),
                      "expect_credits_744": round(c*744.0, 2)}
        if r["reasoning"]:
            print(f"    !! {r['reasoning']} reasoning tokens leaked — enable_thinking:false failed")
        if not dry and r["cached"]:
            print(f"    !! {r['cached']:,} cached input tokens — billed at cache rate, results skewed")
    return out


def phase_b(k, models, size, dry):
    print(f"\n{'='*74}\nPHASE B — output-heavy (~20 in, ~{size:,} out) — isolates OUTPUT rate\n{'='*74}")
    prompt = ("Counting exercise B8K. Write the numbers 1, 2, 3 and so on, separated "
              "by commas, counting up. Do not stop until told. Begin: 1, 2, 3,")
    out = {}
    for m in models:
        n = 200 if dry else size
        r = call(k, m, [{"role": "user", "content": prompt}], n)
        if dry:
            print(f"  {m:20s} in={r['in']:>4,} out={r['out']:>6,}/{n:,} "
                  f"finish={r['finish']:<7} {r['secs']}s  [dry run]")
        else:
            c = usd(m, r["in"], r["out"])
            print(f"  {m:20s} in={r['in']:>4,} out={r['out']:>6,}/{n:,} "
                  f"finish={r['finish']:<7} {r['secs']:>5}s  -> ${c:.5f} = {c*EXPECT_CR_PER_USD:>7.2f} cr @724")
            out[m] = {"in": r["in"], "out": r["out"], "usd": round(c, 6),
                      "expect_credits_724": round(c*EXPECT_CR_PER_USD, 2),
                      "expect_credits_744": round(c*744.0, 2)}
        if r["finish"] != "length":
            print(f"    !! stopped early ({r['finish']}) — got {r['out']:,} of {n:,} output tokens")
    return out


def solve():
    if not os.path.exists(RESULTS):
        sys.exit(f"no {RESULTS} — run --phase a and --phase b first")
    d = json.load(open(RESULTS))
    missing = [m for m in d.get("a", {}) if "credits" not in d["a"][m] or "credits" not in d.get("b", {}).get(m, {})]
    if missing:
        print("Add the console credit figures to the JSON first. Missing for:", ", ".join(missing))
        print(f"  file: {RESULTS}")
        print('  add a "credits": <number> to each model under "a" and "b".')
        return
    print(f"\n{'='*74}\nSOLVED CREDIT RATES\n{'='*74}")
    print(f"{'model':20s} {'C_in/1M':>10s} {'C_out/1M':>10s} {'out/in':>8s} {'expected':>9s} {'cr/$':>10s}")
    base = None
    for m in d["a"]:
        a, b = d["a"][m], d["b"][m]
        det = a["in"] * b["out"] - b["in"] * a["out"]
        if not det:
            continue
        cin = (a["credits"] * b["out"] - b["credits"] * a["out"]) / det
        cout = (a["in"] * b["credits"] - b["in"] * a["credits"]) / det
        ri, ro = RATES[m]
        ratio = cout / cin if cin else float("nan")
        crpd = (a["credits"] / a["usd"]) if a["usd"] else float("nan")
        print(f"{m:20s} {cin*1e6:>10.2f} {cout*1e6:>10.2f} {ratio:>8.2f} {ro/ri:>9.2f} {crpd:>10.1f}")
        if base is None:
            base = (m, cin)
    if base:
        print(f"\nCross-model input-rate ratios (vs {base[0]}):")
        for m in d["a"]:
            a, b = d["a"][m], d["b"][m]
            det = a["in"] * b["out"] - b["in"] * a["out"]
            if not det:
                continue
            cin = (a["credits"] * b["out"] - b["credits"] * a["out"]) / det
            exp = RATES[m][0] / RATES[base[0]][0]
            print(f"  {m:20s} measured {cin/base[1]:>7.2f}x   expected {exp:>7.2f}x")
    print("\nIf measured ~= expected everywhere: credits are bundled PAYG, one "
          "credits-per-dollar constant holds, and the cost chart is valid.\n"
          "If ratios collapse toward 1.00: credits are per-token regardless of "
          "model, and expensive models are underpriced on the plan.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="verify token control cheaply")
    p.add_argument("--phase", choices=["a", "b"], help="fire a phase for real")
    p.add_argument("--solve", action="store_true", help="solve from console figures")
    p.add_argument("--models", default=",".join(MODELS))
    p.add_argument("--in-size", type=int, default=200_000)
    p.add_argument("--out-size", type=int, default=8_000)
    args = p.parse_args()

    if args.solve:
        return solve()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    k = key()

    if args.dry_run:
        phase_a(k, models, args.in_size, True)
        phase_b(k, models, args.out_size, True)
        print("\nDry run only — token control verified, nothing large fired.")
        print("Check above: reasoning must be 0, and phase B finish must be 'length'.")
        return

    if not args.phase:
        p.error("pass --dry-run, --phase a, --phase b, or --solve")

    est = sum(usd(m, args.in_size, 1) if args.phase == "a" else usd(m, 20, args.out_size) for m in models)
    print(f"About to fire phase {args.phase.upper()} across {len(models)} models. "
          f"Estimated ${est:.3f} at console rates.")
    print("Note the wall-clock minute — you need it to read the console.")
    input("Enter to fire, Ctrl-C to abort. ")

    t0 = time.strftime("%H:%M:%S")
    res = phase_a(k, models, args.in_size, False) if args.phase == "a" else phase_b(k, models, args.out_size, False)
    t1 = time.strftime("%H:%M:%S")

    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    d = json.load(open(RESULTS)) if os.path.exists(RESULTS) else {}
    d[args.phase] = res
    d.setdefault("windows", {})[args.phase] = f"{t0}-{t1} local"
    json.dump(d, open(RESULTS, "w"), indent=2)

    print(f"\nFired {t0} to {t1} local. Saved to {RESULTS}")
    print("Now read the console analysis page for THIS window, per model, and add")
    print('a "credits": <number> to each model in the JSON. Then run --solve.')


if __name__ == "__main__":
    main()
