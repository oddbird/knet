"""Tests for accounts admin."""
from django.core.urlresolvers import reverse

from knet.accounts.models import User
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


def test_user_add(client):
    """Can add a User."""
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    form = client.get(
        reverse("admin:accounts_user_add"),
        user=admin,
        status=200,
        ).forms[0]

    form['username'] = 'foo'
    form['password1'] = 'testpw'
    form['password2'] = 'testpw'

    form.submit(status=302)

    assert User.objects.filter(username='foo').exists()
