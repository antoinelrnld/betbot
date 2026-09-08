# BetBot frontend

This is the Next.js App Router frontend foundation for BetBot. The current
home page is intentionally a static, responsive shell; product functionality
will be added in later issues.

## Development

```bash
npm ci
npm run dev
```

Set `NEXT_PUBLIC_API_BASE_URL` when the backend is not running at its local
default. See `.env.example` for the supported configuration.
