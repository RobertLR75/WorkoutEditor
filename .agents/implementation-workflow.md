# Implementation workflow

Read [agent guidance](../AGENTS.md). Inspect Git status and existing work before
editing. Preserve unrelated changes and keep requirements linked to evidence.
Use configured project conventions for branches and trackers; direct requests
require no invented work items.

For .NET work, follow the implementation standard, naming standard and relevant
ADRs. Run actual project builds and relevant unit and integration tests with the
pinned SDK. Report unavailable checks and missing prerequisites explicitly.
For documentation, inspect the final contents and relative references.

For frontend work, read [frontend rules](../docs/standards/frontend-development.md)
and [quality checks](../docs/ci/frontend.md). Use the frontend skills for design,
React composition/performance, accessibility review and browser testing when those
tasks apply. Keep tests in `Frontend/test/` even when a generic skill shows
co-located tests. Run the configured lint, format, strict typecheck, component
tests, production build and built-file checks; verify affected UI in a browser.
Until a frontend application and its scripts exist, these are setup requirements,
not runnable commands. Report that limitation without claiming application checks.

Before committing, obtain independent Standards and Spec reviews through two
read-only sub-agents. Give both the complete candidate, requirements and evidence.
Freeze edits during review and repeat affected reviews after fixes.
Commit and publish within user authorization. Report changes, validation and
remaining limitations. Preserve worktrees unless cleanup is requested.
