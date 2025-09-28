# ACJS — Start the Django server with uv

This project is configured to run with uv (Astral’s ultra-fast package manager). A handy `serve` command has been added in `pyproject.toml` to start the Django development server.

## Prerequisites
- Python 3.13 installed
- uv installed:
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `irm https://astral.sh/uv/install.ps1 | iex`
  - Docs: https://docs.astral.sh/uv/

## Install dependencies
From the project root:

1) Create/select the environment (uv automatically creates and manages an isolated environment):
- Nothing special to do; `uv` handles this for you by default.

2) Install project dependencies:
- `uv sync`
  - Optional: include dev/test deps: `uv sync --group dev --group tests`

## Initialize the database
- Apply migrations: `uv run python manage.py migrate`
- (Optional) Create a superuser: `uv run python manage.py createsuperuser`

## Start the development server
- Command: `uv run serve`
- By default, the server listens on `http://0.0.0.0:8000` (also accessible via `http://localhost:8000`).

## Other useful commands
- Run tests: `uv run pytest`
- Create/apply migrations (if you change models):
  - Create migrations: `uv run python manage.py makemigrations`
  - Apply: `uv run python manage.py migrate`
- Open a Django shell: `uv run python manage.py shell`

## Troubleshooting
- “uv: command not found”: install uv (see Prerequisites) and reopen your terminal.
- Port 8000 in use: run on another port: `uv run python manage.py runserver 0.0.0.0:8080`
- Dependency problems: re-sync: `uv sync --reinstall`

## Where is the `serve` command configured?
In `pyproject.toml`:

```
[tool.uv.scripts]
# Start the Django development server
serve = "python manage.py runserver 0.0.0.0:8000"
```

You can tweak this line if you want to change the port or add options (e.g. `--insecure`, etc.).
