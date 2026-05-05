# STATUS.md — alga-bot

## Phase
Phase 2 — Bot deployed to VPS, Postgres live on both local and VPS

## Current state
🟢 Fully working — bot running, leads saved to PostgreSQL

## What works
- `/start` → language picker (kk/ru/en) → name → phone → service → task → thank you
- Admin lead summary forwarded to ADMIN_CHAT_ID via Telegram ✓
- i18n system: kk (default), ru, en — full string coverage ✓
- Leads saved to PostgreSQL (both local and VPS) ✓
- Graceful DB skip: if DATABASE_URL empty, bot runs, logs warning ✓
- systemd service: auto-starts on reboot, restarts on crash ✓
- Bot running as systemd service on Contabo VPS (user: deploy) ✓
- Bot username: @AlgaWorldBot ✓

## Infrastructure
- VPS: Contabo, user: deploy, path: /home/deploy/alga-bot
- Postgres: local (WSL2) + VPS, DB: alga, user: algabot
- systemd: alga-bot.service, enabled + running
- Logs: `journalctl -u alga-bot -f`

## Open issues
- None blocking

## Next tasks (Phase 3)
1. Add /leads admin command — view recent leads from Telegram
2. Switch FSM storage from MemoryStorage to Redis (survive restarts)
3. Add more languages (uz, ky) if needed
4. Set up log rotation or external monitoring

## Decisions log
- uv for package management — pyproject.toml, no requirements.txt
- aiogram 3.x — modern async API, better FSM
- MemoryStorage for FSM (Redis later in Phase 3)
- asyncpg for DB — consistent async pattern
- Kazakh (kk) as default language — i18n-first from day one
- i18n via simple dict files per language — no external lib needed at this scale
- Lead forwarded to ADMIN_CHAT_ID as formatted message
- DB skip when DATABASE_URL empty — allows local dev without Postgres
- PostgreSQL on VPS (not SQLite) — already had asyncpg, production-ready
