# BetBot frontend

This is the Next.js App Router frontend foundation for BetBot. The current
home page is intentionally a static, responsive shell; product functionality
will be added in later issues.

## Development

```bash
npm ci
npm run dev
```

## Quality checks

```bash
npm run format:check
npm run lint
npm run typecheck
npm run build
```

Run `npm run format` to apply the frontend formatter.

Set `NEXT_PUBLIC_API_BASE_URL` in `.env.local` when the backend is not running
at its local default. Variables prefixed with `NEXT_PUBLIC_` are embedded in
browser code, so this file must never contain backend, Discord, OAuth, or other
secret values. See `.env.example` for the supported public configuration.
