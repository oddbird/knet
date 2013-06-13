"""Story-related template tags and filters."""
from django import template

register = template.Library()



@register.filter
def stories_visible_to(teacher, user):
    """
    Return iterable of ``teacher``'s stories visible to ``user``.

    ``teacher`` should be a ``ViewTeacher`` instance.

    """
    return teacher.stories(user)
