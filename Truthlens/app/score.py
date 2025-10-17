"""Local deterministic scorer for TruthLens.

This module implements a simple, deterministic scoring function that mirrors the
policy in `core/scoring.json`. It can be run locally against the bundled
`data/postproof/sample.jsonl` without requiring Bedrock.

Usage:
    python Truthlens/app/score.py

The module exposes `compute_score(item, policy)` for unit tests and import.
"""
from __future__ import annotations

import json
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def compute_score(item: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    """Compute a deterministic score for a post `item` using `policy`.

    The implementation follows the project policy:
    - Independence: count a source only once per organization (we use `title`).
    - If 2+ independent Tier A or P support and 0 contradict -> +25.
    - Any Tier A/P contradiction -> -30.
    - Each Tier B support -> +15; each Tier C support -> +5 (cap total support at +25).
    - If total independent sources < evidence_floor.min_sources and no Tier P -> clamp label to "Uncertain" (score <= 69).
    """
    t0 = datetime.utcnow()
    w = policy.get("weights", {})
    base = policy.get("base", 50)

    # enforce independence by organization/title
    seen_orgs = set()
    independent_sources: List[Dict[str, Any]] = []
    for s in item.get("sources", []):
        org = (s.get("title") or s.get("organization") or "").strip()
        if org not in seen_orgs:
            seen_orgs.add(org)
            independent_sources.append(s)

    def T(x: Any) -> str:
        return (x or "").upper()

    # counts
    sup_AP = 0
    con_AP = 0
    sup_B = 0
    sup_C = 0
    has_tierP = False

    for s in independent_sources:
        tier = T(s.get("tier"))
        stance = (s.get("stance") or "").lower()
        if tier == "P":
            has_tierP = True
        if tier in ("A", "P"):
            if stance in ("contradict", "contradicts"):
                con_AP += 1
            if stance == "support":
                sup_AP += 1
        elif tier == "B":
            if stance == "support":
                sup_B += 1
        elif tier == "C":
            if stance == "support":
                sup_C += 1

    score = base
    contributions: List[str] = []

    # contradiction penalty (dominant)
    if con_AP >= 1:
        penalty = w.get("contradicts_from_tierA_or_P>=1", -30)
        score += penalty
        contributions.append(f"{penalty}: Tier A/P contradiction")

    # strong A/P support
    if sup_AP >= 2 and con_AP == 0:
        bonus = w.get("supports_from_tierA_or_P>=2", 25)
        score += bonus
        contributions.append(f"+{bonus}: 2+ independent Tier A/P support")

    # lower-tier supports
    support_bonus = sup_B * w.get("tierB_support", 15) + sup_C * w.get("tierC_support", 5)
    # cap support at policy cap if present
    support_cap = w.get("supports_cap", w.get("supports_from_tierA_or_P>=2", 25))
    if support_bonus > support_cap:
        support_bonus = support_cap
    if support_bonus:
        score += support_bonus
        contributions.append(f"+{support_bonus}: Tier B/C supports (capped)")

    # clamp
    score = max(0, min(100, int(score)))

    # evidence floor
    floor_min = policy.get("evidence_floor", {}).get("min_sources", 2)
    forced_label = None
    if len(independent_sources) < floor_min and not has_tierP:
        # ensure label is Uncertain and score <= 69
        score = min(score, 69)
        forced_label = "Uncertain"

    # label mapping
    ladder = sorted(policy.get("ladder", []), key=lambda r: r.get("min", 0), reverse=True)
    label = next((r.get("label") for r in ladder if score >= r.get("min", 0)), ladder[-1].get("label") if ladder else "Uncertain")
    if forced_label:
        label = forced_label

    sc = {
        "version": "1.0",
        "score": int(score),
        "label": label,
        "contributions": contributions,
        "bullets": contributions[:3],
        "badges": [],
        "citations": [
            {"title": s.get("title"), "tier": s.get("tier"), "stance": s.get("stance")} for s in independent_sources
        ],
        "meta": {
            "post_id": item.get("post_id"),
            "run_id": str(uuid.uuid4()),
            "latency_ms": int((datetime.utcnow() - t0).total_seconds() * 1000),
        },
    }

    return sc


def main():
    ROOT = Path(__file__).resolve().parents[1]
    policy_path = ROOT / "core" / "scoring.json"
    data_path = ROOT / "data" / "postproof" / "sample.jsonl"
    outdir = ROOT / "scorecards"
    outdir.mkdir(exist_ok=True)

    policy = json.loads(policy_path.read_text())
    with data_path.open() as f:
        for line in f:
            item = json.loads(line)
            sc = compute_score(item, policy)
            print(item.get("post_id"), sc.get("label"), sc.get("score"))
            (outdir / f"{item['post_id']}.json").write_text(json.dumps(sc, indent=2))


if __name__ == "__main__":
    main()
