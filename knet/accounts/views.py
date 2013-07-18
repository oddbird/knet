import re
import unicodedata
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from oauth2 import OAuthError

from .models import User
from .oauth import get_provider



def oauth(request):
    """OAuth callback."""
    home = reverse('landing')
    redirect_to = request.GET.get('next') or home
    provider = get_provider(redirect_to=redirect_to, state=get_token(request))
    try:
        user_data = provider.get_user_data(request.GET)
    except OAuthError as e:
        messages.error(request, str(e))
        return redirect('landing')

    with transaction.atomic():
        email = user_data['email']
        username = user_data.get('username')
        if username is None:
            username = slugify(email)
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'name': user_data.get('name', ''),
                }
            )

    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

    # If you already have a profile, taking you there is more useful than the
    # landing page.
    if redirect_to == home:
        try:
            user.teacher_profile
        except ObjectDoesNotExist:
            pass
        else:
            redirect_to = reverse(
                'teacher_detail', kwargs={'username': user.username})

    # If you just logged in for the first time, we take you to create-profile.
    # Otherwise, we redirect you back wherever you came from.
    if created:
        return redirect(
            '{}?{}'.format(
                reverse('create_profile'),
                urlencode({'next': redirect_to}),
                )
            )
    return redirect(redirect_to)



def logout(request):
    """Log out on POST; request confirmation on GET."""
    if request.method == 'POST':
        auth.logout(request)

        return redirect(request.POST.get('next') or 'landing')

    return render(request, 'accounts/logout.html')


def login(request):
    """Display login link."""
    return render(
        request, 'accounts/login.html', {'login_next': request.GET.get('next')})



def slugify(value):
    """
    Converts to lowercase, converts spaces and non-word characters to hyphens.

    Also strips leading and trailing whitespace.

    """
    value = unicodedata.normalize(
        'NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '-', value).strip().lower()
    return re.sub('[-\s]+', '-', value)
