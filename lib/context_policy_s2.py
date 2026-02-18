# lib/context_policy_s2.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional


# ----------------------------
# Helpers
# ----------------------------
def _stable_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _deep_get(d: dict, path: str, default=None):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def _set_path(out: dict, path: str, value: Any):
    cur = out
    parts = path.split(".")
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value


def _estimate_chars_for_field(path: str, value: Any) -> int:
    # deterministic char estimate
    return len(path) + 2 + len(_stable_json(value))


def _truncate_text(s: str, max_chars: int) -> str:
    if not isinstance(s, str):
        s = str(s)
    if len(s) <= max_chars:
        return s
    # head+tail, deterministic
    head = max(0, int(max_chars * 0.7))
    tail = max(0, max_chars - head - 3)
    return s[:head] + "..." + (s[-tail:] if tail > 0 else "")


def _topk_list(xs: list, k: int) -> list:
    if not isinstance(xs, list):
        return xs
    return xs[:k]


# ----------------------------
# Core data structures
# ----------------------------
@dataclass(frozen=True)
class FieldSpec:
    path: str
    prio: str  # "P0" | "P1" | "P2"
    reason: str


@dataclass(frozen=True)
class BudgetPolicy:
    metric: str = "chars"
    max_chars: int = 3500


# ----------------------------
# S2: Normalize
# ----------------------------
def normalize_l2(context_l2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonicalize shape; remove None fields deterministically where useful.
    """
    if not isinstance(context_l2, dict):
        return {"_value": context_l2}

    out = json.loads(json.dumps(context_l2))  # deep-copy via JSON

    # Ensure top-level keys exist (deterministic)
    out.setdefault("asset", {})
    out.setdefault("incident", {})
    out.setdefault("environment", {})
    out.setdefault("device", {})

    # Optional: drop None-only leaves (minimal, safe)
    def prune_none(x):
        if isinstance(x, dict):
            nx = {}
            for k in sorted(x.keys()):
                v = prune_none(x[k])
                if v is not None:
                    nx[k] = v
            return nx if nx else {}
        if isinstance(x, list):
            return [prune_none(v) for v in x]
        return x

    out = prune_none(out)
    return out


# ----------------------------
# S2: Triggers
# ----------------------------
def extract_triggers(ctx: Dict[str, Any]) -> Dict[str, Any]:
    inc = ctx.get("incident", {}) or {}
    env = ctx.get("environment", {}) or {}
    dev = ctx.get("device", {}) or {}

    severity = inc.get("severity", "unknown")
    fault_type = inc.get("fault_type", "unknown")

    connectivity = dev.get("connectivity", "unknown")
    device_state = dev.get("device_state", "unknown")

    weather = env.get("weather", "unknown")
    visibility = env.get("lighting_condition", "unknown")
    time_of_day = env.get("time_of_day", "unknown")

    return {
        "severity": severity,
        "fault_type": fault_type,
        "offline": str(connectivity).lower() in ("offline", "none", "no", "false"),
        "spotty": str(connectivity).lower() in ("spotty", "poor", "unstable"),
        "connectivity": connectivity,
        "device_state": device_state,
        "low_battery": str(device_state).lower() in ("low_battery", "critical_battery"),
        "weather": weather,
        "poor_visibility": str(visibility).lower() in ("poor_visibility", "low", "fog", "dark"),
        "time_of_day": time_of_day,
        "photo_available": bool(inc.get("photo_available", False)),
    }


# ----------------------------
# S2: Deterministic Selector
# ----------------------------
def deterministic_selection_plan(ctx: Dict[str, Any], triggers: Dict[str, Any]) -> List[FieldSpec]:
    """
    Ruleset v1 for your utility field support scenarios (lamps/signals).
    Keep it simple + explainable.
    """
    fields: List[FieldSpec] = []

    # P0 — must-have
    p0 = [
        ("incident.fault_type", "must-have"),
        ("incident.severity", "must-have"),
        ("incident.reported_at", "time-anchor"),
        ("asset.asset_osm", "identity"),
        ("asset.latitude", "location"),
        ("asset.longitude", "location"),
    ]
    # optional nice identity if exists
    if _deep_get(ctx, "asset.name") is not None:
        p0.append(("asset.name", "identity"))

    for path, reason in p0:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P0", reason=reason))

    # P1 — conditional (constraints + risk)
    # Always include device/connectivity if present (action constraints)
    p1_always = [
        ("device.connectivity", "action-constraints"),
        ("device.device_state", "action-constraints"),
    ]
    for path, reason in p1_always:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P1", reason=reason))

    # Environment becomes important if severity high/medium, or poor visibility, or traffic exposure high
    sev = str(triggers.get("severity", "unknown")).lower()
    if sev in ("high", "medium") or triggers.get("poor_visibility") or triggers.get("spotty") or triggers.get("offline"):
        for path, reason in [
            ("environment.time_of_day", "risk-context"),
            ("environment.weather", "risk-context"),
            ("environment.lighting_condition", "risk-context"),
            ("environment.traffic_exposure", "risk-context"),
        ]:
            if _deep_get(ctx, path) is not None:
                fields.append(FieldSpec(path=path, prio="P1", reason=reason))

    # If photo exists, include that fact (not the image itself) to cue workflow
    if triggers.get("photo_available"):
        if _deep_get(ctx, "incident.photo_available") is not None:
            fields.append(FieldSpec(path="incident.photo_available", prio="P1", reason="workflow-cue"))

    # P2 — nice-to-have (only if budget left)
    for path, reason in [
        ("asset.lit", "nice-to-have"),
        ("environment.noise_level", "nice-to-have"),
        ("incident.reporter", "nice-to-have"),
    ]:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P2", reason=reason))

    # Stable ordering: P0 then P1 then P2; within each, lex by path
    order = {"P0": 0, "P1": 1, "P2": 2}
    fields = sorted(fields, key=lambda f: (order.get(f.prio, 9), f.path))
    return fields


# ----------------------------
# S2: Budget packer (chars)
# ----------------------------
def pack_under_budget(
    ctx: Dict[str, Any],
    plan: List[FieldSpec],
    budget: BudgetPolicy,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Greedy packing by plan order. Deterministic compression:
      - long strings: truncate
      - long lists: top-k
    """
    max_chars = budget.max_chars
    used = 0

    out: Dict[str, Any] = {}
    selected_fields = []
    dropped_fields = []
    compressed_fields = []

    def add_field(spec: FieldSpec, value: Any):
        nonlocal used, out

        # Estimate size
        est = _estimate_chars_for_field(spec.path, value)

        # If too large, compress deterministically
        compressed = False
        before = est
        v2 = value

        # compress strings
        if isinstance(v2, str) and est > 800:
            v2 = _truncate_text(v2, max_chars=600)
            compressed = True

        # compress lists
        if isinstance(v2, list) and len(v2) > 10:
            v2 = _topk_list(v2, 10)
            compressed = True

        est2 = _estimate_chars_for_field(spec.path, v2)

        # If still too large, drop
        if used + est2 > max_chars:
            dropped_fields.append({"path": spec.path, "reason": "budget_exceeded", "prio": spec.prio})
            return

        _set_path(out, spec.path, v2)
        used += est2

        selected_fields.append({"path": spec.path, "prio": spec.prio, "reason": spec.reason})

        if compressed:
            compressed_fields.append(
                {
                    "path": spec.path,
                    "method": "truncate_or_topk",
                    "before_chars": before,
                    "after_chars": est2,
                }
            )

    for spec in plan:
        val = _deep_get(ctx, spec.path)
        if val is None:
            continue
        add_field(spec, val)

    packing_meta = {
        "budget_policy": {"metric": budget.metric, "max": max_chars, "used": used},
        "selected_fields": selected_fields,
        "dropped_fields": dropped_fields,
        "compressed_fields": compressed_fields,
    }
    return out, packing_meta


# ----------------------------
# S2: Stable ordering serializer
# ----------------------------
def stable_serialize_context(context_partial: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure predictable top-level ordering by constructing a new dict.
    (JSON dumps will sort keys anyway, but we keep human order.)
    """
    ordered = {}
    for k in ["incident", "asset", "device", "environment", "extras"]:
        if k in context_partial:
            ordered[k] = context_partial[k]
    # carry over any remaining keys deterministically
    for k in sorted(set(context_partial.keys()) - set(ordered.keys())):
        ordered[k] = context_partial[k]
    return ordered


# ----------------------------
# Public: Build L2B output
# ----------------------------
def build_l2b(
    context_l2: Dict[str, Any],
    *,
    selector_version: str = "s2-det-v1",
    budget: Optional[BudgetPolicy] = None,
) -> Dict[str, Any]:
    budget = budget or BudgetPolicy()

    normalized = normalize_l2(context_l2)
    triggers = extract_triggers(normalized)
    plan = deterministic_selection_plan(normalized, triggers)
    packed, packing_meta = pack_under_budget(normalized, plan, budget)
    packed = stable_serialize_context(packed)

    packed.setdefault("extras", {})
    packed["extras"]["context_notes"] = [
        "device.* beschreibt das Techniker-Gerät (App), NICHT das Asset.",
        "low_battery/offline beeinflusst Vorgehen/Workflow (z.B. kurz, offlinefähig dokumentieren), ist keine Fehlerursache des Assets."
    ]

    return {
        "context": packed,
        "selection_meta": {
            "selector_version": selector_version,
            "trigger_signals": triggers,
            **packing_meta,
        },
    }
