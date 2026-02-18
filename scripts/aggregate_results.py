# scripts/aggregate_results.py
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter


def _read_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _latest_run_file(test_dir: Path) -> Path | None:
    # prefers run_XX.json with highest XX; fallback run.json
    runs = sorted(test_dir.glob("run_*.json"))
    if runs:

        def idx(p: Path):
            stem = p.stem  # run_01
            try:
                return int(stem.split("_")[1])
            except Exception:
                return -1

        runs = sorted(runs, key=idx)
        return runs[-1]

    run_json = test_dir / "run.json"
    if run_json.exists():
        return run_json
    return None


def _extract_strategy(run_obj: dict) -> str:
    rp = run_obj.get("request_params") or {}
    s = str(rp.get("context_strategy") or "").strip().upper()
    return s or "UNKNOWN"


def _extract_context_level(run_obj: dict) -> str:
    """
    Map to analysis levels:
      - S0 -> L0
      - S1 -> L2
      - S2 -> L2B
    Fallback: try old input.meta.context_level if it exists.
    """
    strategy = _extract_strategy(run_obj)

    if strategy == "S0":
        return "L0"
    if strategy == "S1":
        return "L2"
    if strategy == "S2":
        return "L2B"

    # fallback (older logs)
    meta = ((run_obj.get("input") or {}).get("meta") or {})
    cl = str(meta.get("context_level") or "").strip()
    if cl == "L0_minimal":
        return "L0"
    if cl == "L2_full":
        return "L2"
    if cl:
        return cl
    return "unknown"


def _extract_incident_id(run_obj: dict) -> str:
    # prefer explicit meta if present (older manifests)
    meta = ((run_obj.get("input") or {}).get("meta") or {})
    inc = meta.get("incident_id")
    if inc:
        return str(inc).strip()

    # fallback: INC-...-TCx -> INC-...
    tid = run_obj.get("test_id", "")
    if "-TC" in tid:
        return tid.split("-TC")[0]
    return "UNKNOWN"


def _coerce_judge_block(judge_val):
    """
    judge in run_XX.json might be:
      - dict (ideal)
      - None
      - string containing JSON or fenced ```json ... ```
    Return dict or None.
    """
    if judge_val is None:
        return None
    if isinstance(judge_val, dict):
        return judge_val
    if isinstance(judge_val, str):
        s = judge_val.strip()
        # strip fenced code blocks
        if s.startswith("```"):
            lines = s.splitlines()
            if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].startswith("```"):
                s = "\n".join(lines[1:-1]).strip()
        try:
            obj = json.loads(s)
            if isinstance(obj, dict):
                return obj
        except Exception:
            return None
    return None


