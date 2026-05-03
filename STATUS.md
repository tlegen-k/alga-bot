# STATUS.md — alga-bot

## Phase
Phase 1 / Week 2 — Bot built and tested locally

## Current state
🟡 Working — bot functional, DB pending

## What works
- `/start` → language picker (kk/ru/en) → name → phone → service → task → thank you
- Admin lead summary forwarded to ADMIN_CHAT_ID via Telegram (confirmed working)
- i18n system: kk (default), ru, en — full string coverage
- Graceful DB skip: if DATABASE_URL empty, bot runs fine, logs warning on lead save
- systemd unit file ready for VPS deploy
- uv project: pyproject.toml + uv.lock committed

## What's broken / in progress
- DB save fails (no Postgres running locally) — expected, non-blocking
- DATABASE_URL not set in .env

## Open issues
- Need Postgres: local or on Contabo VPS
- Set DATABASE_URL=postgresql+asyncpg://user:pass@host/alga in .env
- On VPS: copy deploy/alga-bot.service to /etc/systemd/system/, set correct User= and WorkingDirectory=

## Next task
1. Set up PostgreSQL (local or VPS)
2. Add DATABASE_URL to .env
3. Run `uv run python -m bot.main` — init_db() auto-creates leads table
4. Test full flow with DB — verify lead saved in DB
5. Deploy to Contabo: scp project, copy service file, systemctl enable + start

## Decisions log
- uv for package management — pyproject.toml, no requirements.txt
- aiogram 3.x — modern async API, better FSM
- MemoryStorage for FSM (Redis later in Phase 3)
- asyncpg for DB — consistent async pattern
- Kazakh (kk) as default language — i18n-first from day one
- i18n via simple dict files per language — no external lib needed at this scale
- Lead forwarded to ADMIN_CHAT_ID as formatted message (no n8n, keep simple)
- DB skip when DATABASE_URL empty — allows local dev/testing without Postgres
- VPS: Contabo, bot username: @AlgaWorldBot
