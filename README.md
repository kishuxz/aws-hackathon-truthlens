
# TruthLens – Phase 1 (Local scorer)

Score a social post’s reliability against a simple auditable policy using Amazon Bedrock (Nova Micro).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure AWS once (no secrets in repo)
aws configure    # region: us-east-2

jupyter lab
# open Truthlens/app/score.ipynb and run all
```

Layout
Truthlens/
	app/score.ipynb         # calls Bedrock; writes scorecards/*.json
	core/scoring.json       # policy (tier weights, ladder, evidence floor)
	data/postproof/*.jsonl  # sample inputs
	scorecards/             # outputs (gitignored)

Bedrock config

Region: us-east-2

Model: us.amazon.nova-micro-v1:0 (Nova Micro)

Notes

No credentials in repo; outputs are ignored.

Notebook prints a summary and writes one JSON per post to scorecards/.


---

## 4) Clear notebook outputs (optional, tidy)
In VS Code: **Notebook menu → Clear All Outputs**, then save. (We’ve printed only benign info, but clean is nice.)

---

## 5) Commit & push
From the repo root:

```bash
git init
git add .
git status           # verify AWSCLIV2.pkg and scorecards/ are NOT staged
git commit -m "feat: Phase 1 scorer notebook, policy, samples, docs"

# create empty repo on GitHub, then:
git remote add origin https://github.com/<you>/<repo>.git
git branch -M main
git push -u origin main
```


If AWSCLIV2.pkg already got staged once, unstage/remove it:

```bash
git rm --cached AWSCLIV2.pkg
echo "AWSCLIV2.pkg" >> .gitignore
git add .gitignore
git commit -m "chore: ignore local installer"
git push
```


- A deterministic, local scorer (no cloud needed) in `Truthlens/app/score.py`.
- Sample data in `Truthlens/data/postproof/sample.jsonl`.
- The scoring policy in `Truthlens/core/scoring.json`.
- Unit tests in `tests/` and a CI workflow in `.github/workflows/ci.yml`.

Quick start (local)
1. Install dev requirements:

```bash
python -m pip install -r requirements-dev.txt
```

2. Run the local scorer (writes JSON scorecards to `Truthlens/scorecards/`):

```bash
python Truthlens/app/score.py
```

3. Run tests:

```bash
PYTHONPATH=. pytest -q
```

Bedrock-backed scorer
- The original notebook and code include a Bedrock-backed scoring flow that
	invokes an LLM (configured via AWS credentials and `MODEL_ID`). The local
	scorer is deterministic and useful for development or CI.

Notes
- I added a `.gitignore` that excludes typical virtualenv files and outputs.
- Review the repository for any secrets before sharing publicly.

Repo: https://github.com/kishuxz/aws-hackathon-truthlens

