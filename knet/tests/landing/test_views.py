from django.test.utils import override_settings

from knet.landing.models import Lead



@override_settings(ENABLE_LOGIN=True)
def test_login_button(client):
    """Login link is in banner."""
    resp = client.get('/')

    assert len(resp.html.findAll('a', 'fb-login')) == 1


@override_settings(ENABLE_LOGIN=False)
def test_login_disabled(client):
    """No login link if disabled in settings."""
    resp = client.get('/')

    assert len(resp.html.findAll('a', 'fb-login')) == 0