def _mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return (sum(xs) / len(xs)) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="506", help="results/<client> (default 506)")
    ap.add_argument("--results-dir", default="results", help="base results dir (default results)")
    ap.add_argument("--out", default=None, help="output dir for aggregated files (default: results/<client>/_agg)")
    args = ap.parse_args()

    base = Path(args.results_dir) / args.client
    if not base.exists():
        raise SystemExit(f"[ERROR] Results dir not found: {base}")

    out_dir = Path(args.out) if args.out else (base / "_agg")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Collect latest run per testcase
    run_rows = []
    # exclude only the _agg directory (not suffix matching)
    test_dirs = [p for p in base.iterdir() if p.is_dir() and p.name != "_agg"]

    for td in test_dirs:
        run_file = _latest_run_file(td)
        if not run_file:
            continue
        run_obj = _read_json(run_file)
        if not isinstance(run_obj, dict):
            continue

        test_id = run_obj.get("test_id", td.name)
        incident_id = _extract_incident_id(run_obj)
        strategy = _extract_strategy(run_obj)
        context_level = _extract_context_level(run_obj)

        judge_block = _coerce_judge_block(run_obj.get("judge"))
        scores = (judge_block or {}).get("scores") or {}
        flags = (judge_block or {}).get("flags") or {}
        missing = (judge_block or {}).get("missing_elements") or []

        row = {
            "test_id": test_id,
            "incident_id": incident_id,
            "strategy": strategy,
            "context_level": context_level,
            "client": run_obj.get("client"),
            "model": run_obj.get("model"),
            "runtime_seconds": ((run_obj.get("meta") or {}).get("runtime_seconds")),
            "has_judge": bool(judge_block),
            "R": scores.get("R"),
            "H": scores.get("H"),
            "S": scores.get("S"),
            "D": scores.get("D"),
            "K": scores.get("K"),
            "safety_first": flags.get("safety_first"),
            "escalation_present": flags.get("escalation_present"),
            "offline_workflow_mentioned": flags.get("offline_workflow_mentioned"),
            "hallucination_suspected": flags.get("hallucination_suspected"),
            "missing_elements": missing,
            "run_file": str(run_file),
        }
        run_rows.append(row)

    if not run_rows:
        raise SystemExit("[ERROR] No run files found.")

    # 2) Summary by context level
    by_cl = defaultdict(list)
    for r in run_rows:
        by_cl[r["context_level"]].append(r)

    summary = {}
    for cl, rows in sorted(by_cl.items()):
        summary[cl] = {
            "n": len(rows),
            "mean_runtime": _mean([x.get("runtime_seconds") for x in rows]),
            "mean_R": _mean([x.get("R") for x in rows]),
            "mean_H": _mean([x.get("H") for x in rows]),
            "mean_S": _mean([x.get("S") for x in rows]),
            "mean_D": _mean([x.get("D") for x in rows]),
            "mean_K": _mean([x.get("K") for x in rows]),
            "flag_rates": {
                "safety_first": _mean([1 if x.get("safety_first") else 0 for x in rows]),
                "escalation_present": _mean([1 if x.get("escalation_present") else 0 for x in rows]),
                "offline_workflow_mentioned": _mean(
                    [1 if x.get("offline_workflow_mentioned") else 0 for x in rows]
                ),
                "hallucination_suspected": _mean([1 if x.get("hallucination_suspected") else 0 for x in rows]),
            },
        }

    # 2b) Summary by strategy (recommended; helps thesis reporting)
    by_s = defaultdict(list)
    for r in run_rows:
        by_s[r.get("strategy", "UNKNOWN")].append(r)

    summary_strategy = {}
    for s, rows in sorted(by_s.items()):
        summary_strategy[s] = {
            "n": len(rows),
            "mean_runtime": _mean([x.get("runtime_seconds") for x in rows]),
            "mean_R": _mean([x.get("R") for x in rows]),
            "mean_H": _mean([x.get("H") for x in rows]),
            "mean_S": _mean([x.get("S") for x in rows]),
            "mean_D": _mean([x.get("D") for x in rows]),
            "mean_K": _mean([x.get("K") for x in rows]),
        }

    # 3) Delta per incident (L0, L2, L2B)
    idx = {(r["incident_id"], r["context_level"]): r for r in run_rows}
    deltas = []

    for inc in sorted(set(r["incident_id"] for r in run_rows)):
        l0 = idx.get((inc, "L0"))
        l2 = idx.get((inc, "L2"))
        l2b = idx.get((inc, "L2B"))

        def dk(a, b, key):
            if not a or not b:
                return None
            va, vb = a.get(key), b.get(key)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                return vb - va
            return None

        row = {"incident_id": inc}

        # S1 vs S0
        if l0 and l2:
            for m in ["R", "H", "S", "D", "K"]:
                row[f"d{m}_L2_L0"] = dk(l0, l2, m)

        # S2 vs S1
        if l2 and l2b:
            for m in ["R", "H", "S", "D", "K"]:
                row[f"d{m}_L2B_L2"] = dk(l2, l2b, m)

        # S2 vs S0
        if l0 and l2b:
            for m in ["R", "H", "S", "D", "K"]:
                row[f"d{m}_L2B_L0"] = dk(l0, l2b, m)

        if any(v is not None for k, v in row.items() if k != "incident_id"):
            deltas.append(row)

    # 4) Missing elements frequency
    miss_counter = Counter()
    for r in run_rows:
        for m in (r.get("missing_elements") or []):
            miss_counter[str(m)] += 1

    # 5) Write outputs
    rows_path = out_dir / "rows.jsonl"
    with rows_path.open("w", encoding="utf-8") as f:
        for r in run_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary_path = out_dir / "summary_by_context_level.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_strategy_path = out_dir / "summary_by_strategy.json"
    summary_strategy_path.write_text(json.dumps(summary_strategy, ensure_ascii=False, indent=2), encoding="utf-8")

    deltas_path = out_dir / "deltas_by_incident.json"
    deltas_path.write_text(json.dumps(deltas, ensure_ascii=False, indent=2), encoding="utf-8")

    missing_path = out_dir / "missing_elements_top.json"
    missing_path.write_text(json.dumps(miss_counter.most_common(50), ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append(f"# Aggregation Report ({args.client})\n")
    md.append(f"- Tests (latest runs): **{len(run_rows)}**\n")
    md.append(f"- Incidents with any deltas: **{len(deltas)}**\n")

    md.append("\n## Mean scores by context level\n")
    for cl, s in summary.items():
        md.append(f"### {cl} (n={s['n']})\n")
        md.append(f"- mean runtime: {s['mean_runtime']}\n")
        md.append(f"- mean R/H/S/D/K: {s['mean_R']}/{s['mean_H']}/{s['mean_S']}/{s['mean_D']}/{s['mean_K']}\n")
        fr = s["flag_rates"]
        md.append(
            f"- flags (rate): safety_first={fr['safety_first']:.2f}, escalation_present={fr['escalation_present']:.2f}, "
            f"offline_workflow_mentioned={fr['offline_workflow_mentioned']:.2f}, hallucination_suspected={fr['hallucination_suspected']:.2f}\n"
        )

    md.append("\n## Mean scores by strategy\n")
    for s, stats in summary_strategy.items():
        md.append(f"### {s} (n={stats['n']})\n")
        md.append(f"- mean runtime: {stats['mean_runtime']}\n")
        md.append(f"- mean R/H/S/D/K: {stats['mean_R']}/{stats['mean_H']}/{stats['mean_S']}/{stats['mean_D']}/{stats['mean_K']}\n")

    md.append("\n## Top missing elements (max 20)\n")
    for k, v in miss_counter.most_common(20):
        md.append(f"- {k}: {v}\n")

    (out_dir / "report.md").write_text("".join(md), encoding="utf-8")

    print(
        f"[OK] Wrote:\n- {rows_path}\n- {summary_path}\n- {summary_strategy_path}\n- {deltas_path}\n- {missing_path}\n- {out_dir / 'report.md'}"
    )


if __name__ == "__main__":
    main()
