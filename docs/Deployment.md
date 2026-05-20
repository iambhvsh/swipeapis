# Deployment

Atlas is built as a portable ASGI application that deploys seamlessly across diverse infrastructure.

## Docker

A `docker-compose.yml` is provided at the root for container orchestration.
```bash
docker-compose up -d
```
It builds standard images utilizing Python environments, mapping the port `8000` to the host.

## Vercel

Atlas maintains a `vercel.json` file for immediate serverless deployment out of the box via Vercel.
```bash
npm i -g vercel
vercel
```

## Self-Hosting

If deploying directly onto a VPS or bare metal, use a robust ASGI server like `uvicorn` managed via `systemd` or `supervisor`.
```bash
uvicorn app.main:app --host 0.0.0.0 --port 80 --workers 4
```
