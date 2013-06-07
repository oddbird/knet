"""Test hooks and fixture resources."""
import pytest


@pytest.fixture
def client(request, db, webtest):
    """Give a test access to a WebTest client for integration-testing views."""
    from knet.tests.client import TestClient
    return TestClient()


@pytest.fixture
def no_csrf_client(request, client, webtest):
    """Give a test access to a CSRF-exempt WebTest client."""
    webtest._disable_csrf_checks()
    return client


@pytest.fixture
def webtest(request):
    """
    Get an instance of a django-webtest TestCase subclass.

    We don't use TestCase classes, but we instantiate the django_webtest
    TestCase subclass in our web client fixtures to use its methods for
    patching/unpatching settings.

    """
    import django_webtest
    webtest = django_webtest.WebTest("__init__")

    webtest._patch_settings()
    request.addfinalizer(webtest._unpatch_settings)

    return webtest
