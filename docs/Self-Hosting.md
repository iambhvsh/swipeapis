# Self-Hosting

Atlas was built specifically with a self-host-first philosophy.

## Stateless Design

Atlas avoids the complexity of SaaS platforms by intentionally omitting databases, authentication layers, and billing metrics.
- There are no user accounts.
- There are no API keys.
- You deploy the code and immediately query the endpoints.

## Infrastructure Simplicity

By offloading rate-limiting to memory (`slowapi`) and avoiding state entirely, Atlas allows you to focus purely on the application utilizing the APIs rather than managing the API infrastructure itself.
