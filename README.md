# VeloxaHost API examples

Small, working examples for the [VeloxaHost REST API](https://docs.veloxahost.com/api/overview.html): create servers, restart them, add storage and alerts — from bash, Python or CI.

Base URL: `https://console.veloxahost.com/api/v1` · Auth: `Authorization: Bearer <key>`

## Setup

1. Create a key in the console: **Settings → API Keys**. Give it only the scopes you need (e.g. `instances:read instances:write`), an expiry, and an IP allow-list.
2. Export it — never commit it:

```bash
export VELOXA_API_KEY="veloxa_..."
```

## Examples

| File | Does |
|---|---|
| `bash/list-instances.sh` | List servers with status |
| `bash/create-instance.sh` | Create an Ubuntu 24.04 container |
| `bash/restart-instance.sh` | Restart a server |
| `python/veloxa.py` | Tiny client: list, create, state change, volumes, alert rules — with rate-limit handling |
| `github-actions/restart-on-deploy.yml` | Restart a server from CI after a deploy |

## Rate limits

60 requests/min per key per `/api/v1` endpoint. Responses include `X-RateLimit-Remaining` and `X-RateLimit-Reset`; a 429 includes `Retry-After`. The Python client retries automatically.

## Don't have an account?

[Start a free 14-day trial](https://veloxahost.com/?utm_source=github&utm_medium=referral&utm_campaign=api-examples) — no card required.

## License

MIT
