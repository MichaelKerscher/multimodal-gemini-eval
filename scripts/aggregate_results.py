# scripts/aggregate_results.py
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
    """Prefer run_XX.json with highest XX; fallback run.json."""
    runs = sorted(test_dir.glob("run_*.json"))
    if runs:

        def idx(p: Path):
            try:
                return int(p.stem.split("_")[1])
            except Exception:
                return -1

        runs = [p for p in runs if idx(p) >= 0]
        runs = sorted(runs, key=idx)
        return runs[-1] if runs else None

    run_json = test_dir / "run.json"
    return run_json if run_json.exists() else None


def _all_run_files(test_dir: Path) -> list[Path]:
    """Return all run files ordered by run_index (run_01.json, run_02.json, ...)."""
    runs = list(test_dir.glob("run_*.json"))
    if not runs:
        run_json = test_dir / "run.json"
        return [run_json] if run_json.exists() else []

    def idx(p: Path):
        try:
            return int(p.stem.split("_")[1])
        except Exception:
            return -1

    runs = [p for p in runs if idx(p) >= 0]
    return sorted(runs, key=idx)


def _run_index_from_file(p: Path) -> int | None:
    try:
        if p.stem.startswith("run_"):
            return int(p.stem.split("_")[1])
    except Exception:
        pass
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
    return cl or "unknown"


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


def _extract_judge_version(run_obj: dict) -> str:
    rp = run_obj.get("request_params") or {}
    return str(rp.get("judge_version") or "").strip() or "unknown"


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


def _overall_score_row(r: dict) -> float | None:
    vals = [r.get("R"), r.get("H"), r.get("S"), r.get("D"), r.get("K")]
    vals = [v for v in vals if isinstance(v, (int, float))]
    if not vals:
        return None
    return sum(vals) / len(vals)


