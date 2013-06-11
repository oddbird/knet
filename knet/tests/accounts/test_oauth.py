from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from pretend import stub

from knet.accounts.oauth import get_provider


class FakeProvider(stub):
    pass


@override_settings(
    BASE_URL = 'http://example.com',
    OAUTH_PROVIDER='knet.tests.accounts.test_oauth.FakeProvider',
    OAUTH_CLIENT_ID='client id',
    OAUTH_CLIENT_SECRET='client secret')
def test_get_provider():
    provider = get_provider(redirect_to='/foo/')

    assert isinstance(provider, FakeProvider)
    assert provider.redirect_uri == (
        'http://example.com' + reverse('oauth') + '?next=%2Ffoo%2F')
    assert provider.client_id == 'client id'
    assert provider.client_secret == 'client secret'
