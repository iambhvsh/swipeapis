# Getting Started

Atlas is designed to be run immediately with zero configuration. It is stateless and does not require API keys or databases.

## Prerequisites

- Python 3.10+
- `pip` or `uv`

## Local Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the runtime:
   ```bash
   python -m uvicorn app.main:app
   ```

## Your First Request

The root endpoint returns the system status:
```bash
curl http://127.0.0.1:8000/
```

Run a search query:
```bash
curl "http://127.0.0.1:8000/search/?q=atlas"
```

## Development Workflow

When modifying Atlas, it is recommended to run the API with the `--reload` flag:
```bash
python -m uvicorn app.main:app --reload
```
This will automatically reload the application on code changes.
