"""
WSGI config for knet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "knet.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Allow OAuth provider to wrap WSGI app
from knet.accounts import oauth
provider = oauth.get_provider()
application = provider.wrap_app(application)
