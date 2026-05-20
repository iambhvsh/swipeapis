# Structure

The repository maintains a flat and explicit structure.

```
app/
├── routes/        # HTTP entry points and validation
├── services/      # Aggregation, deduplication, and ranking logic
├── providers/     # Domain-specific backend adapters (search, finance, news)
├── middleware/    # Rate limiters and protective layers
├── utils/         # Pure helper functions (e.g., URL normalization)
├── models/        # (Reserved for future type schemas)
├── core/          # (Reserved for central config systems)
└── main.py        # The FastAPI application runtime
```
