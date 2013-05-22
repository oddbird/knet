"""Tests for landing-page models."""
from . import factories


def test_lead_unicode():
    """Unicode representation of a Lead is its email address."""
    lead = factories.LeadFactory.build(email="someone@example.com")

    assert str(lead) == "someone@example.com"
