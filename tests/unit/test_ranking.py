from app.services.ranker import rank_results
from app.models import SearchResult


def test_provider_weighting():
    results = [
        SearchResult(
            title="1",
            description="1",
            url="https://yahoo.com/1",
            provider="yahoo",
            original_rank=1,
            frequency=1,
        ),
        SearchResult(
            title="2",
            description="2",
            url="https://bing.com/2",
            provider="bing",
            original_rank=1,
            frequency=1,
        ),
        SearchResult(
            title="3",
            description="3",
            url="https://duck.com/3",
            provider="duckduckgo",
            original_rank=1,
            frequency=1,
        ),
    ]
    ranked = rank_results(results, "test")

    assert ranked[0].provider == "bing"
    assert ranked[1].provider == "duckduckgo"
    assert ranked[2].provider == "yahoo"


def test_duplicate_frequency_scoring():
    results = [
        SearchResult(
            title="1",
            description="1",
            url="1",
            provider="bing",
            original_rank=1,
            frequency=1,
        ),
        SearchResult(
            title="2",
            description="2",
            url="2",
            provider="brave",
            original_rank=1,
            frequency=3,
        ),
    ]
    ranked = rank_results(results, "test")

    assert ranked[0].provider == "brave"
    assert ranked[1].provider == "bing"


def test_original_rank_penalty():
    results = [
        SearchResult(
            title="1",
            description="1",
            url="1",
            provider="bing",
            original_rank=5,
            frequency=1,
        ),
        SearchResult(
            title="2",
            description="2",
            url="2",
            provider="bing",
            original_rank=1,
            frequency=1,
        ),
    ]
    ranked = rank_results(results, "test")

    assert ranked[0].url == "2"
    assert ranked[1].url == "1"


def test_stable_assignment():
    results = [
        SearchResult(
            title="1",
            description="1",
            url="1",
            provider="bing",
            original_rank=1,
            frequency=1,
        ),
    ]
    ranked = rank_results(results, "test")

    assert ranked[0].rank == 1
    assert ranked[0].score > 0
