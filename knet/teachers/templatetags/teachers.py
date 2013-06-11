"""Teacher-related template tags and filters."""
from django import template

from ..models import TeacherProfile

register = template.Library()



@register.filter
def teacher_profile(user):
    """Return user's teacher profile, or ``None``."""
    try:
        return user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return None
