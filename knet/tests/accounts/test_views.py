from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from oauth2 import OAuthError

from ..factories import UserFactory
from ..utils import redirects_to


@override_settings(OAUTH_PROVIDER='oauth2.dummy.DummyOAuth')
def test_oauth(client):
    """Test dummy OAuth workflow."""
    data = {
        'username': 'oauthuser',
        'email': 'oauth@example.com',
        'first_name': 'OAuth',
        'last_name': 'User',
        'name': 'O User',
        }
    resp = client.get(reverse('oauth'), data)

    # @@@ assert data is stored in session

    assert redirects_to(resp) == reverse(
        'teacher_detail', kwargs={'username': 'oauthuser'})


class ErrorProvider(object):
    def __init__(self, *a, **kw):
        pass

    def get_authorize_url(self):
        return '/authorize/'

    def get_user_data(self, *a, **kw):
        raise OAuthError('something bad happens!')


@override_settings(
    OAUTH_PROVIDER='knet.tests.accounts.test_views.ErrorProvider')
def test_oauth_error(client):
    """Test handling of OAuth error."""
    data = {
        'username': 'oauthuser',
        'email': 'oauth@example.com',
        'first_name': 'OAuth',
        'last_name': 'User',
        'name': 'O User',
        }
    resp = client.get(reverse('oauth'), data)

    assert redirects_to(resp) == reverse('landing')

    resp.follow().mustcontain('something bad happens!')


def test_logout(client):
    """GET to logout view returns a confirmation; submitting logs out."""
    u = UserFactory()
    resp = client.get(reverse('logout'), user=u, status=200).forms[0].submit()

    assert redirects_to(resp) == reverse('landing')
