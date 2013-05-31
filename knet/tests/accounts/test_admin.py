"""Tests for accounts admin."""
from django.core.urlresolvers import reverse

from ..factories import UserFactory



def test_user_changelist(client):
    """The User admin changelist loads successfully."""
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    client.get(
        reverse("admin:accounts_user_changelist"), user=admin, status=200)


def test_user_change(client):
    """The User admin change page loads successfully."""
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    user = UserFactory.create()
    client.get(
        reverse("admin:accounts_user_change", args=[user.id]),
        user=admin,
        status=200,
        )
