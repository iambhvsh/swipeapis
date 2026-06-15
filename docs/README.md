# Atlas Documentation

Welcome to the Atlas documentation.

Atlas is a self hosted API infrastructure toolkit focused exclusively on search. It is designed to be lightweight, deterministic, and entirely private. Atlas has no user accounts, no API keys, and no databases. It functions strictly to retrieve, rank, and return search results.

## Overview

The documentation is organized by system responsibility:

* **[Architecture](Architecture.md)**: Details the modular request lifecycle from routing to provider invocation.
* **[Configuration](Configuration.md)**: Explains the centralized variables that govern result constraints, deduplication thresholds, and ranking multipliers.
* **[Ranking](Ranking.md)**: Covers the explicit heuristics used to score, classify, and sort web results.
* **[Providers](Providers.md)**: Describes how Atlas interfaces with upstream search engines.
* **[API Reference](API.md)**: Provides technical specifications for the primary search endpoint.

Atlas is designed for predictability and long term maintainability. It achieves this by remaining stateless and relying on standard web primitives.
