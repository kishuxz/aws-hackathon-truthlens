## Contributing to aws-hackathon-truthlens

Thanks for your interest in improving this project. The repo contains a small, local scorer and sample data used for development and testing. Follow these guidelines to contribute effectively.

Quick start
- Fork the repository and create a branch for your work: `git checkout -b feat/my-change`
- Keep changes small and focused; one behavioral change per pull request.

Development setup
- Python 3.10+ recommended. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

- Run tests:

```bash
PYTHONPATH=. pytest -q
```

Code style
- Follow existing project conventions. Keep changes small and avoid reformatting unrelated files.

Testing
- Add unit tests for new behavior in the `tests/` folder. The CI workflow runs `pytest` on pushes and pull requests.

Submitting changes
- Open a PR against `main`. Include a short description of what you changed and why. If your change affects scoring logic, include example inputs and expected outputs.

Security and secrets
- Never commit credentials, secrets, or large data files. Use environment variables for AWS credentials if testing Bedrock/`boto3` code locally.

Contact
- For questions, create an issue in the repo describing the problem and your environment.

Thanks — maintainers
