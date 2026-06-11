# Agent Notes

## Project Shape
- This is a small Python script repo, not a packaged project: there is no `pyproject.toml`, `requirements.txt`, lockfile, CI workflow, or test suite in the repo.
- Main entrypoint: `hashmeter.py` continuously measures PBKDF2-HMAC-SHA256 timing, updates a `TDigest`, and writes `data/hashmeter.json` plus `data/timing_values_*.log` by default.
- Analysis entrypoint: `analyze_hashmeter.py` reads `data/hashmeter.json` by default, or another file via `-f/--file`.
- Visualization entrypoint: `visualize_hashmeter.py` is hard-coded to read `./data/hashmeter.json` and opens an interactive matplotlib chart.

## Setup And Commands
- Environment setup is via `./setup.sh`; it uses `uv` to install Python 3.11, create `.venv`, and install `tdigest`, `uvloop`, `probscale`, `matplotlib`, and `numpy`.
- Activate before running scripts: `source .venv/bin/activate`.
- Run collection without waiting 15 seconds between samples during checks: `python hashmeter.py --interval 1 --data-dir /tmp/hashtimer-data` and stop with Ctrl-C.
- Run analysis against generated data: `python analyze_hashmeter.py -f /tmp/hashtimer-data/hashmeter.json`.
- Smoke-check Python syntax when changing scripts: `python -m py_compile hashmeter.py analyze_hashmeter.py visualize_hashmeter.py`.

## Data And Docs Gotchas
- `hashmeter.py` persists the T-Digest only every 1000 measurements; short manual runs may create only a `timing_values_*.log`, not `hashmeter.json`.
- Avoid committing generated `data/` directories or timing logs unless explicitly requested.
- `README.md` has newer visualization content than lowercase `readme.md`; if changing duplicated usage/setup docs, keep the duplicate in mind rather than assuming there is only one README.

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
