from django.template.loader import render_to_string

from bs4 import BeautifulSoup



def redirects_to(response):
    """Assert that the given response redirects to the given URL."""
    return response.headers['location'].replace('http://localhost:80', '')


def render_to_soup(*args, **kwargs):
    """Render a template and return a BeautifulSoup instance."""
    html = render_to_string(*args, **kwargs)
    return BeautifulSoup(html)


def innerhtml(element):
    """Return whitespace-stripped inner HTML of a BeautifulSoup element."""
    return element.decode_contents().strip()


def is_deleted(instance):
    """Return ``True`` if given model instance has been deleted in the db."""
    return not type(instance)._base_manager.filter(pk=instance.pk).exists()


def refresh(instance):
    """Refresh given model instance from the database."""
    return type(instance)._base_manager.get(pk=instance.pk)
