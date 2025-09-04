import os
from services.scraper.app import fetch_currency, fetch_crypto


def test_fetch_currency_returns_rows():
    rows = fetch_currency()
    assert isinstance(rows, list)
    assert any(r["symbol"] == "EUR" for r in rows)


def test_fetch_crypto_returns_rows():
    rows = fetch_crypto()
    assert isinstance(rows, list)
    assert any(r["symbol"] == "BTC" for r in rows)