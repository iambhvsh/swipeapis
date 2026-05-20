import pytest
from app.utils.urls import normalize_url

def test_normalize_trailing_slash():
    assert normalize_url("https://example.com/") == "https://example.com"
    assert normalize_url("https://example.com/path/") == "https://example.com/path"

def test_normalize_www():
    assert normalize_url("https://www.example.com") == "https://example.com"
    assert normalize_url("http://www.example.com/path") == "http://example.com/path"

def test_normalize_tracking_parameters():
    assert normalize_url("https://example.com?utm_source=test") == "https://example.com"
    assert normalize_url("https://example.com?fbclid=123") == "https://example.com"
    assert normalize_url("https://example.com?q=search&utm_medium=email") == "https://example.com?q=search"
    assert normalize_url("https://example.com?ref=twitter") == "https://example.com"

def test_normalize_canonical_equivalence():
    url1 = "https://www.example.com/path/?utm_source=news"
    url2 = "https://example.com/path?fbclid=abc"
    assert normalize_url(url1) == normalize_url(url2)

def test_malformed_url():
    assert normalize_url("") == ""
    assert normalize_url("invalid_url") == "invalid_url"
