---
name: git-guardrails-claude-code
description: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
---

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

The hook inspects literal commands, including Git global options, combined short flags,
and `sh`/`bash`/`zsh -c` commands. It does not execute commands or resolve aliases,
shell functions or dynamically constructed command names; use it as an accidental-operation guard.
Use `$(...)` for nested substitutions; escaped nested backticks are rejected.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Check the runtime and copy both hook files

Run `python3 --version` in the environment where Claude Code runs. Python 3.8 or newer
must be on its PATH before enabling the hook; install it if missing and repeat the check.
The hook uses only Python's standard library and does not require `jq`.

Copy [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh) and
[scripts/block-dangerous-git.py](scripts/block-dangerous-git.py) into the same directory:

- **Project**: `.claude/hooks/`
- **Global**: `~/.claude/hooks/`

Make `block-dangerous-git.sh` executable with `chmod +x`. Missing Python, a missing
helper, invalid JSON or an unreadable command cause exit 2, blocking execution.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array. Don't overwrite other settings.

### 4. Ask about customization

Ask if user wants to add or remove any commands from the blocked list. Edit the copied Python helper accordingly.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Should exit with code 2 and print a BLOCKED message to stderr.

Repeat with `git -C /workspace push origin main` and `git clean -df`; both must
exit 2. A payload with `git status` must exit 0. Invalid input such as `{}` must
exit 2. Pass these as JSON input to the hook; the Git commands themselves are not run.
