import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .models import TeacherProfile
from ..stories.forms import StoryForm



def get_or_none(qs, **kwargs):
    try:
        return qs.get(**kwargs)
    except ObjectDoesNotExist:
        return None



def _response(request, teacher, story=None, success=True):
    """Return JSON response to AJAX request or redirect otherwise."""
    if request.is_ajax():
        data = {'success': success}
        if story:
            data['html'] = render_to_string(
                '_story.html',
                {'story': story, 'teacher': teacher, 'user': request.user},
                )
        return HttpResponse(
            json.dumps(data), content_type="application/json")
    else:
        return redirect(request.path)



def teacher_detail(request, username):
    teacher_profile = get_object_or_404(
        TeacherProfile.objects.select_related('user'), user__username=username)
    teacher = teacher_profile.user
    if request.method == 'POST':

        if 'delete-story' in request.POST:
            with transaction.atomic():
                teacher.stories.filter(pk=request.POST['delete-story']).delete()
            messages.success(request, "Story deleted.")
            return _response(request, teacher)
        elif 'publish-story' in request.POST:
            with transaction.atomic():
                story = get_or_none(
                    teacher.stories.select_for_update(),
                    pk=request.POST['publish-story'],
                    private=False,
                    published=False,
                    )
                if story:
                    story.published = True
                    story.save()
            return _response(request, teacher, story, success=story is not None)
        elif 'hide-story' in request.POST:
            with transaction.atomic():
                story = get_or_none(
                    teacher.stories.select_for_update(),
                    pk=request.POST['hide-story'],
                    published=True,
                    )
                if story:
                    story.published = False
                    story.save()
            return _response(request, teacher, story, success=story is not None)

        form = StoryForm(teacher, request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Thanks for submitting your story!")
            return _response(request, teacher)
    else:
        form = StoryForm(teacher)

    return render(
        request, 'teacher_detail.html', {'form': form, 'teacher': teacher})
