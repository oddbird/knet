"""Landing page views."""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .decorators import ajax
from .forms import LeadForm



@ajax("landing/_form.html")
def landing(request):
    """A landing page with an email address signup."""
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(
                request, "Thanks for your interest; we'll be in touch soon!")
            if not request.is_ajax():
                return redirect("landing")
    else:
        form = LeadForm()

    return TemplateResponse(request, "home.html", {"form": form})
