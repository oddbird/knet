from urllib.parse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module



def get_provider():
    """Return a configured OAuth provider instance."""
    mod_name, class_name = settings.OAUTH_PROVIDER.rsplit('.', 1)
    provider_class = getattr(import_module(mod_name), class_name)
    return provider_class(
        redirect_uri=urljoin(settings.BASE_URL, reverse('oauth')),
        client_id=settings.OAUTH_CLIENT_ID,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        )
