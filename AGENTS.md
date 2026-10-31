# WorkoutEditor agent guidance

Skills live in `.agents/skills`; `skills-lock.json` records their sources.
Before implementation, read [.agents/implementation-workflow.md](.agents/implementation-workflow.md).
Before writing or reviewing .NET code or tests, read
[implementation rules](docs/standards/dotnet-implementation.md),
[naming rules](docs/standards/dotnet-naming.md) and relevant [ADRs](docs/adr/README.md).
Use the pinned SDK and shared build and package properties.
Before domain work, read [domain guidance](docs/agents/domain.md).
Preserve user changes and honor the requested scope and publication authorization.
