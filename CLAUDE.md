# CLAUDE.md — alga-bot

## Project
Agency inquiry bot for Alga (alga.world) — Kazakhstan digital agency.
Collects leads from potential clients via Telegram.
Runs as a systemd service on Contabo VPS.

## Stack
- Python 3.11+ managed with **uv** (pyproject.toml, never requirements.txt)
- aiogram 3.x (async Telegram framework)
- PostgreSQL — leads table (name, phone, service_interest, message, lang, created_at)
- python-dotenv — env vars
- asyncpg — async PG driver

## Package management
- **Always use uv.** Never requirements.txt, never pip directly.
- Add deps: `uv add aiogram asyncpg python-dotenv`
- Run: `uv run python -m bot.main`
- Sync: `uv sync`
- Lock file: `uv.lock` (commit this)

## Repo structure
```
alga-bot/
├── CLAUDE.md             ← you are here
├── STATUS.md             ← current build state (agent-maintained)
├── pyproject.toml        ← deps + project metadata (uv)
├── uv.lock               ← committed lockfile
├── .env.example          ← template, never commit .env
├── bot/
│   ├── main.py           ← entry point, bot init
│   ├── config.py         ← load env vars
│   ├── i18n/
│   │   ├── __init__.py   ← get_text(key, lang) helper
│   │   ├── kk.py         ← Kazakh strings (default)
│   │   ├── ru.py         ← Russian strings
│   │   └── en.py         ← English strings
│   ├── handlers/
│   │   └── inquiry.py    ← /start + FSM conversation
│   └── db/
│       ├── connection.py
│       └── leads.py      ← save_lead()
└── deploy/
    └── alga-bot.service  ← systemd unit file
```

## Env vars (.env)
```
BOT_TOKEN=
ADMIN_CHAT_ID=       # your Telegram ID — new leads forwarded here
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/alga
```

## Internationalisation
- **Default language: Kazakh (kk)**
- Supported now: `kk`, `ru`, `en`
- Architecture: `bot/i18n/` — one file per language, dict of string keys
- `get_text(key, lang)` falls back to `kk` if key missing in requested lang
- User's chosen language stored in FSM state and saved to DB with the lead
- Language selector shown at `/start` as inline keyboard before any questions
- Future languages (uz, ky, etc.) = add a new file in `i18n/`, zero other changes

## Bot conversation flow
```
/start
  → Language picker (inline keyboard): 🇰🇿 Қазақша · 🇷🇺 Русский · 🇬🇧 English
  → All subsequent messages in chosen language
  → Q1: Name
  → Q2: Phone
  → Q3: Service interest (inline keyboard: Website / Telegram bot / Automation / Other)
  → Q4: Brief description of task
  → Confirmation message to user
  → Save lead to PostgreSQL (with lang field)
  → Forward formatted lead summary to ADMIN_CHAT_ID
```

## Absolute rules
- **uv only** — never pip, never requirements.txt
- Use aiogram 3.x FSM (MemoryStorage for now, Redis later)
- Kazakh is the default — all new string keys must have a `kk` value first
- Never block the event loop — everything async
- Validate phone loosely (accept any string, don't reject users)
- On DB error: log it, still confirm to user, don't crash

## Deployment (VPS)
- VPS: Contabo, domain alga.world
- Copy `deploy/alga-bot.service` to `/etc/systemd/system/`
- `systemctl enable alga-bot && systemctl start alga-bot`
- Logs: `journalctl -u alga-bot -f`
- Run bot via: `uv run python -m bot.main`

## Wrap up protocol
When I say "wrap up", you must:
1. Update STATUS.md — what works, what's broken, current phase, next task
2. Print a session summary I can paste into Obsidian:
   - What was built
   - Decisions made (with reasoning)
   - Blockers / open questions
   - Exact first task for next session

## Current focus
<!-- Paste today's tasks here before starting -->
- Build the inquiry bot: /start handler + FSM conversation flow
- i18n system: kk (default), ru, en
- Save leads to PostgreSQL (including lang field)
- Forward new lead to admin via Telegram message
- Generate systemd unit file for VPS deployment