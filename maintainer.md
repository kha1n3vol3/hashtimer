# Maintainer Onboarding

This records the Beads and DOX setup steps used for this repository. Keep `AGENTS.md` as the compact agent-facing contract; use this file for maintainer runbook details.

## Beads Setup Used Here

1. Initialize Beads against a Dolt SQL server:
   ```bash
   bd init --server
   ```
2. Confirm the generated context:
   ```bash
   bd prime
   bd ready --json
   bd context --json
   ```
3. Shorten the issue prefix from `hashtimer` to `ht`:
   ```bash
   bd rename-prefix ht- --dry-run --actor kha1n3vol3
   bd rename-prefix ht- --actor kha1n3vol3
   ```
4. Set the default Beads actor to the active GitHub login:
   ```bash
   gh api user --jq .login
   bd config set actor kha1n3vol3 --actor kha1n3vol3
   ```
5. Verify Beads state after configuration changes:
   ```bash
   bd config get issue_prefix --json
   bd config get actor --json
   bd ready --json
   bd doctor
   ```

Repo-specific Beads state after onboarding:
- Issue prefix: `ht`
- Default actor: `kha1n3vol3`
- Backend mode: Dolt server mode
- Known warning: no Beads remote is configured unless a maintainer adds one with `bd dolt remote add origin <url>`.

## DOX Setup Used Here

1. Review the candidate DOX guidance in `dox.md`.
2. Preserve only repo-specific operational guidance in `AGENTS.md`; do not copy broad framework text wholesale.
3. Scan the current instruction tree:
   ```bash
   # Any equivalent file discovery command is fine.
   # Current result should list only ./AGENTS.md unless child scopes have been added.
   ```
4. Record the active DOX tree in `AGENTS.md`:
   - Root scope `/` owns current project paths.
   - Child DOX Index is currently empty.
   - Tool/generated directories remain under root guidance until their workflows diverge.
5. Verify the instruction update:
   ```bash
   bd ready --json
   bd doctor
   nit diff -- AGENTS.md
   ```

## Maintenance Notes

- Create a child `AGENTS.md` only when a subtree gains stable local responsibilities or verification rules that differ from the root.
- Update `AGENTS.md` when durable workflows, contracts, required artifacts, or user preferences change.
- Keep `maintainer.md` focused on maintainer procedures; keep `AGENTS.md` compact for future agent sessions.
