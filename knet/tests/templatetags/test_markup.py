"""
Tests for markup-related template tags and filters.

"""
from django.utils.safestring import SafeData

from knet.templatetags import markup



def test_markdown_renders_html():
    """Markdown filter renders markdown to HTML."""
    assert markup.markdown("_foo_") == "<p><em>foo</em></p>\n"


def test_markdown_returns_safestring():
    """Markdown filter returns marked-safe HTML string."""
    assert isinstance(markup.markdown("_foo"), SafeData)


def test_markdown_escapes_html():
    """Markdown filter escapes HTML."""
    assert markup.markdown("<script>") == "<p>&lt;script&gt;</p>\n"
