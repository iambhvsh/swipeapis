# Atlas

Atlas is a stateless, privacy focused search engine API.

Designed to be self hosted, lightweight, and deterministic, Atlas aggregates, normalizes, and ranks search results across multiple provider backends in real time. It explicitly avoids databases, tracking, user profiles, or artificial intelligence dependencies to ensure absolute transparency and predictable performance.

## Architecture

Atlas follows a clean, single responsibility architecture:

* **Routes**: Request validation and configuration (`app/routes/`).
* **Providers**: Headless adapters for upstream search APIs (`app/providers/`).
* **Intent**: Query understanding and classification (`app/services/intent.py`).
* **Ranker**: Explainable scoring pipeline across diverse signals (`app/services/ranker.py`).
* **Authority**: Domain and source-quality scoring for official and trusted results (`app/services/authority.py`).
* **Dedupe**: Strict metadata and URL normalization to merge duplicate results (`app/services/dedupe.py`).

## Installation

Atlas requires Python 3.10+.

<details>
<summary>macOS / Linux</summary>

```bash
git clone https://github.com/atlas-search/atlas.git
cd atlas
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
</details>

<details>
<summary>Windows</summary>

```powershell
git clone https://github.com/atlas-search/atlas.git
cd atlas
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
</details>

## Quick Start

Start the Uvicorn application server:

```bash
python -m uvicorn app.main:app
```

Execute a search:

```bash
curl "http://127.0.0.1:8000/search?q=react"
```

To see the API description and endpoint specifications, fetch the root:

```bash
curl "http://127.0.0.1:8000/"
```

## Configuration

Ranking weights, duplicate penalties, provider thresholds, authority boosts, and rate limits are centralized in `app/config.py`. To customize how Atlas scores results, adjust these tunables.

Atlas explicitly avoids magic numbers in its ranking algorithms.

## Development

Atlas is fully typed and verified by Pytest.

```bash
# Run tests
python -m pytest tests/

# Format code
black app/ tests/
```

## Design Constraints

Atlas strictly adheres to the following constraints:

1. **No Databases**: Atlas is fully stateless.
2. **No Tracking**: Atlas has no user accounts, histories, or telemetry.
3. **No ML/AI**: Atlas uses deterministic heuristics, not language models or vector search.
4. **Search Only**: Atlas focuses exclusively on retrieving and ranking web results.

## License

MIT
