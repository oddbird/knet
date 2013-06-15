"""Landing page views."""
from django.template.response import TemplateResponse



def landing(request):
    """A static landing page."""
    return TemplateResponse(request, "home.html")
