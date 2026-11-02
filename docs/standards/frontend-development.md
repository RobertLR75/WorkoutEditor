# React and frontend development

Apply these rules to new and changed frontend code, styles and tests. This repo
currently contains guidance only; application files, npm scripts and CI are not
installed by this import. The [frontend ADR](../adr/0005-react-typescript-bff.md)
keeps the BFF integration proposal distinct from implemented behavior.

## Foundation and tooling

Use React and strict TypeScript with Vite and React Compiler. Vite builds static
files; Node is a development, build and test runtime. Vite preview is for local
verification. It is neither production hosting nor a BFF.
Use Tailwind CSS and versioned shadcn/ui components, with TanStack Query for server
state. Keep the dependency graph and tooling compatible when choosing versions.

When creating the application, pin Node in `Frontend/.nvmrc`, declare supported
Node/npm versions and `packageManager` in `package.json`, and commit the npm
lockfile. Use `npm ci` for reproducible installation. Check TypeScript support in
typescript-eslint before compiler upgrades. Keep runtime documentation and pins
in sync; source-project version numbers are not verified recommendations here.

Keep application code in `Frontend/src/` and tests in `Frontend/test/`. Mirror
source paths and use `*.test.ts` or `*.test.tsx`; configure Vitest to collect only
`test/**/*.test.{ts,tsx}`. Resolve `@/*` to `src/*` in both TypeScript and Vite.

## Components, state and rendering

Use composition and focused component APIs. Consult
[React composition patterns](../../.agents/skills/vercel-composition-patterns/SKILL.md)
for component boundaries and
[React best practices](../../.agents/skills/vercel-react-best-practices/SKILL.md)
for performance work. Browser rules apply to Vite; Next.js, React Server Components
and server actions require an explicitly adopted runtime.

Enable React Compiler in the Vite pipeline and React Hooks/Compiler diagnostics
in ESLint. Verify actual compiler-generated memo-cache operations in served
development code and a production build; the presence of React's runtime alone
does not prove compilation. Generated names and cache-slot counts can change.

Create one stable QueryClient outside rendering and provide it through
QueryClientProvider. Choose stale time, retries and refetch behavior for the
specific operation. Keep API tokens and secrets out of query data and storage.
Tests create their own QueryClient per test, unmount after each case and clear
the cache; they never import the application-wide client or browser entry point.

## Styling and accessibility

Keep shared colors, radii, fonts and theme values in `src/index.css`. Keep copied
shadcn components in `src/components/ui/` and the `cn` helper in `src/lib/utils.ts`.
Add only components needed by a feature. Preview changes with the locked shadcn
CLI's `--dry-run` before adding; inspect dependencies, lockfile, CSS, helper files
and environment changes. Preserve local component edits when considering overwrite.

Use [frontend design](../../.agents/skills/frontend-design/SKILL.md) for UI creation
and [web design guidelines](../../.agents/skills/web-design-guidelines/SKILL.md)
for UI/accessibility reviews. Existing project rules and accessibility needs take
precedence over stylistic suggestions. Component libraries do not prove accessible
usage: check semantics, accessible names, keyboard operation and visible focus.
Use appropriate document language, landmarks, a clear heading hierarchy and a
keyboard-visible skip link that moves focus to main content.

Verify changed UI in development and built preview at narrow and desktop widths
(320 x 740 and 1440 x 900 CSS pixels are baseline cases). Check readability,
overflow, layout, keyboard navigation, console errors and expected network activity.

## Formatting and static analysis

Use ESLint as the frontend linter: recommended JavaScript and TypeScript rules,
React Hooks/Compiler, TanStack Query and Fast Refresh checks. Errors and warnings
fail lint. Include application sources, tests, copied UI components and tooling;
use browser and Node globals only in their respective scopes. Ignore build output.

Use Prettier with single quotes, no JavaScript semicolons and the Tailwind plugin.
Read Tailwind v4 theme values from `src/index.css` and sort classes in JSX and
`cn`/`cva` calls. Root EditorConfig supplies whitespace rules. Ignore dependencies,
build output and the generated package lockfile in formatting checks.

Set `strict: true` and `noEmit: true` for application and tooling TypeScript
projects. Check unused locals/parameters and switch fallthrough. Keep incremental
metadata under `node_modules/.tmp/`. Run `tsc -b` independently and before bundling;
Vite's TypeScript transform alone is not a typecheck.

## Tests and delivery

Use Vitest with jsdom, React Testing Library and jest-dom. Share the application's
Vite plugins, compiler and alias configuration. Test user-visible behavior and
meaningful boundaries, using accessible queries. Keep unit/component tests isolated
from live services, credentials and environment files.
Use [webapp testing](../../.agents/skills/webapp-testing/SKILL.md) for browser checks.
The optional [TypeScript module setup](../../.agents/skills/setup-ts-deep-modules/SKILL.md)
is user-invoked; its examples do not override this repo's test placement.

Follow [frontend quality checks](../ci/frontend.md). Do not carry verification
claims from another application into this repo.

## Configuration and security

`VITE_*` values are public client configuration embedded in built files. Keep
credentials, keys, access/refresh/ID tokens and server settings outside frontend
sources, client responses, URLs and logs. Treat the browser bundle as public.
Review added environment files before committing; keep local overrides untracked.

Protected browser requests use the same-origin BFF when that proposal is adopted.
Keep tokens server-side and use an HttpOnly, Secure session cookie with explicit
CSRF protection. Local development must preserve these boundaries rather than
moving tokens into browser storage or relaxing cookie security.
