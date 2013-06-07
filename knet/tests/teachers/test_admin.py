"""Tests for teachers admin."""
from django.core.urlresolvers import reverse

from ..factories import UserFactory
from .factories import TeacherProfileFactory



def test_teacherprofile_changelist(client):
    """The Teacherprofile admin changelist loads successfully."""
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    client.get(
        reverse("admin:teachers_teacherprofile_changelist"),
        user=admin,
        status=200,
        )


def test_teacherprofile_change(client):
    """The Teacherprofile admin change page loads successfully."""
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    teacherprofile = TeacherProfileFactory.create()
    client.get(
        reverse(
            "admin:teachers_teacherprofile_change", args=[teacherprofile.id]),
        user=admin,
        status=200,
        )
