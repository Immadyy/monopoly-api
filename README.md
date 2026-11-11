# Monopoly Banker API

A backend for a digital banker and money tracker for the physical board game *International Business* (a Monopoly-style game). Players keep playing on the real board; the app replaces the paper money and the banker's notebook, so payments are fast, correct and visible to everyone at the table.

> **Status: work in progress.** Built step by step as a learning project. See the roadmap below for what works today.

## Why

In a long board game, paying rent, collecting salary and settling debts with paper money is slow and error-prone, and the banker has to keep track of everything. This API keeps every player's balance and records each money movement, so nobody has to do the maths or argue about who paid what.

## What it does (and doesn't)

- Tracks **money only**. Properties, houses, rent, jail and passport stay on the physical board.
- A game is created with a short **join code**; players join with that code.
- Every payment is a **ledger entry** (who paid whom, how much, when). The bank is represented as "no player" (`NULL`) in the ledger.
- All transactions are visible to everyone in the game, which keeps play honest.

## Tech stack

- Python 3.13
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) with PostgreSQL
- [uv](https://docs.astral.sh/uv/) for dependency management

## Project structure

```
app/
  main.py          # FastAPI app and router registration
  api/             # route handlers (HTTP layer)
  schemas/         # Pydantic models that validate incoming requests
  models/          # SQLAlchemy models (database tables)
  services/        # business rules (e.g. money transfers)
  repositories/    # database queries
  core/            # configuration and database setup
```

## Getting started

### Prerequisites

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running PostgreSQL database

### Setup

```bash
git clone <your-repo-url>
cd monopoly-api
uv sync
```

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/monopoly_bank
```

### Run the server

Run from the project root (the folder containing `pyproject.toml`):

```bash
uv run fastapi dev app/main.py
```

Open http://127.0.0.1:8000/docs for the interactive API documentation.

## API

| Method | Path | Description | Status |
| ------ | ---- | ----------- | ------ |
| GET | `/` | Health check | Done |
| POST | `/games` | Create a game and get its join code | Done |
| POST | `/players` | Join a game with a join code and a name | Done |
| POST | `/transfer` | Move money between players, or to/from the bank | In progress |
| GET | `/games/{join_code}/players` | List players and balances | Planned |
| GET | `/games/{join_code}/transactions` | Transaction history | Planned |

### Data model

- **games**: id, join code, current round, created at
- **players**: id, game, name, balance, is banker, is playing
- **transactions**: id, game, from player, to player, amount, type, note, created at

## Roadmap

- [x] Project setup, database connection, models
- [x] Create a game, join a game
- [ ] Money transfers with balance checks (one atomic commit per payment)
- [ ] Balances and history endpoints
- [ ] Player identity and banker-only actions
- [ ] Rounds and one-tap banker actions
- [ ] Credit card debt and net worth
- [ ] Web frontend and deployment

## What I'm learning

SQLAlchemy sessions and transactions, request validation with Pydantic, layered API structure, HTTP status codes, and designing a ledger so balances can always be traced back to transactions.
