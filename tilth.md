# Tilth Setup Notes

Use this as a reusable checklist for enabling Tilth in other projects and documenting it in that project's `AGENTS.md`.

## Install For OpenCode

Install Tilth as an OpenCode MCP server with edit-mode tools:

```bash
tilth install opencode --edit
```

Observed result:
- Updates `/home/user/.config/opencode/opencode.json`.
- Installs at user scope, so Tilth is available in all projects.
- Edit mode enables hash-anchored editing tools in addition to read/search/diff tools.

## Common CLI Usage

Use the CLI when you need structural reads or diffs from a shell:

```bash
tilth AGENTS.md --budget 7000
tilth hashmeter.py --section 45-89
tilth HashMeter --scope . --expand
tilth analyze_hashmeter_data --scope . --callers
tilth hashmeter.py --deps
tilth grok HashMeter
tilth diff
```

Prefer these over ad hoc `cat`, broad grep, or raw `git diff` when structural context matters.

## MCP Tool Equivalents

Use the MCP tools when available in OpenCode:
- `tilth_read` for smart file reads and line/heading sections.
- `tilth_search` for symbols, content, regex, and callers.
- `tilth_files` for glob-style file discovery.
- `tilth_diff` for structural diffs.
- `tilth_deps` before signature/export behavior changes.
- `tilth_grok` when you need definition, callers, callees, siblings, and tests for one symbol.
- `tilth_write` when edit mode is enabled and you are doing hash-anchored edits.

Tool caveat: pass either `pattern` or `patterns` to `tilth_files`, not both.

## Suggested AGENTS.md Snippet

Add a short repo-local section like this, adjusting examples to the project's language and layout:

```markdown
## Tooling
- Use Tilth for structural code reading and diffs: `tilth <file>`, `tilth <file> --section 45-89`, `tilth <symbol> --scope . --expand`, and `tilth diff`.
- Use Tilth MCP tools when available for the same jobs: `tilth_read`, `tilth_search`, `tilth_files`, `tilth_diff`, `tilth_deps`, and `tilth_grok`.
- Use `tilth_files` with either `pattern` or `patterns`, never both.
- Prefer Tilth for reading whole files, targeted sections, symbol searches, caller/dependency checks, and function-level diffs; use exact search only when matching a literal string.
```

For projects that allow MCP edit mode, add:

```markdown
- When Tilth edit mode is available, use `tilth_write` for hash-anchored edits after reading the target lines with `tilth_read`.
```

## When To Update AGENTS.md

Update the project `AGENTS.md` after installing or changing Tilth usage when:
- Tilth becomes the preferred structural read/search/diff tool.
- Edit mode is enabled and agents should use `tilth_write`.
- The repo has local caveats, such as generated directories, large files, or language-specific entrypoints that affect Tilth usage.