def _summary_from_rows(rows: list[dict]) -> dict:
    return {
        "n": len(rows),
        "mean_runtime": _mean([x.get("runtime_seconds") for x in rows]),
        "mean_R": _mean([x.get("R") for x in rows]),
        "mean_H": _mean([x.get("H") for x in rows]),
        "mean_S": _mean([x.get("S") for x in rows]),
        "mean_D": _mean([x.get("D") for x in rows]),
        "mean_K": _mean([x.get("K") for x in rows]),
        "mean_overall": _mean([_overall_score_row(x) for x in rows]),
        "flag_rates": {
            "safety_first": _mean([1 if x.get("safety_first") else 0 for x in rows]),
            "escalation_present": _mean([1 if x.get("escalation_present") else 0 for x in rows]),
            "offline_workflow_mentioned": _mean([1 if x.get("offline_workflow_mentioned") else 0 for x in rows]),
            "hallucination_suspected": _mean([1 if x.get("hallucination_suspected") else 0 for x in rows]),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="506", help="results/<client> (default 506)")
    ap.add_argument("--results-dir", default="results", help="base results dir (default results)")
    ap.add_argument("--out", default=None, help="output dir for aggregated files (default: results/<client>/_agg)")
    ap.add_argument("--all-runs", action="store_true", help="also compute run history (runs_by_index + runs_overall)")
    ap.add_argument("--judge-version", default=None, help="filter runs by request_params.judge_version (e.g. judge_v1_1)")
    args = ap.parse_args()

    base = Path(args.results_dir) / args.client
    if not base.exists():
        raise SystemExit(f"[ERROR] Results dir not found: {base}")

    out_dir = Path(args.out) if args.out else (base / "_agg")
    out_dir.mkdir(parents=True, exist_ok=True)

    # exclude only the _agg directory (not suffix matching)
    test_dirs = [p for p in base.iterdir() if p.is_dir() and p.name != "_agg"]

    # ----------------------------
    # 1) Collect latest run per testcase (snapshot)
    # ----------------------------
    run_rows = []

    for td in test_dirs:
        run_file = _latest_run_file(td)
        if not run_file:
            continue

        run_obj = _read_json(run_file)
        if not isinstance(run_obj, dict):
            continue

        # optional filter by judge_version (recommended when you changed the judge)
        if args.judge_version:
            if _extract_judge_version(run_obj) != args.judge_version:
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
        raise SystemExit("[ERROR] No run files found (after optional judge-version filtering).")

    # ----------------------------
    # 2) Summary by context level (snapshot)
    # ----------------------------
    by_cl = defaultdict(list)
    for r in run_rows:
        by_cl[r["context_level"]].append(r)

    summary_by_context = {}
    for cl, rows in sorted(by_cl.items()):
        summary_by_context[cl] = _summary_from_rows(rows)

    # ----------------------------
    # 2b) Summary by strategy (snapshot)
    # ----------------------------
    by_strategy = defaultdict(list)
    for r in run_rows:
        by_strategy[(r.get("strategy") or "UNKNOWN").upper()].append(r)

    summary_by_strategy = {}
    for strat, rows in sorted(by_strategy.items()):
        summary_by_strategy[strat] = _summary_from_rows(rows)

    # ----------------------------
    # 3) Delta per incident (L0, L2, L2B) (snapshot)
    # ----------------------------
    idx = {(r["incident_id"], r["context_level"]): r for r in run_rows}
    deltas = []

    def dk(a, b, key):
        if not a or not b:
            return None
        va, vb = a.get(key), b.get(key)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            return vb - va
        return None

    for inc in sorted(set(r["incident_id"] for r in run_rows)):
        l0 = idx.get((inc, "L0"))
        l2 = idx.get((inc, "L2"))
        l2b = idx.get((inc, "L2B"))

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

    # ----------------------------
    # 4) Missing elements frequency (snapshot)
    # ----------------------------
    miss_counter = Counter()
    for r in run_rows:
        for m in (r.get("missing_elements") or []):
            miss_counter[str(m)] += 1

    # ----------------------------
    # 5) Write snapshot outputs
    # ----------------------------
    rows_path = out_dir / "rows.jsonl"
    with rows_path.open("w", encoding="utf-8") as f:
        for r in run_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary_context_path = out_dir / "summary_by_context_level.json"
    summary_context_path.write_text(json.dumps(summary_by_context, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_strategy_path = out_dir / "summary_by_strategy.json"
    summary_strategy_path.write_text(json.dumps(summary_by_strategy, ensure_ascii=False, indent=2), encoding="utf-8")

    deltas_path = out_dir / "deltas_by_incident.json"
    deltas_path.write_text(json.dumps(deltas, ensure_ascii=False, indent=2), encoding="utf-8")

    missing_path = out_dir / "missing_elements_top.json"
    missing_path.write_text(json.dumps(miss_counter.most_common(50), ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append(f"# Aggregation Report ({args.client})\n")
    if args.judge_version:
        md.append(f"- judge_version filter: **{args.judge_version}**\n")
    md.append(f"- Tests (latest runs): **{len(run_rows)}**\n")
    md.append(f"- Incidents with any deltas: **{len(deltas)}**\n")

    md.append("\n## Mean scores by context level (snapshot)\n")
    for cl, s in summary_by_context.items():
        md.append(f"### {cl} (n={s['n']})\n")
        md.append(f"- mean runtime: {s['mean_runtime']}\n")
        md.append(f"- mean R/H/S/D/K: {s['mean_R']}/{s['mean_H']}/{s['mean_S']}/{s['mean_D']}/{s['mean_K']}\n")
        md.append(f"- mean overall (avg R/H/S/D/K): {s['mean_overall']}\n")
        fr = s["flag_rates"]
        md.append(
            f"- flags (rate): safety_first={fr['safety_first']:.2f}, escalation_present={fr['escalation_present']:.2f}, "
            f"offline_workflow_mentioned={fr['offline_workflow_mentioned']:.2f}, hallucination_suspected={fr['hallucination_suspected']:.2f}\n"
        )

    md.append("\n## Mean scores by strategy (snapshot)\n")
    for strat, s in summary_by_strategy.items():
        md.append(f"### {strat} (n={s['n']})\n")
        md.append(f"- mean runtime: {s['mean_runtime']}\n")
        md.append(f"- mean R/H/S/D/K: {s['mean_R']}/{s['mean_H']}/{s['mean_S']}/{s['mean_D']}/{s['mean_K']}\n")
        md.append(f"- mean overall (avg R/H/S/D/K): {s['mean_overall']}\n")

    md.append("\n## Top missing elements (max 20)\n")
    for k, v in miss_counter.most_common(20):
        md.append(f"- {k}: {v}\n")

    (out_dir / "report.md").write_text("".join(md), encoding="utf-8")

    wrote = [
        str(rows_path),
        str(summary_context_path),
        str(summary_strategy_path),
        str(deltas_path),
        str(missing_path),
        str(out_dir / "report.md"),
    ]

    # ----------------------------
    # (Optional) Run history outputs
    # ----------------------------
    if args.all_runs:
        run_rows_all = []
        for td in test_dirs:
            for rf in _all_run_files(td):
                run_obj = _read_json(rf)
                if not isinstance(run_obj, dict):
                    continue

                if args.judge_version:
                    if _extract_judge_version(run_obj) != args.judge_version:
                        continue

                run_index = _run_index_from_file(rf)
                if run_index is None:
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
                    "run_index": run_index,
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
                    "run_file": str(rf),
                }
                run_rows_all.append(row)

        by_run_strat = defaultdict(list)
        for r in run_rows_all:
            by_run_strat[(r["run_index"], r["strategy"])].append(r)

        runs_by_index = {}
        for (ri, strat), rows in sorted(by_run_strat.items(), key=lambda x: (x[0][0], x[0][1])):
            runs_by_index.setdefault(str(ri), {})
            runs_by_index[str(ri)][strat] = _summary_from_rows(rows)

        runs_by_index_path = out_dir / "runs_by_index.json"
        runs_by_index_path.write_text(json.dumps(runs_by_index, ensure_ascii=False, indent=2), encoding="utf-8")

        # Unweighted mean over run means (mean_overall per run_index)
        strat_run_means = defaultdict(list)
        for ri_str, strat_map in runs_by_index.items():
            for strat, summ in strat_map.items():
                mo = summ.get("mean_overall")
                if isinstance(mo, (int, float)):
                    strat_run_means[strat].append(mo)

        runs_overall = {
            "judge_version_filter": args.judge_version,
            "unweighted": True,
            "per_strategy": {},
        }
        for strat, mos in sorted(strat_run_means.items()):
            runs_overall["per_strategy"][strat] = {
                "n_runs": len(mos),
                "mean_of_run_means": _mean(mos),
                "min_run_mean": min(mos) if mos else None,
                "max_run_mean": max(mos) if mos else None,
            }

        runs_overall_path = out_dir / "runs_overall.json"
        runs_overall_path.write_text(json.dumps(runs_overall, ensure_ascii=False, indent=2), encoding="utf-8")

        wrote += [str(runs_by_index_path), str(runs_overall_path)]

    print("[OK] Wrote:\n- " + "\n- ".join(wrote))


if __name__ == "__main__":
    main()