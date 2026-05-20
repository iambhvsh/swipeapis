# Ranking

Atlas employs an internal global scoring engine to ensure relevance and diversity after aggregation.

## Scoring Flow

Once results are aggregated and deduplicated, they pass through the `rank_results` function (`app/services/ranking.py`).

1. **Provider Weighting**
   - Each provider carries a base weight.
   - Example: Bing (100), Brave (90), DuckDuckGo (70), Yahoo (50).

2. **Original Position Penalty**
   - Results retrieved higher up on a provider's page receive a smaller penalty.
   - `penalty = original_rank * 2`.

3. **Duplicate Frequency Bonus**
   - If a canonical URL appears across multiple providers, it is considered more relevant.
   - `bonus = (frequency - 1) * 15`.

4. **Global Sorting**
   - The final score is calculated: `base_score - penalty + bonus`.
   - Results are sorted descending and assigned a final, global `rank`.
