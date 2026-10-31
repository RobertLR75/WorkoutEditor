# Layered services and persistence

Status: Accepted as development guidance.

## Decision

Separate HTTP transport (Api), use cases and domain invariants (Application), and
provider implementations (Infrastructure). The Api is the composition root.
Compile-time dependencies point toward Application and remain acyclic.
Application contains no HTTP framework or database provider types.

Keep each operation's endpoint, request, response, validator and mapper together.
Handlers live in Application and coordinate one use case. Mappers translate models;
domain models enforce invariants. Introduce abstractions for concrete seams.

Persist through application-owned contracts. Persistence write methods own their
commit. A use case makes one persistence write call; related changes are committed
atomically by Infrastructure. Keep explicit transaction orchestration out of handlers.
Represent queries beyond lookup by ID with concrete purpose-named specifications.

Propagate cancellation. Register request-scoped handlers and persistence adapters
with scoped lifetimes. Keep singleton dependencies thread-safe and free of request
state. Validate DI scopes in development and tests.

## Consequences and verification

Use cases can be tested without HTTP or a database. Verify provider-specific
behavior with the real provider in integration tests. Review dependency direction,
commit boundaries and domain invariants. Use xUnit and Shouldly, deterministic
unit tests and strictly more than 90 % unit line coverage of handwritten code.

Use English code names and comments. HTTP contracts document actual routes,
validation, responses and authorization through OpenAPI when HTTP APIs exist.
Choose frameworks, database providers and authentication from concrete requirements.
