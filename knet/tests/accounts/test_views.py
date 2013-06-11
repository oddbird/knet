from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from oauth2 import OAuthError

from knet.accounts.models import User
from ..factories import UserFactory
from ..utils import redirects_to


@override_settings(OAUTH_PROVIDER='oauth2.dummy.DummyOAuth')
def test_oauth_new_user(client):
    """After creating new user, OAuth view redirects to create_profile."""
    data = {
        'next': '/foo/',
        'username': 'oauthuser',
        'email': 'oauth@example.com',
        'first_name': 'OAuth',
        'last_name': 'User',
        'name': 'O User',
        }
    resp = client.get(reverse('oauth'), data)
    user = User.objects.get(username='oauthuser')

    assert user.email == 'oauth@example.com'
    assert user.first_name == 'OAuth'
    assert user.last_name == 'User'
    assert user.name == 'O User'
    assert redirects_to(resp) == reverse('create_profile') + '?next=%2Ffoo%2F'


@override_settings(OAUTH_PROVIDER='oauth2.dummy.DummyOAuth')
def test_oauth_existing_user(client):
    """After existing user logs in, OAuth view redirects to ``next`` param."""
    UserFactory.create(username='oauthuser')

    data = {
        'next': '/foo/',
        'username': 'oauthuser',
        'email': 'oauth@example.com',
        }
    resp = client.get(reverse('oauth'), data)

    assert redirects_to(resp) == '/foo/'


class ErrorProvider:
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
    resp = client.get(reverse('logout'), user=u, status=200).forms[1].submit()

    assert redirects_to(resp) == reverse('landing')



@override_settings(ENABLE_LOGIN=True)
def test_login(client):
    """Login page contains login links in both header and body."""
    resp = client.get(reverse('login') + '?next=/foo/', status=200)

    login_links = resp.html.findAll('a', 'fb-login')
    assert len(login_links) == 2



@override_settings(ENABLE_LOGIN=False)
def test_login_disabled(client):
    """Login page contains no login links if login disabled."""
    resp = client.get(reverse('login'), status=200)

    assert len(resp.html.findAll('a', 'fb-login')) == 0
