# Frontend quality checks

These are requirements for the future frontend tooling. No npm application or CI
job currently exists in this repository. Configure these scripts when creating
`Frontend/`, then run them from that directory after `npm ci`:

```sh
npm run lint
npm run format:check
npm run typecheck
npm test
npm run build
npm run verify:dist
```

Each command must be non-interactive and exit nonzero on violations. Lint fails on
warnings as well as errors. Build runs strict typechecking before Vite bundling.
Test runs Vitest once, collecting `test/**/*.test.{ts,tsx}`. See
[frontend development](../standards/frontend-development.md) for rule coverage.

## Built-file verification

Implement `verify:dist` to serve the production build through Vite preview on a
free loopback port. Request the start page and each referenced script/stylesheet.
Require successful HTTP status, correct content types and nonempty assets. Check
the application's language, title, root, expected content and compiled Tailwind
styles; reject references to source files. Verify React Compiler-generated
memo-cache output separately from React's runtime. Always stop the preview server,
including on failure. This text/asset check supplements component and real-browser
checks; it does not execute the bundle or prove layout and keyboard behavior.

## CI requirements

When configuring CI, use the pinned Node/npm runtime, verify it against `.nvmrc`
and install exactly from the committed lockfile. Cache npm downloads keyed by the
lockfile rather than `node_modules`. Run frontend checks on changes to the frontend
or its pipeline/configuration, with every check blocking delivery on failure.
Preserve existing backend checks. If using container images, pin and verify their
digest and runner platform when updating the runtime.

Keep copied shadcn components versioned; CI builds them without fetching new
components. Remove inherited `VITE_*` values before installation/build unless
explicitly allowlisted as public configuration. Pass no secrets into client builds.
If producing test reports, emit JUnit output as required by the selected CI host.

## Verification evidence

Validate from a clean installation without `node_modules`, `dist`, credentials or
local environment files. Check that representative lint, format and strict-type
violations fail their gates, including copied UI components. Check built-file
verification against missing builds, empty assets and absent compiler output.
Remove temporary probes and rerun affected checks. Record actual local and CI
results separately; local success does not prove a hosted pipeline ran.
