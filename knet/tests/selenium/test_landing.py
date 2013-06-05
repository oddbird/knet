"""Selenium tests for landing page."""
"""Selenium tests for landing page."""


def test_landing_loads(selenium):
    selenium.get(selenium.live_server.url)

    assert selenium.title == "K Network"
