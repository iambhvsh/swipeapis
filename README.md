# Atlas

A modern self-hosted API infrastructure toolkit.

Atlas is an elegant, minimal, and modular API framework focused on search, finance, and news aggregation. Designed with safe defaults, configurable limits, and a clean developer experience, it provides robust infrastructure without the complexity of enterprise bloat or SaaS lock-in.

## Documentation

Full framework documentation is provided in the `docs/` directory:

- [Architecture](docs/Architecture.md)
- [Getting Started](docs/Getting-Started.md)
- [Installation](docs/Installation.md)
- [Search Engine](docs/Search.md)
- [Providers](docs/Providers.md)
- [API Reference](docs/API.md)

[View all documentation](docs/README.md)

## Quick Start

```bash
git clone https://github.com/iambhvsh/atlas.git
cd atlas
pip install -r requirements.txt
python -m uvicorn app.main:app
```

```bash
curl "http://127.0.0.1:8000/search/?q=atlas"
curl "http://127.0.0.1:8000/finance/AAPL"
curl "http://127.0.0.1:8000/news/?category=technology"
```

## License

MIT
