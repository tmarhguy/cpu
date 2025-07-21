💬 PROMPT

You are my automated project bootstrapper.

**Context**

1. You are currently in an empty folder that already contains a file named `literature.md`.
2. The project has not yet been initialized in Git.
3. I will develop primarily in **VS Code** on macOS (M‑series) but teammates may use Windows or Linux.
4. Assume good broadband and latest OS patches.

**High‑level goal**
Read `literature.md`, infer the domain and likely tech stack, then set up _everything_ a modern professional repository needs, from tooling to CI.
If any essential decision (language, framework, DB, cloud target, etc.) is ambiguous, ask me succinct follow‑up questions **before** proceeding.

**Step‑by‑step tasks**

1. **Analyze project brief**
   • Parse `literature.md`; summarise its objectives in ≤ 10 bullet points for your own reference.
   • Detect domain keywords (e.g., “api”, “ml”, “mobile”, “iot”) to shortlist suitable stacks.
   • Base the default language choice on these heuristics:
   – Web/backend → Node LTS (TypeScript) + Express/Fastify OR Python 3.12 + FastAPI.
   – ML/DS heavy → Python 3.12 + Poetry, optional Jupyter.
   – Mobile → React Native/Flutter (Dart 3).
   – Frontend‑only PWA → Vite + React 18 or SvelteKit.
   – Firmware/embedded → CMake + PlatformIO.
   • If multiple stacks fit, prompt me to pick.

2. **Install & pin runtimes**
   • Use language‑specific version managers:
   – `asdf` universal OR
   – `nvm` for Node, `pyenv` for Python, `plenv` for Perl, `goenv` for Go, `jabba` for JDK.
   • Install the **latest stable** LTS of each required runtime and write version files:
   – `.tool‑versions`, `.nvmrc`, `.python‑version`, etc.
   • Globally install core CLIs (latest): Git, Docker Desktop/Engine, `gh`, `pre‑commit`, `pipx`, `direnv`.

3. **Create folders & essential files**

```

/src → production code
/tests → automated tests
/scripts → utility CLI scripts
/docs → MkDocs/Docusaurus site sources
/.vscode → workspace‑specific settings
/.devcontainer → VS Code Remote‑Containers configuration
/configs → lint/format/build config fragments
/infra → IaC (Terraform/Pulumi) and k8s manifests
/examples → quick‑start usage samples
/data (git‑ignored) → local datasets or db volumes

```

• Generate: `README.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE` (MIT by default), `.editorconfig`, `.gitignore`, `.gitattributes`, `.env.example`, `CHANGELOG.md` (keep/changelog style).

4. **Project tooling**
   • **Lint/format**:
   – TypeScript ⇒ ESLint + Prettier (standard config).
   – Python ⇒ ruff + black + isort + mypy.
   • **Tests**:
   – TS ⇒ vitest/jest + testing‑library.
   – Py ⇒ pytest + hypothesis.
   • **Package manager**:
   – TS ⇒ pnpm (preferred), fallback to npm 10 or yarn Berry; enable workspace support.
   – Py ⇒ Poetry 1.8 with PEP 621 `pyproject.toml`.
   • **Commit automation**: Husky pre‑commit + `lint‑staged`, Commitizen with Conventional Commits, semantic‑release.
   • **Containerization**:
   – `Dockerfile` multi‑stage: `dev`, `prod`.
   – `docker‑compose.yml` for db/cache/services.
   • **Dev container**: `.devcontainer/devcontainer.json` referencing the Dockerfile.
   • **CI/CD**:
   – GitHub Actions workflows:
   _ `ci.yml` → lint, type‑check, unit‑test on push/pr (matrix: macOS‑latest, ubuntu‑latest, windows‑latest).
   _ `release.yml` → semantic‑release on `main`. \* `devcontainer‑ci.yml` → build & test inside dev‑container.
   – Optionally ask if GitLab, Azure Pipelines, or CircleCI is preferred instead.
   • **Docs/website**: MkDocs Material or Docusaurus 3, auto‑deploy to GitHub Pages.
   • **Secrets management**: create `.git‑secret‑ignore` list and sample `.env`.
   • **Infrastructure**: if cloud keywords found, scaffold Terraform modules and GitHub OIDC workflows.

5. **VS Code workspace**
   • Install and recommend extensions via `.vscode/extensions.json`:
   – MS‑python.python, ms‑vscode.vscode‑typescript‑next, dbaeumer.vscode‑eslint, esbenp.prettier‑vscode, eamodio.gitlens, ms‑azuretools.vscode‑docker, github.copilot‑chat, editorconfig.editorconfig, ms‑vcscode‑remote.remote‑containers, streetsidesoftware.code‑spell‑checker.
   • Populate `.vscode/settings.json` with lint/format‑on‑save, tab spacing, test explorer, and dev‑container attach settings.
   • Add `.vscode/launch.json` debug configs (node, python, jest/pytest, docker).
   • Add `.vscode/tasks.json` for common CLI tasks (build, test, lint, format, docs‑serve).

6. **Git initialization**
   • `git init -b main`
   • Stage all generated files.
   • `git commit -m "chore: initial project scaffold"`
   • If a remote URL is supplied (`<https://github.com/tmarhguy/cpu.git>` placeholder), run `git remote add origin <https://github.com/tmarhguy/cpu.git>` and `git push -u origin main`.
   • Configure default branch protection advice and enable Git hooks via Husky.

7. **Quality gates & badges**
   • Add README badges: build status, codecov, license, last commit, code quality.
   • Set up Codecov/Coveralls, SonarCloud (optional) with secret tokens in repo settings.

8. **Finishing touches**
   • Generate a one‑paragraph project summary extracted from step 1.
   • Print a quick‑start block showing the minimal commands:

```bash
# 1‑click setup
brew bundle         # or winget/scoop/choco/apt for non‑mac
direnv allow
asdf install        # pulls versions from .tool-versions
pnpm i              # or poetry install
pnpm dev            # start dev server
pnpm test --watch   # run tests continuously
```

• Open VS Code in the current folder (`code .`).

**Non‑negotiables**
• Use **latest stable** versions (e.g., Node 20 LTS, Python 3.12.x) and pin them explicitly.
• Make all scripts cross‑platform (`bash`, PowerShell, `shx`, or `cross‑env`).
• Every generated config/file must include sensible defaults and inline comments for easy tweaking.
• Conform to Conventional Commits and Semantic Versioning from day 1.
• Compact, clear commit history (single initial commit + squash merges).

**Deliverables to me**

1. A concise summary of decisions you made (language, frameworks, CI flow, etc.).
2. Any questions you still need answered.
3. Confirmation that `pnpm dev` / `poetry run` succeeds and tests pass (with sample test).
4. A **single** “done!” message so I know bootstrap is complete.

# START NOW.

```

```
