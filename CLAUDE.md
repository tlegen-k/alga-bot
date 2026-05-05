# CLAUDE.md — alga-bot

> **For Claude Code (WSL) or any AI coding agent.**
> Read this file completely before writing any code.
> All implementation notes and current state go in `STATUS.md` — never in this file.

---

## Absolute rules

1. **Do not modify `CLAUDE.md`.** It is the human-authored source of truth.
   All agent notes, decisions, and current state go in `STATUS.md`.
2. **Update `STATUS.md` on every "wrap up".** Before writing the session note.
3. **No secrets in repo.** All config lives in `.env` — never committed.
4. **uv only** — never pip, never requirements.txt.
5. **Kazakh is the default** — all new string keys must have a `kk` value first.
6. **Never block the event loop** — everything async.
7. **On DB error: log it, still confirm to user, don't crash.**
8. **Phase gate:** Do not work on Phase 2 tasks if Phase 1 is not complete.
   Check `STATUS.md` before starting.

---

## Business context

Telegram inquiry bot for Alga (alga.world) — Kazakhstan digital agency.
Collects leads from potential clients, saves to PostgreSQL, forwards to admin.
Primary market: Kazakhstan. Languages: KZ (default), RU, EN.

---

## Current focus

<!-- YOU update this at session start. Paste from Obsidian Agency/Plan.md. -->
- [ ] Task 1
- [ ] Task 2

---

## Stack

| Layer | Tech |
|---|---|
| Language | Python 3.11+ via **uv** |
| Framework | aiogram 3.x (async Telegram) |
| DB | PostgreSQL via asyncpg |
| Config | python-dotenv |
| Infra | Contabo VPS · systemd |

---

## Package management

- Add deps: `uv add <package>`
- Run: `uv run python -m bot.main`
- Sync: `uv sync`
- Lock file: `uv.lock` (commit this)

---

## Repo structure

```
alga-bot/
├── CLAUDE.md             ← you are here — never modify
├── STATUS.md             ← agent-maintained — update on every wrap up
├── pyproject.toml        ← deps + project metadata (uv)
├── uv.lock               ← committed lockfile
├── .env                  ← never commit
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

---

## Env vars (.env)

```
BOT_TOKEN=
ADMIN_CHAT_ID=       # your Telegram ID — new leads forwarded here
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/alga
```

---

## Internationalisation

- **Default language: Kazakh (kk)**
- Supported: `kk`, `ru`, `en`
- `get_text(key, lang)` falls back to `kk` if key missing in requested lang
- Language selector shown at `/start` as inline keyboard
- Future languages (uz, ky) = add a new file in `i18n/`, zero other changes

---

## Bot conversation flow

```
/start
  → Language picker (inline keyboard): 🇰🇿 Қазақша · 🇷🇺 Русский · 🇬🇧 English
  → Q1: Name
  → Q2: Phone
  → Q3: Service interest (Website / Telegram bot / Automation / Other)
  → Q4: Brief description of task
  → Confirmation message to user
  → Save lead to PostgreSQL
  → Forward formatted lead summary to ADMIN_CHAT_ID
```

---

## Phases

### Phase 1 — Bot live on VPS with Postgres
**Stop condition:** Bot running on VPS, leads saved to DB, admin forwarding confirmed.

- [x] FSM conversation flow (all languages)
- [x] i18n: kk (default), ru, en
- [x] PostgreSQL lead save
- [x] Admin forwarding via Telegram
- [x] systemd service on Contabo VPS
- [x] Postgres on VPS — leads persisted

### Phase 2 — Admin tooling + resilience
**Stop condition:** Admin can view leads in Telegram. Bot survives restarts mid-conversation.
*Do not start until Phase 1 stop condition is met.*

- [ ] `/leads` admin command — view last 10 leads from Telegram
- [ ] Redis FSM storage (survive bot restarts mid-conversation)

### Phase 3 — Polish + monitoring
*Do not start until Phase 2 stop condition is met.*

- [ ] Log rotation
- [ ] External monitoring / alerting
- [ ] Additional languages (uz, ky)

---

## Deployment

```bash
# On VPS
cd /home/deploy/alga-bot && git pull origin main
sudo systemctl restart alga-bot
journalctl -u alga-bot -f
```

VPS: Contabo · user: `deploy` · path: `/home/deploy/alga-bot`

---

## Obsidian vault

- Vault (WSL): `/mnt/c/Vaults/second-brain`
- Session notes: `Agency/Sessions/YYYY-MM-DD-alga-bot.md`
- Decisions log: `Agency/Decisions.md`
- Master plan: `Agency/Plan.md`

---

## End of session protocol

When the user says **"wrap up"**, do in this exact order:

1. **Update `STATUS.md`** — fill current phase, what works, open issues, next task.

2. **Write the session note** directly into the Obsidian vault:
   `/mnt/c/Vaults/second-brain/Agency/Sessions/YYYY-MM-DD-alga-bot.md`
   Sections to fill (no placeholders — write actual content):
   - ✅ Done
   - 🧠 Decisions + reasoning
   - 🪲 Issues & blockers
   - 🔜 Next session (exact first task)

3. **Run the logger:**
   ```bash
   bash ~/scripts/log-session.sh
   ```

4. **Print next session's first task** to the terminal.
