# scripts/delta_stats.py
import argparse
import json
import os
from statistics import median
from typing import List, Dict, Any

def _pct(x: float) -> str:
    return f"{x*100:.1f}%"

def _quantiles(values: List[float]):
    if not values:
        return None
    v = sorted(values)
    n = len(v)
    def q(p: float):
        # simple nearest-rank with interpolation-ish index
        idx = p * (n - 1)
        lo = int(idx)
        hi = min(lo + 1, n - 1)
        frac = idx - lo
        return v[lo] * (1 - frac) + v[hi] * frac
    return {
        "min": v[0],
        "q25": q(0.25),
        "median": q(0.50),
        "q75": q(0.75),
        "max": v[-1],
        "mean": sum(v) / n,
        "n": n,
    }

def _sign_stats(values: List[float]):
    n = len(values)
    if n == 0:
        return {"n": 0}
    pos = sum(1 for x in values if x > 0)
    zero = sum(1 for x in values if x == 0)
    neg = sum(1 for x in values if x < 0)
    return {
        "n": n,
        "pos": pos, "zero": zero, "neg": neg,
        "pos_rate": pos / n,
        "zero_rate": zero / n,
        "neg_rate": neg / n,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="506", help="results/<client>/_agg/...")
    ap.add_argument("--infile", default=None, help="Override input json path")
    ap.add_argument("--top", type=int, default=5, help="Top gains/losses per metric")
    args = ap.parse_args()

    base = os.path.join("results", args.client, "_agg")
    infile = args.infile or os.path.join(base, "deltas_by_incident.json")
    if not os.path.isfile(infile):
        raise SystemExit(f"[ERROR] File not found: {infile}")

    with open(infile, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = ["R", "H", "S", "D", "K"]
    pairs = ["L1_L0", "L2_L1", "L2_L0"]

    # collect values
    values: Dict[str, Dict[str, List[float]]] = {p: {m: [] for m in metrics} for p in pairs}
    by_incident: Dict[str, Dict[str, Any]] = {}

    for row in data:
        inc = row.get("incident_id", "UNKNOWN")
        by_incident[inc] = row
        for p in pairs:
            for m in metrics:
                key = f"d{m}_{p}"
                if key in row and row[key] is not None:
                    try:
                        values[p][m].append(float(row[key]))
                    except Exception:
                        pass

    # Build markdown
    lines = []
    lines.append(f"# Delta Stats ({args.client})")
    lines.append(f"- Source: `{infile}`")
    lines.append(f"- Incidents: **{len(data)}**")
    lines.append("")

    # Overview tables
    for p in pairs:
        lines.append(f"## {p.replace('_', ' → ')}")
        lines.append("")
        lines.append("| Metric | n | mean | median | q25 | q75 | pos | zero | neg | pos-rate | neg-rate |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

        for m in metrics:
            v = values[p][m]
            q = _quantiles(v)
            s = _sign_stats(v)
            if not q:
                lines.append(f"| {m} | 0 | - | - | - | - | 0 | 0 | 0 | - | - |")
                continue
            lines.append(
                f"| {m} | {q['n']} | {q['mean']:.3f} | {q['median']:.3f} | {q['q25']:.3f} | {q['q75']:.3f} | "
                f"{s['pos']} | {s['zero']} | {s['neg']} | {_pct(s['pos_rate'])} | {_pct(s['neg_rate'])} |"
            )
        lines.append("")

        # Top gains/losses per metric for this pair
        lines.append(f"### Top ±{args.top} Incidents (by {p})")
        for m in metrics:
            key = f"d{m}_{p}"
            scored = []
            for inc, row in by_incident.items():
                if key in row and row[key] is not None:
                    try:
                        scored.append((inc, float(row[key])))
                    except Exception:
                        pass
            scored.sort(key=lambda x: x[1], reverse=True)

            top_pos = [x for x in scored if x[1] > 0][:args.top]
            top_neg = list(reversed([x for x in scored if x[1] < 0][-args.top:]))

            lines.append(f"- **{m}**:")
            if top_pos:
                lines.append(f"  - Gains: " + ", ".join([f"{inc} ({val:+.0f})" for inc, val in top_pos]))
            else:
                lines.append("  - Gains: (none)")
            if top_neg:
                lines.append(f"  - Losses: " + ", ".join([f"{inc} ({val:+.0f})" for inc, val in top_neg]))
            else:
                lines.append("  - Losses: (none)")
        lines.append("")

    out_md = os.path.join(base, "delta_stats.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Wrote: {out_md}")

if __name__ == "__main__":
    main()
