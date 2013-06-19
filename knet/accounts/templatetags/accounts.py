from django.middleware.csrf import get_token
from django import template
from django.utils.html import escape

from .. import oauth

register = template.Library()



@register.simple_tag
def oauth_authorize_url(request, redirect_to):
    """Get OAuth provider login url that will redirect to given URL."""
    provider = oauth.get_provider(
        redirect_to=redirect_to, state=get_token(request))
    return escape(provider.get_authorize_url())
