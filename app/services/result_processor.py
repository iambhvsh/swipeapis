from typing import List, Dict, Any
from collections import defaultdict
import re

from app.utils.urls import normalize_url


def normalize_title(title: str) -> str:
    """
    Create a normalized title representation
    for duplicate detection.

    Does NOT modify the original title.
    """

    title = title.lower().strip()

    title = re.sub(
        r"\s+",
        " ",
        title,
    )

    return title


def normalize_description(
    description: str,
    max_length: int = 1000,
) -> str:
    """
    Clean description text.

    Keeps original meaning while removing
    excessive whitespace.
    """

    description = description.strip()

    description = re.sub(
        r"\s+",
        " ",
        description,
    )

    if len(description) > max_length:
        description = description[:max_length]

    return description


def enrich_results(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Normalize metadata without altering
    original ranking signals.
    """

    enriched = []

    for result in results:
        item = dict(result)

        item["title"] = str(
            item.get(
                "title",
                "",
            )
        ).strip()

        item["description"] = normalize_description(
            str(
                item.get(
                    "description",
                    "",
                )
            )
        )

        enriched.append(item)

    return enriched


def merge_duplicate_urls(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Merge results that point to the same URL.

    Tracks:
    - frequency
    - providers
    """

    merged: Dict[str, Dict[str, Any]] = {}

    for idx, result in enumerate(
        results,
        start=1,
    ):
        url = result.get("url")

        if not url:
            continue

        normalized_url = normalize_url(str(url))

        if normalized_url not in merged:
            item = dict(result)

            item["frequency"] = 1

            item["providers"] = {
                str(
                    item.get(
                        "provider",
                        "",
                    )
                )
            }

            item["original_rank"] = idx

            merged[normalized_url] = item

            continue

        existing = merged[normalized_url]

        existing["frequency"] += 1

        existing["providers"].add(
            str(
                result.get(
                    "provider",
                    "",
                )
            )
        )

    final_results = []

    for result in merged.values():
        result["providers"] = sorted(
            list(
                result.get(
                    "providers",
                    set(),
                )
            )
        )

        final_results.append(result)

    return final_results


def merge_duplicate_titles(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Merge identical normalized titles.

    Keeps the strongest version.
    """

    grouped = defaultdict(list)

    for result in results:
        normalized_title = normalize_title(
            str(
                result.get(
                    "title",
                    "",
                )
            )
        )

        grouped[normalized_title].append(result)

    final_results = []

    for items in grouped.values():
        best = max(
            items,
            key=lambda item: (
                int(
                    item.get(
                        "frequency",
                        1,
                    )
                ),
                len(
                    str(
                        item.get(
                            "description",
                            "",
                        )
                    )
                ),
            ),
        )

        final_results.append(best)

    return final_results


def process_results(
    raw_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Generic Atlas result processing pipeline.

    Steps:

    1. Normalize metadata
    2. Merge duplicate URLs
    3. Merge duplicate titles
    """

    results = enrich_results(raw_results)

    results = merge_duplicate_urls(results)

    results = merge_duplicate_titles(results)

    return results
