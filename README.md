# Skarion Job Scraper

A Flask dashboard and scheduled scraper for candidate-specific USA job matching. The app stores candidates and jobs in a SQL database, scrapes LinkedIn and Dice, filters out senior roles and US-citizenship-required roles, scores matches by candidate skills, and lets users mark jobs as `New`, `Applied`, or `Dismissed`.

## Tech stack

- Flask + Flask-SQLAlchemy
- PostgreSQL on Neon for production
- SQLite fallback for local development
- Render web service for the dashboard/API
- GitHub Actions scheduled workflow for background scraping every 4 hours

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

Run a local scrape once:

```bash
source .venv/bin/activate
python scraper.py
```

Run the local blocking scheduler:

```bash
source .venv/bin/activate
python scheduler.py
```

## Production architecture

Recommended production setup:

1. Neon hosts the PostgreSQL database.
2. Render hosts the Flask web app using `render.yaml`.
3. GitHub Actions runs `python scraper.py` every 4 hours using `.github/workflows/scrape.yml`.

This avoids keeping a paid always-on background worker just for scheduling. If you prefer Render background workers, `scheduler.py` is ready to use as a worker start command: `python scheduler.py`.

## Neon setup

1. Create a Neon project at `https://neon.tech`.
2. Create or use the default database.
3. Copy the pooled connection string. It usually looks like:

```text
postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require
```

4. Use that value as `DATABASE_URL` in Render and GitHub Actions.

The app automatically creates tables on startup with `db.create_all()` and seeds candidate data if the `candidate` table is empty.

## Render deployment

This repository includes `render.yaml` for a Render Blueprint web service.

Steps:

1. Push this repository to GitHub.
2. In Render, click **New +** → **Blueprint**.
3. Connect this GitHub repository.
4. Render will detect `render.yaml` and create the `skarion-job-scraper-web` service.
5. In the service environment variables, set:

| Key | Value |
| --- | --- |
| `DATABASE_URL` | Neon pooled PostgreSQL connection string |
| `PYTHON_VERSION` | `3.11.9` |

6. Deploy.
7. After deploy, verify:

```text
https://YOUR-RENDER-SERVICE.onrender.com/health
```

Expected response:

```json
{"status":"ok"}
```

## GitHub Actions background scraping

The scheduled scraper workflow is defined in `.github/workflows/scrape.yml`.

Manual setup required:

1. Go to GitHub repository → **Settings** → **Secrets and variables** → **Actions**.
2. Add a repository secret:

| Secret | Value |
| --- | --- |
| `DATABASE_URL` | Neon pooled PostgreSQL connection string |

3. The scraper will run every 4 hours via cron:

```yaml
0 */4 * * *
```

4. You can also run it manually from GitHub → **Actions** → **Scheduled scraper** → **Run workflow**.

## Important runtime behavior

- Only LinkedIn and Dice jobs are scraped/displayed.
- Jobs requiring US citizenship or citizenship for clearance are filtered out and not displayed.
- Senior, lead, manager, director, principal, and 7+ years roles are filtered out.
- The dashboard sorts by match score high-to-low by default.
- The API also enforces source and citizenship filters as a safety layer.

## Useful commands

Compile check:

```bash
python -m py_compile app.py models.py scraper.py scheduler.py
```

Smoke test:

```bash
python - <<'PY'
from app import app
client = app.test_client()
assert client.get('/health').status_code == 200
assert client.get('/api/candidates').status_code == 200
print('smoke ok')
PY
```

Run one scrape:

```bash
python scraper.py
```
