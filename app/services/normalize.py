import re


def normalize_title(title: str) -> str:
    """
    Create a normalized title representation for duplicate detection.
    """
    title = title.lower().strip()
    title = re.sub(r"\s+", " ", title)
    return title


def normalize_description(description: str, max_length: int = 360) -> str:
    """
    Clean description text.
    """
    description = description.strip()
    description = re.sub(r"\s+", " ", description)
    if len(description) > max_length:
        description = description[: max_length - 1].rstrip() + "..."
    return description
