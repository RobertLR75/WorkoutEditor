# Domain Docs

## Before exploring

This repo uses a single-context layout. `CONTEXT.md` is its glossary: whenever an engineering skill says to read, create, or update `GLOSSARY.md`, use `CONTEXT.md` here. Keep domain vocabulary in this one file.

- Read `CONTEXT.md` at the repo root for domain terms and their definitions.
- Read relevant architecture decision records in the root `docs/adr/` directory before working in an area they cover.

If these files do not exist, proceed silently. The `domain-modeling` skill creates them as terms or decisions are resolved; this setup does not create placeholder domain documentation.

## Use the glossary's vocabulary

When naming domain concepts in issues, proposals, hypotheses, or tests, use the terms defined in `CONTEXT.md`. If a needed concept is missing, check whether the project already has a term for it; record a real vocabulary gap for `domain-modeling`.

## Surface ADR conflicts

If a proposed change contradicts an existing ADR, identify the ADR and explain why the decision should be revisited before overriding it.
