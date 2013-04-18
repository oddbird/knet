"""Test hooks and fixture resources."""
import pytest


@pytest.fixture
def client(request, db):
    """Give a test access to a WebTest client for integration-testing views."""
    # We don't use TestCase classes, but we instantiate the django_webtest
    # TestCase subclass to use its methods for patching/unpatching settings.
    from knet.tests import client
    import django_webtest
    webtestcase = django_webtest.WebTest("__init__")
    webtestcase.setup_auth = False
    webtestcase._patch_settings()
    request.addfinalizer(webtestcase._unpatch_settings)

    return client.TestClient()



@pytest.fixture
def no_csrf_client(request, db):
    """Give a test access to a CSRF-exempt WebTest client."""
    # We don't use TestCase classes, but we instantiate the django_webtest
    # TestCase subclass to use its methods for patching/unpatching settings.
    from knet.tests import client
    import django_webtest
    webtestcase = django_webtest.WebTest("__init__")
    webtestcase.setup_auth = False
    webtestcase.csrf_checks = False
    webtestcase._patch_settings()
    request.addfinalizer(webtestcase._unpatch_settings)

    return client.TestClient()
