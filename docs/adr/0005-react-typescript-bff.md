# React and TypeScript behind an ASP.NET Core Backend-for-Frontend

Status: Proposed. This records the imported frontend architecture for evaluation
in WorkoutEditor; it does not claim that a frontend, authentication or BFF exists.

## Context and proposal

Use React and TypeScript, built with Vite and React Compiler, with Tailwind CSS,
shadcn/ui, TanStack Query, ESLint and Vitest. Build static assets instead of a
Next.js application server. For authenticated features, an ASP.NET Core BFF serves
those assets and owns the browser session and API calls on one origin. This keeps
access and refresh tokens out of scripts running in the browser.

## Authentication and sessions

The BFF is a confidential OpenID Connect client using authorization code and PKCE.
Keep ID, access and rotating refresh tokens on the server; choose provider,
scopes and client authentication from the actual integration requirements.
The browser receives only a random session identifier in a `__Host-` cookie with
HttpOnly, Secure, SameSite=Strict, Path=/ and no Domain. Preserve the OIDC handler's
callback-compatible correlation/nonce cookie behavior. The first page load after
a cross-site sign-in redirect may lack the Strict session cookie; static assets
must not depend on that cookie, and following same-origin calls can send it.

The proposed baseline expires sessions after 30 idle minutes or 8 hours total,
revokes refresh tokens on expiry/sign-out and removes the local session. Provider
sign-out is part of the integration. Without back-channel logout, idle expiry
bounds a session left open elsewhere. An in-memory store works only with one
replica and loses sessions on restart; multiple replicas require shared storage.
Confirm these tradeoffs before acceptance and deployment.

## Request and HTTP boundaries

Serve static pages at `/`; reserve `GET /bff/login`, `GET /bff/user` and
`POST /bff/logout` for session operations. The user endpoint returns minimal
identity data or 401. Forward only approved `/api/*` routes to the backend via
YARP, adding the server-held bearer token. The BFF is not a general proxy.
Backend APIs validate issuer, audience, signature, expiry and operation-specific
authorization even when ingress is internal.

Require `X-CSRF: 1` on `/api/*` and `GET /bff/user`, with no cross-origin CORS
access. Reject unsafe-method requests with missing or foreign Origin, including
form-based logout. HttpOnly cookies alone do not provide CSRF protection.

The proposed production headers are Content-Security-Policy with
`default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'`,
HSTS, X-Content-Type-Options: nosniff and
Referrer-Policy: strict-origin-when-cross-origin. Verify the actual build and UI
against this policy; avoid inline scripts/styles in production assets.

In development, the browser still uses the BFF origin, which proxies Vite pages
and the HMR WebSocket. Any development-only CSP allowances must stay out of
production. Decide HTTPS/cookie handling before implementing local sign-in;
do not weaken Secure cookies or move tokens to the client.

## Alternatives and consequences

A token-holding SPA exposes credentials to page scripts. A BFF adds server-side
session lifecycle, CSRF, logout and proxy responsibilities. Framework-based OIDC
and YARP avoid a separate commercial BFF dependency but require explicit tests
of these boundaries. Distributed session storage is deferred until scaling needs
justify it. Keeping the BFF separate from application use cases preserves their
different responsibilities, consistent with [layering](0004-layered-services-and-persistence.md).

Before accepting this proposal, settle identity provider/client contracts,
deployment topology, session storage/lifetimes, logout, concrete API routes and
permissions, BFF ownership, static asset delivery and the local development setup.
