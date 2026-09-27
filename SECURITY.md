# Security Policy — dolphin-anty-profile-manager

## Scope

This repo holds local orchestration code only. It talks to the Dolphin Anty
desktop API on `http://127.0.0.1:3001` (default) and never phones home.
Any PR that adds outbound network calls to non-loopback hosts is rejected.

## Secrets

Profile tokens, proxy creds, and `.env` files are git-ignored. Never commit
a live `tokens.json` or `cookies/` dump. If you do, rotate immediately and
open a `security` issue.

## Threat model

- Local-only attack surface. The Dolphin Anty API is unauthenticated on
  loopback; treat any other process on the box as hostile.
- Proxy credentials are passed through to Dolphin Anty and not logged at
  `INFO`. Keep `LOG_PROXY_CREDS=0` in prod.
- The `adapters/` layer shells out to `DolphinAnty.exe` for a couple of
  legacy paths — argument lists are built with `shlex.quote`, never
  `shell=True`.

## Reporting

Open a private security advisory, or email `security@<repo-owner>.invalid`.
72h acknowledgement, 7d triage.