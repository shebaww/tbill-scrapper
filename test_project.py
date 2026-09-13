import pytest
from project import run_webscraper, run_merge, run_kenya, run_ethiopia

def test_ethiopia():
    assert callable(run_ethiopia)

def test_kenya():
    assert callable(run_kenya)

def test_merge():
    assert callable(run_merge)

def test_web_scraper():
    assert callable(run_webscraper)
