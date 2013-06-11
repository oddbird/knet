from urllib.parse import urljoin, urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module



def get_provider(redirect_to=None):
    """Return a configured OAuth provider instance."""
    mod_name, class_name = settings.OAUTH_PROVIDER.rsplit('.', 1)
    provider_class = getattr(import_module(mod_name), class_name)
    qs_data = {'next': redirect_to} if redirect_to else {}
    redirect_uri = '{}?{}'.format(
        urljoin(settings.BASE_URL, reverse('oauth')), urlencode(qs_data))
    return provider_class(
        redirect_uri=redirect_uri,
        client_id=settings.OAUTH_CLIENT_ID,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        )
