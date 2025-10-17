# Copilot instructions for this repository

Note: the repository currently appears empty. These instructions are written to help AI coding agents quickly discover and follow this project's conventions when code is added. If you already have an existing `.github/copilot-instructions.md`, merge these recommendations while keeping any project-specific rules.

1. Quick discovery steps
   - Scan the repo root for these files (in order): `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `workspace.json`/`nx.json`, `Makefile`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/*.yml`, `openapi.yaml|openapi.yml`, `README.md`, `src/`, `services/`, `infra/`, `charts/`.
   - Identify the primary language and build tool from the manifest (e.g. `package.json` -> npm/pnpm/yarn; `pyproject.toml` -> poetry/pytest). Use that tool's standard commands for builds/tests.

2. Big-picture architecture checks (what to look for)
   - Monorepo vs single-service: presence of `services/`, `packages/`, or multiple `package.json` files signals multiple services. Example pattern to detect: `services/*/package.json` or `packages/*/tsconfig.json`.
   - API surface: look for `openapi.yaml`, `api/`, or `routes/` to infer service boundaries. Prefer changes that respect API contracts found there.
   - Infra and runtime: `Dockerfile`, `docker-compose.yml`, `infra/` or `charts/` indicate containerized deployments and infra-as-code. Changes that affect runtime must update these artifacts or document rationale.

3. Developer workflows (commands to try)
   - JavaScript/TypeScript: run `npm ci` (or `pnpm install` if `pnpm-lock.yaml` exists), `npm run build`, `npm test`, `npm run lint`.
   - Python: run `python -m venv .venv && . .venv/bin/activate`, then `pip install -r requirements.txt` or `poetry install`; tests via `pytest`.
   - Go: `go test ./...` and builds with `go build ./...`.
   - Docker: `docker build -t <name> .` and `docker-compose up --build` when `docker-compose.yml` exists.

4. Project-specific conventions and patterns
   - Look for `/.github/workflows/*` to learn CI steps (linters, test matrix, build steps) and follow the same commands locally before proposing changes.
   - If `Makefile` exists, prefer targets there (e.g., `make build`, `make test`) since they capture project-specific wrappers and env setups.
   - Search for `.env.example` or `.env.sample` for required environment variables and default values.
   - Follow existing lint/formatter config: `.eslintrc`, `pyproject.toml` `[tool.black]`, `.prettierrc`. Mirror those settings in generated code.

5. Integrations and external dependencies
   - Check `package.json`/`requirements.txt`/`go.mod` for third-party services (e.g., Sentry, Redis, PostgreSQL). If present, update calls and configs cautiously and follow existing auth/env var patterns.
   - For API clients, prefer existing helper modules in `lib/`, `utils/`, or `internal/` rather than creating new ad-hoc clients.

6. PR and commit guidance for AI agents
   - Make small, focused changes. One behavioral change per PR and include the rationale and affected commands in the PR description.
   - Run the project test suite and linters locally; include test output summary in the PR body.
   - If altering public API or contracts (`openapi.yaml`, `schema/`, DB migrations), include migration steps and update documentation files (`README.md`, `docs/`).

7. Examples of actionable checks (automatable)
   - If `package.json` includes `scripts.start`, prefer editing or extending that script rather than adding a new top-level run script.
   - If `src/index.ts` (or `main.py`, `cmd/*.go`) is the entrypoint, update only downstream modules and add tests covering new behavior.
   - When a new environment variable is required, add it to `.env.example` and reference it in `README.md`.

8. When you can't find expected files
   - If the repository is empty or missing manifests, add a short note in the PR describing assumptions and include minimal reproducible steps (e.g., `node` app: add `package.json` with `scripts.test` and a basic test file).

9. Where to document exceptions
   - Add project-specific rules to `.github/copilot-instructions.md` or create `AGENT.md` at the repo root for longer guidance. Preserve any existing human-written sections when merging.

If any of the sections above are unclear or you want the instructions tailored to the actual code in this repo, add the code (or point me to the directory) and I'll re-run a scan and update this file with concrete examples drawn from the sources.
