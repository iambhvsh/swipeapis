from typing import List, Dict, Any

PROVIDER_WEIGHTS = {
    "bing": 100,
    "brave": 90,
    "duckduckgo": 70,
    "yahoo": 50,
}

def rank_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranks deduplicated results based on:
    - Provider weight
    - Duplicate frequency (if merged)
    - Original position
    """
    scored_results = []

    for result in results:
        # Get weight based on the primary provider that found it
        provider = result.get('provider', 'duckduckgo')
        base_score = PROVIDER_WEIGHTS.get(provider, 50)

        # Position penalty (lower index = better, less penalty)
        # e.g., if it was rank 1 in Bing, it's better than rank 5 in Bing.
        position = result.get('original_rank', 1)
        position_penalty = position * 2

        # Frequency bonus (if multiple providers returned it, we can increment freq)
        freq = result.get('frequency', 1)
        freq_bonus = (freq - 1) * 15

        final_score = base_score - position_penalty + freq_bonus
        result['score'] = final_score
        scored_results.append(result)

    # Sort descending by score
    scored_results.sort(key=lambda x: x['score'], reverse=True)

    # Assign final rank
    for i, res in enumerate(scored_results):
        res['rank'] = i + 1

    return scored_results
