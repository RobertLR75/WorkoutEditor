# WorkoutEditor agent guidance

Skills live in `.agents/skills`; `skills-lock.json` records their sources.
Before implementation, read [.agents/implementation-workflow.md](.agents/implementation-workflow.md).
Before writing or reviewing .NET code or tests, read
[implementation rules](docs/standards/dotnet-implementation.md),
[naming rules](docs/standards/dotnet-naming.md) and relevant [ADRs](docs/adr/README.md).
Use the pinned SDK and shared build and package properties.
Before implementing or reviewing React, TypeScript, CSS or frontend tests, read
[frontend rules](docs/standards/frontend-development.md) and the relevant
[frontend ADR](docs/adr/0005-react-typescript-bff.md).
For React performance, consult `.agents/skills/vercel-react-best-practices/SKILL.md`;
for component APIs, consult `.agents/skills/vercel-composition-patterns/SKILL.md`.
Apply browser/Vite guidance to this project; Next.js and server-component rules
apply only if that runtime is explicitly adopted.
Frontend tests belong in `Frontend/test/`, mirroring `src/`, never beside source.
Repository test-placement rules override generic skill examples.
Before domain work, read [domain guidance](docs/agents/domain.md).
Preserve user changes and honor the requested scope and publication authorization.
