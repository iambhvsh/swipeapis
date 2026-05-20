# Installation

Atlas is lightweight and can be deployed in multiple environments.

## Cloning

```bash
git clone https://github.com/your-org/atlas.git
cd atlas
```

## Virtual Environment

It is recommended to run Atlas inside an isolated environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Dependencies

Atlas utilizes a minimal dependency tree.
```bash
pip install -r requirements.txt
```

Core dependencies include:
- `fastapi` and `uvicorn` for the runtime
- `ddgs` for Search provider adapters
- `yfinance` for Finance provider adapters
- `pygooglenews` for News provider adapters

## Docker

Atlas includes a standard `docker-compose.yml` for containerized environments.
```bash
docker-compose up -d
```
The API will be available on port `8000`.

## Local Runtime

If not using Docker, invoke the runtime module directly:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
