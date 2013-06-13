"""
Markup-related template tags and filters.

"""
from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

import markdown2



register = template.Library()



@register.filter
def markdown(text, safe_mode="escape"):
    if safe_mode == "unsafe":
        safe_mode = None
    return mark_safe(
        force_text(
            markdown2.markdown(text, safe_mode=safe_mode)))
markdown.is_safe = True
