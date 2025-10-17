import json
from pathlib import Path

from Truthlens.app.score import compute_score


def load_policy_and_samples(root: Path):
    policy = json.loads((root / "Truthlens" / "core" / "scoring.json").read_text())
    samples = [json.loads(l) for l in (root / "Truthlens" / "data" / "postproof" / "sample.jsonl").read_text().splitlines()]
    return policy, samples


def test_compute_score_samples(tmp_path):
    root = Path(".").resolve().parents[0]
    policy, samples = load_policy_and_samples(Path('.'))
    # run scorer and assert valid shape
    for item in samples:
        sc = compute_score(item, policy)
        assert isinstance(sc, dict)
        assert "score" in sc and 0 <= sc["score"] <= 100
        assert "label" in sc
