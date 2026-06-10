# Ranking

The Atlas ranking engine calculates scores by evaluating multiple independent signals. The final rank of a result is deterministic and strictly dependent on its cumulative score.

## The Ranking Pipeline

Ranking occurs in `app/services/ranker.py` and proceeds in the following sequence:

### 1. Intent Classification
The query is analyzed by `app/services/intent.py` to determine its intent category: freshness, local, transactional, navigational, informational, ambiguous, or entity. This classification determines which specialized boosts apply.

### 2. Relevance Scoring
Relevance evaluates the text metadata.
* Calculates query term coverage within the title, URL, and description.
* Applies phrase matching.
* Evaluates title purity to penalize keyword stuffing.

### 3. Quality Scoring
Quality scoring occurs in `app/services/quality.py`. It does not analyze content relevance. It strictly evaluates structural health:
* Does the title exist? Is it a reasonable length?
* Is the URL well formed? Is the path excessively deep?
* Does the description exist? Is it long enough to be useful?

### 4. Provider and Frequency Scoring
Scores are augmented based on the reputation of the origin provider and the cross provider agreement.
* If multiple providers return the same URL, it is awarded a frequency multiplier.
* A base score is established using Reciprocal Rank Fusion based on the URL's original position from the upstream provider.

### 5. Intent Specific Boosts
If the query indicates navigational, entity, or ambiguous intent, the system applies heavy boosts to official domains matching the query terms. If the query indicates freshness intent, the system applies a boost for dates or recent time indicators parsed from the metadata.

### 6. Safety Penalties
Severe point deductions are applied to results lacking a title, URL, or description.

### 7. Diversity Enforcement
Results are sorted by score, then passed to `app/services/diversity.py`.
* Results from a single domain are capped at a strict maximum.
* Subsequent results from the same domain receive compounding score penalties.

### 8. Final Sort
The final array is sorted by the diversified score, assigned a strict index rank, and returned.
