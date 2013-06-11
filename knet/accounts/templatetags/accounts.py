from django import template

from .. import oauth

register = template.Library()



@register.simple_tag
def oauth_authorize_url(redirect_to):
    """Get OAuth provider login url that will redirect to given URL."""
    provider = oauth.get_provider(redirect_to=redirect_to)
    return provider.get_authorize_url()
