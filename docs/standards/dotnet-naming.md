# .NET naming standard

This standard applies to handwritten .NET production code and tests in this repository.
Use English names and the canonical English domain terms in `CONTEXT.md` when the domain glossary is established.
Names must describe the responsibility or behavior, and must distinguish domain concepts
from HTTP transport, persistence representations and provider implementations.

## Casing and identifiers

| Element                                                | Rule                                                      | Examples                                                                                          |
| ------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Namespaces and projects                                | PascalCase segments; match the owning project and feature | `WorkoutEditor.Api.Features.Workouts.GetWorkout`, `WorkoutEditor.Api.Infrastructure` |
| Classes, records, structs and enums                    | Singular PascalCase names                                 | `WorkoutRow`, `WorkoutExercise`, `DatabaseMigrationOutcome`                          |
| Interfaces                                             | `I` followed by a meaningful PascalCase contract name     | `IDatabaseReadiness`, `IWorkoutReader`                                                       |
| Methods                                                | PascalCase verb or verb phrase describing the operation   | `Configure`, `ApplyAsync`, `IsReadyAsync`                                                         |
| Properties and enum members                            | PascalCase                                                | `WorkoutId`, `CreatedAt`, `Inactive`                                                         |
| Constants and static readonly fields                   | PascalCase                                                | `SchemaName`, `SupportedSchemaVersion`                                                            |
| Private instance fields                                | camelCase without an underscore prefix                    | `probe`, `timeout`                                                                                |
| Parameters, local variables and constructor parameters | camelCase                                                 | `workoutId`, `cancellationToken`, `connectionString`                                         |
| Generic type parameters                                | `T`, or `T` plus a descriptive PascalCase name            | `TEntity`, `TId`, `TResult`                                                                       |
| Boolean members                                        | Name the condition using `Is`, `Has`, `Can` or `Supports` | `IsReady`, `HasActiveAdministrator`, `CanRequestAccess`                                           |

Use familiar .NET casing for abbreviations: `Api`, `Http`, `Json`, `Jwt`, `Id` and `Dto`
in identifiers, rather than all-capital fragments. Preserve established product/project names
such as `WorkoutEditor` and `PostgreSQL`, and identifiers supplied by external
frameworks. Avoid unexplained abbreviations and vague names such as `Helper`, `Manager`, `Common`,
`Data` or `Service` when the name can describe a concrete responsibility. Established
contracts retain their agreed name.

## Projects and directories

Use PascalCase project names and namespaces under `WorkoutEditor`.
Production projects live under `Backend/src` and tests under `Backend/tests`.
Organize HTTP operations under `Features/<Area>/<Operation>`.

Operation directories use PascalCase verb phrases. Keep the endpoint, validator,
mapper, request and response for one operation together. Domain types, invariants and use cases belong in Application. Provider-specific
storage belongs in Infrastructure. Local orchestration contains only startup wiring.

HTTP endpoint types use the operation name plus Endpoint, such as
CreateWorkoutEndpoint. Validators and mappers use the same operation plus
Validator or Mapper. Request and response payloads use Request and Response suffixes.
Persistence rows use a Row suffix. Async production methods returning Task or
ValueTask end in Async, except framework overrides. Cancellation parameters are named
cancellationToken and are last. Test classes end in Tests; test method names describe
behavior and need no Async suffix.

Feature namespaces follow directories, for example
WorkoutEditor.Api.Features.Workouts.CreateWorkout. Files are named
after their primary type.

## Specifications and persistence services

Name concrete queries after their purpose plus Specification, with one class per
file in the owning Application project's Specifications directory.
Persistence adapters belong in Infrastructure. Entity configuration names end in
Configuration. Keep migrations in a Migrations directory. Database identifiers
use English singular snake_case names and preserve published contracts.

## Automated checks

The root `.editorconfig` and `Directory.Build.props` enforce naming diagnostics.
Review domain terminology and responsibility boundaries. Establish additional
checks alongside the application projects.
