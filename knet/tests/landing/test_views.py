from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from knet.landing.models import Lead



@override_settings(ENABLE_LOGIN=True)
def test_login_button(client):
    """Login link is available."""
    resp = client.get(reverse('landing'))

    assert len(resp.html.findAll('a', 'fb-login'))


@override_settings(ENABLE_LOGIN=False)
def test_login_disabled(client):
    """No login link if disabled in settings."""
    resp = client.get(reverse('landing'))

    assert len(resp.html.findAll('a', 'fb-login')) == 0
