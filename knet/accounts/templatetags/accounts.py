from django import template

from .. import oauth

register = template.Library()



@register.simple_tag
def oauth_authorize_url():
    """Get OAuth provider login url."""
    provider = oauth.get_provider()
    return provider.get_authorize_url()
