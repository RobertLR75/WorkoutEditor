# .NET implementation standard

This standard applies to new and changed handwritten .NET production code and tests
in this repository. Mandatory rules use **must**; preferences use **prefer**;
conditional guidance states when it applies. Generated code follows its generator.

Read the [naming standard](dotnet-naming.md) and relevant [ADRs](../adr/README.md).
Use the pinned SDK and shared build and package settings.

## Readable layout

Handwritten C# must use line breaks that expose control flow and separate responsibilities:

- Put block braces on separate lines for types, methods and control flow. Expand `if`,
  `else`, loops, `try`, `catch` and `finally` into blocks with each statement on its own
  line, including guards and short error handlers.
- Put each statement and member declaration on its own line. Separate methods and other
  block-bodied members with one blank line; keep related fields and simple auto-properties
  together. Prefer concise expression-bodied members only for simple expressions.
- Keep consecutive properties in one object initializer together without blank
  lines between each property. Use a blank line only to separate meaningful groups.
- Separate logical steps with one blank line, such as input validation, setup, I/O and
  result construction. In tests, separate Arrange, Act and Assert with blank lines.
  Keep consecutive statements within the same step together.
- Wrap long signatures, calls, conditions and fluent chains at logical boundaries.
  Prefer one parameter, argument or chained operation per line when the expression spans
  several lines. Prefer lines within 120 characters where practical; preserve literal
  content and external identifiers when splitting would alter their meaning.

For example, keep guards and error handlers visibly separate from the work they protect:

```csharp
if (timeout <= TimeSpan.Zero)
{
  throw new ArgumentOutOfRangeException(nameof(timeout));
}

try
{
  return await probe.IsReadyAsync(cancellationToken);
}
catch (TimeoutException)
{
  return false;
}
```

Apply these rules when adding or changing code; wider formatting changes belong to an
explicitly scoped formatting task. Follow `.editorconfig` for indentation and whitespace.

## Automated layout checks

The root `.editorconfig` defines whitespace and naming diagnostics. Shared build
settings enforce code style and treat warnings as errors. Review logical grouping,
Arrange/Act/Assert boundaries and the practical 120-character preference.
Add automated layout checks when the application projects are established.

## Documentation

Write XML documentation only when it tells the reader something the name, types and
signature do not: invariants, bounds, side effects, ordering or precedence, security
reasons, what cancellation does not undo, and caller-visible exceptions. Omit tags that
restate the signature, such as `<param>` for injected dependencies or `<returns>` for
"a task that completes". Endpoint `Configure` and `HandleAsync` overrides need no XML
comments: their OpenAPI text belongs in `Summary(...)`. XML comments do not reach the
OpenAPI document. Keep implementation comments focused on non-obvious reasons.
Code comments and documentation must use English.

For HTTP endpoints, verify actual routes and responses in the generated OpenAPI document
(`/openapi/v1.json`, presented by Scalar) when endpoint behavior changes. XML comments
supplement the endpoint contract.

## Design and dependency injection

Keep HTTP transport, application use cases and provider implementations separate.
Follow [ADR 0004](../adr/0004-layered-services-and-persistence.md).
Keep handlers focused on one use case. Introduce interfaces, factories or shared
bases when a concrete dependency seam or shared behavior justifies them.
Use concrete purpose-named specifications for queries beyond lookup by ID.
Persistence adapters own commits; handlers use the application persistence contract.

Prefer primary constructors for straightforward dependency injection when they keep
initialization readable. Validate required reference arguments at callable boundaries
with `ArgumentNullException.ThrowIfNull` or an equivalent guard; internal DI-only
constructors need guards when null validation is part of their intended contract.

Register dependencies through the Microsoft.Extensions.DependencyInjection composition
root of each API, which registers the handlers it serves and the `IPersistenceService<T>`
implementation as scoped. Enable DI scope validation in development and test environments.
Singleton validators and mappers must remain thread-safe and free of request state;
scoped dependencies must be resolved within their owning scope.

## Async, cancellation and resource ownership

Use asynchronous APIs for I/O and propagate `CancellationToken` through the operation.
Return `Task` or `Task<T>`; use `ValueTask` only when a measured or established contract
justifies it. Await asynchronous work rather than blocking with `.Result` or `.Wait()`.
CPU-bound work requires an execution strategy appropriate to its cost; adding `async`
or `Task.Run` to a request handler does not establish that strategy.

Use `ConfigureAwait(false)` in reusable library code when continuation context is
irrelevant; it is not a blanket requirement for ASP.NET Core request code.
Propagate caller cancellation and distinguish it from an operation's own timeout.

Dispose resources owned by the operation with `using` or `await using` as appropriate.
Let the DI container dispose container-owned services. Background work must have explicit
lifetime, cancellation, failure reporting and scope ownership.

## Validation and configuration

Use strongly typed configuration and options binding; validate required settings
before accepting work. Use data annotations or custom validators when they express the
actual configuration constraints. HTTP input validation follows the API's validation
contract, such as FastEndpoints/FluentValidation; domain models enforce their own
invariants.

Keep configuration keys compatible. Follow the Host's environment, appsettings and
secret-provider behavior. Credentials and tokens must remain outside committed
configuration, documentation and logs.

## Errors, logging and localization

Represent expected use-case outcomes through typed results. Catch exceptions where the
operation can recover, add actionable context or translate a technical failure into the
owning contract. Preserve exception causes and stack traces; allow unexpected failures
to reach the error boundary.

Use structured Microsoft.Extensions.Logging message templates with meaningful named
properties. Use logging scopes when several events share an operation identity. Log
failures at the responsible boundary, avoiding repeated logging of the same exception.
Follow the published Problem Details and masked-error contract. Logs must exclude credentials,
tokens and sensitive payloads.

Use resources when a feature requires localized user-facing text. Keep localization
behind a cohesive message interface and retain stable machine-readable error codes.
ResourceManager, resource-file separation and GetString calls are implementation choices
for that need, rather than requirements for every message or log event.

## Testing and verification

Use xUnit as the test framework and Shouldly for new or changed value, collection
and boolean assertions. For example, use `actual.ShouldBe(expected)` and
`result.ShouldNotBeNull()`. Add the pinned Shouldly dependency to a test project
when adopting it there. Existing tests can migrate in scoped changes; a touched
assertion does not require converting every assertion in the solution.
Retain xUnit exception assertions when their exact-type or derived-type behavior
is part of the test contract; any replacement must preserve those semantics.
Structure tests as Arrange,
Act and Assert, with descriptive scenario names. Prefer small deterministic stubs for
use-case dependencies; introduce a mocking library only for a demonstrated need.

Cover successful behavior, meaningful failures, boundaries and cancellation relevant to
the changed contract. Test null validation where callers rely on that contract rather
than adding repetitive guard tests to every internal constructor.

Keep unit and integration tests with their owning project. Filter integration
cases by Category=Integration and measure unit coverage separately; require strictly
more than 90 % line coverage of handwritten production code. Test pure use-case
decisions with unit tests and provider behavior against the actual provider.
Before delivery, run the actual solution build, relevant unit tests and affected
integration tests. Establish project-specific commands when projects are created.

## Security, performance and integrations

Use parameterized database commands and established mappings. Validate external
input at its boundary and preserve database and wire contracts. Implement feature
requirements for authentication, authorization and secret handling explicitly.

Bound work and data retrieval according to the operation contract. Optimize demonstrated
bottlenecks using measurements rather than introducing speculative caching or concurrency.

AI libraries, model settings and structured-output mechanisms belong to features that
actually require AI integration. Select and validate them through the feature's concrete
requirements and applicable architecture decisions.
