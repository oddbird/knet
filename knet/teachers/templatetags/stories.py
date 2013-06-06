"""Story-related template tags and filters."""
from django import template

register = template.Library()



@register.filter
def stories_visible_to(teacher, user):
    """
    Filter ``teacher``'s stories to those visible to ``user``.

    ``teacher`` should be a ``ViewTeacher`` instance.

    """
    qs = teacher.stories()
    if teacher.user != user:
        qs = qs.filter(published=True)
    return qs
