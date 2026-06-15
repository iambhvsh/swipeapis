from app.models import SearchResult
from app.services.ranker import rank_results


def test_official_compact_domain_beats_keyword_heavy_reference():
    results = [
        SearchResult(
            title="Next.js by Vercel - The React Framework",
            url="https://nextjs.org",
            description="The official Next.js framework site.",
            provider="bing",
            original_rank=4,
        ),
        SearchResult(
            title="Next.js - Wikipedia",
            url="https://en.wikipedia.org/wiki/Next.js",
            description="Next.js is an open-source full-stack web development framework.",
            provider="bing",
            original_rank=1,
        ),
    ]

    ranked = rank_results(results, "next.js")

    assert ranked[0].url == "https://nextjs.org"


def test_low_authority_noise_is_demoted_for_entity_queries():
    results = [
        SearchResult(
            title="React",
            url="https://react.dev",
            description="React lets you build user interfaces out of components.",
            provider="bing",
            original_rank=2,
        ),
        SearchResult(
            title="React (Wagakki Band EP)",
            url="https://grokipedia.com/page/react_wagakki_band_ep",
            description="React is a concept extended play by a Japanese rock band.",
            provider="bing",
            original_rank=1,
        ),
    ]

    ranked = rank_results(results, "react")

    assert ranked[0].url == "https://react.dev"
