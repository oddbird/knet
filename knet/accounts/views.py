from django.conf import settings
from django.contrib import auth, messages
from django.db import transaction
from django.shortcuts import redirect, render
from oauth2 import OAuthError

from .models import User
from .oauth import get_provider



def oauth(request):
    """OAuth callback."""
    provider = get_provider()
    try:
        user_data = provider.get_user_data(request.GET)
    except OAuthError as e:
        messages.error(request, str(e))
        return redirect('landing')

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'name': user_data.get('name', ''),
                }
            )

    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

    # If you just logged in for the first time, we take you to create-profile.
    # Otherwise, we redirect you back wherever you came from.
    if created:
        return redirect('create_profile')
    return redirect(request.GET.get('next', '/'))



def logout(request):
    """Log out on POST; request confirmation on GET."""
    if request.method == 'POST':
        auth.logout(request)

        return redirect(request.POST.get('next') or 'landing')

    return render(request, 'accounts/logout.html')
