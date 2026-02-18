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
    return len(path) + 2 + len(_stable_json(value))


def _truncate_text(s: str, max_chars: int) -> str:
    if not isinstance(s, str):
        s = str(s)
    if len(s) <= max_chars:
        return s
    head = max(0, int(max_chars * 0.7))
    tail = max(0, max_chars - head - 3)
    return s[:head] + "..." + (s[-tail:] if tail > 0 else "")


def _topk_list(xs: list, k: int) -> list:
    if not isinstance(xs, list):
        return xs
    return xs[:k]


def _append_note_dedup(container: dict, note: str):
    """
    Deterministically append note into extras.context_notes with dedup.
    - Keeps insertion order for stable behavior.
    - extras/context_notes are created if missing.
    """
    if not note:
        return
    extras = container.setdefault("extras", {})
    notes = extras.setdefault("context_notes", [])
    if not isinstance(notes, list):
        # if polluted by wrong type, overwrite deterministically
        notes = []
        extras["context_notes"] = notes
    if note not in notes:
        notes.append(note)


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
    out.setdefault("extras", {})  # NEW: ensure extras exists for semantic notes

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
        "low_battery": str(device_state).lower() in ("low_battery", "critical_battery", "low_power_mode"),
        "weather": weather,
        "poor_visibility": str(visibility).lower() in ("poor_visibility", "low", "fog", "dark"),
        "time_of_day": time_of_day,
        "photo_available": bool(inc.get("photo_available", False)),
    }


# ----------------------------
# S2: Deterministic Selector
# ----------------------------
def deterministic_selection_plan(ctx: Dict[str, Any], triggers: Dict[str, Any]) -> List[FieldSpec]:
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
    if _deep_get(ctx, "asset.name") is not None:
        p0.append(("asset.name", "identity"))

    for path, reason in p0:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P0", reason=reason))

    # P1 — conditional (constraints + risk)
    p1_always = [
        ("device.connectivity", "action-constraints"),
        ("device.device_state", "action-constraints"),
    ]
    for path, reason in p1_always:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P1", reason=reason))

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

    if triggers.get("photo_available"):
        if _deep_get(ctx, "incident.photo_available") is not None:
            fields.append(FieldSpec(path="incident.photo_available", prio="P1", reason="workflow-cue"))

    # P2 — nice-to-have
    for path, reason in [
        ("asset.lit", "nice-to-have"),
        ("environment.noise_level", "nice-to-have"),
        ("incident.reporter", "nice-to-have"),
        # NEW: allow extras.context_notes to flow through deterministically (small)
        ("extras.context_notes", "semantic-guardrail"),
    ]:
        if _deep_get(ctx, path) is not None:
            fields.append(FieldSpec(path=path, prio="P2", reason=reason))

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
    max_chars = budget.max_chars
    used = 0

    out: Dict[str, Any] = {}
    selected_fields = []
    dropped_fields = []
    compressed_fields = []

    def add_field(spec: FieldSpec, value: Any):
        nonlocal used, out

        est = _estimate_chars_for_field(spec.path, value)

        compressed = False
        before = est
        v2 = value

        if isinstance(v2, str) and est > 800:
            v2 = _truncate_text(v2, max_chars=600)
            compressed = True

        if isinstance(v2, list) and len(v2) > 10:
            v2 = _topk_list(v2, 10)
            compressed = True

        est2 = _estimate_chars_for_field(spec.path, v2)

        if used + est2 > max_chars:
            dropped_fields.append({"path": spec.path, "reason": "budget_exceeded", "prio": spec.prio})
            return

        _set_path(out, spec.path, v2)
        used += est2

        selected_fields.append({"path": spec.path, "prio": spec.prio, "reason": spec.reason})

        if compressed:
            compressed_fields.append(
                {"path": spec.path, "method": "truncate_or_topk", "before_chars": before, "after_chars": est2}
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
    ordered = {}
    for k in ["incident", "asset", "device", "environment", "extras"]:
        if k in context_partial:
            ordered[k] = context_partial[k]
    for k in sorted(set(context_partial.keys()) - set(ordered.keys())):
        ordered[k] = context_partial[k]
    return ordered


# ----------------------------
# NEW: Deterministic semantic guardrails
# ----------------------------
def apply_semantic_guardrails(ctx_norm: Dict[str, Any], triggers: Dict[str, Any], *, guardrails_version: str) -> None:
    """
    Mutates ctx_norm in-place (deterministic). Adds small, high-value notes that prevent misinterpretation.
    Keep this minimal; it is exactly the "policy" in S2.
    """
    # Guardrail 1: device.* refers to technician device, not the asset.
    # Apply if any device information exists, or if offline/low-battery signals are present.
    dev = ctx_norm.get("device") or {}
    has_device_signals = isinstance(dev, dict) and any(k in dev for k in ("connectivity", "device_state"))
    if has_device_signals or triggers.get("offline") or triggers.get("spotty") or triggers.get("low_battery"):
        _append_note_dedup(
            ctx_norm,
            "device.* beschreibt das Techniker-Gerät (App/Smartphone), NICHT das Asset.",
        )
        _append_note_dedup(
            ctx_norm,
            "connectivity/device_state beeinflusst Vorgehen (z.B. offlinefähig dokumentieren), ist keine Fehlerursache des Assets.",
        )

    # Guardrail 2 (optional, example): photo_available is a workflow cue, not evidence of defect.
    if triggers.get("photo_available"):
        _append_note_dedup(
            ctx_norm,
            "incident.photo_available ist ein Workflow-Hinweis (Foto vorhanden), kein Beweis für eine konkrete Ursache.",
        )

    # Stamp version for audit (very small)
    ctx_norm.setdefault("extras", {})
    ctx_norm["extras"].setdefault("guardrails_version", guardrails_version)


# ----------------------------
# Public: Build L2B output
# ----------------------------
def build_l2b(
    context_l2: Dict[str, Any],
    *,
    selector_version: str = "s2-det-v1",
    guardrails_version: str = "s2-guard-v1",  # NEW
    budget: Optional[BudgetPolicy] = None,
) -> Dict[str, Any]:
    budget = budget or BudgetPolicy()

    normalized = normalize_l2(context_l2)
    triggers = extract_triggers(normalized)

    # NEW: apply guardrails BEFORE selection/packing so notes can be selected too
    apply_semantic_guardrails(normalized, triggers, guardrails_version=guardrails_version)

    plan = deterministic_selection_plan(normalized, triggers)
    packed, packing_meta = pack_under_budget(normalized, plan, budget)
    packed = stable_serialize_context(packed)

    return {
        "context": packed,
        "selection_meta": {
            "selector_version": selector_version,
            "guardrails_version": guardrails_version,  # NEW: audit
            "trigger_signals": triggers,
            **packing_meta,
        },
    }
