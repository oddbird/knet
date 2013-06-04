from django.conf import settings
from django.contrib import auth, messages
from django.db import transaction
from django.shortcuts import redirect, render
from oauth2 import OAuthError

from ..teachers.models import TeacherProfile
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

    # @@@ just store data in session and redirect to signup page
    with transaction.atomic():
        user, _ = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'name': user_data.get('name', ''),
                }
            )
        # @@@ for now all logins are teachers, no signup form
        TeacherProfile.objects.get_or_create(user=user)

    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

    return redirect('teacher_detail', username=user.username)



def logout(request):
    """Log out on POST; request confirmation on GET."""
    if request.method == 'POST':
        auth.logout(request)

        return redirect(request.POST.get('next') or 'landing')

    return render(request, 'accounts/logout.html')
