# Agent Notes

## Project Shape
- This is a small Python script repo, not a packaged project: there is no `pyproject.toml`, lockfile, or CI workflow in the repo.
- Main entrypoint: `hashmeter.py` continuously measures PBKDF2-HMAC-SHA256 timing, updates a `TDigest`, and writes `data/hashmeter.json` plus `data/timing_values_*.log` by default.
- Analysis entrypoint: `analyze_hashmeter.py` reads `data/hashmeter.json` by default, or another file via `-f/--file`.
- Visualization entrypoint: `visualize_hashmeter.py` is hard-coded to read `./data/hashmeter.json` and opens an interactive matplotlib chart.

## Setup And Commands
- Environment setup is via `./setup.sh`; it uses `uv` to install Python 3.11, create `.venv`, and install third-party dependencies from `requirements.txt`.
- Activate before running scripts: `source .venv/bin/activate`.
- Run collection without waiting 15 seconds between samples during checks: `python hashmeter.py --interval 1 --data-dir /tmp/hashtimer-data` and stop with Ctrl-C.
- Run analysis against generated data: `python analyze_hashmeter.py -f /tmp/hashtimer-data/hashmeter.json`.
- Run focused regression tests with stdlib unittest: `python -m unittest test_analyze_hashmeter test_hashmeter`.
- Smoke-check Python syntax when changing scripts: `python -m py_compile hashmeter.py analyze_hashmeter.py visualize_hashmeter.py`.

## Data And Docs Gotchas
- `hashmeter.py` persists the T-Digest every 1000 measurements and again on shutdown after measurements are collected, so short manual runs should create both a `timing_values_*.log` and `hashmeter.json`.
- Avoid committing generated `data/` directories or timing logs unless explicitly requested.
- `README.md` has newer visualization content than lowercase `readme.md`; if changing duplicated usage/setup docs, keep the duplicate in mind rather than assuming there is only one README.

## Instruction Docs
- Root `AGENTS.md` is currently the only repo instruction file; re-check for nearer `AGENTS.md` files before editing if new directories gain local rules.
- Update the nearest owning `AGENTS.md` when a change alters durable structure, workflows, contracts, required artifacts, or user preferences.
- Maintainer onboarding/history for Beads and DOX lives in `maintainer.md`; keep operational agent rules here and maintainer runbook detail there.
- Create child `AGENTS.md` files only when a subtree gains stable local responsibilities or verification rules that differ from the root.
- Keep instruction docs operational: remove stale guidance instead of documenting history, and do not copy broad framework text from `dox.md` unless it changes how agents should work here.

## DOX Tree
- Root scope `/`: this `AGENTS.md` owns all current project paths, including Python scripts, setup/docs, image assets, and repo-local tool configuration.
- Child DOX Index: none currently; no subdirectory has distinct durable rules that justify a child `AGENTS.md`.
- Tool/generated directories such as `.beads/`, `.claude/`, `.grepai/`, `.venv/`, and `data/` stay under root guidance unless their workflows diverge.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
