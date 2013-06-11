import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.template import RequestContext

from .forms import StoryForm, TeacherProfileForm
from .models import TeacherProfile
from .viewmodels import ViewTeacher



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
                context_instance=RequestContext(request),
                )
        return HttpResponse(
            json.dumps(data), content_type="application/json")
    else:
        return redirect(request.path)



def teacher_detail(request, username):
    teacher_profile = get_object_or_404(
        TeacherProfile.objects.select_related('user'), user__username=username)
    teacher = ViewTeacher(teacher_profile)
    if request.method == 'POST':

        if 'delete-story' in request.POST:
            with transaction.atomic():
                teacher.stories().filter(
                    pk=request.POST['delete-story']).delete()
            messages.success(request, "Story deleted.")
            return _response(request, teacher)
        elif 'publish-story' in request.POST:
            with transaction.atomic():
                story = get_or_none(
                    teacher.stories().select_for_update(),
                    pk=request.POST['publish-story'],
                    private=False,
                    )
                if story:
                    story.published = True
                    story.save()
                else:
                    messages.error(request, "That story has been removed.")
            return _response(request, teacher, story, success=story is not None)
        elif 'hide-story' in request.POST:
            with transaction.atomic():
                story = get_or_none(
                    teacher.stories().select_for_update(),
                    pk=request.POST['hide-story'],
                    )
                if story:
                    story.published = False
                    story.save()
                else:
                    messages.error(request, "That story has been removed.")
            return _response(request, teacher, story, success=story is not None)

        form = StoryForm(teacher_profile, request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Thanks for submitting your story!")
            return _response(request, teacher)
        elif request.is_ajax():
            # provide form errors as user messages instead of form errors
            for fieldname, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return _response(request, teacher, success=False)
    else:
        form = StoryForm(teacher_profile)

    return render(
        request,
        'teacher_detail.html',
        {'form': form, 'teacher': teacher},
        )


@login_required
def create_profile(request):
    """Give user option to create a teacher profile."""
    try:
        request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        pass
    else:
        return redirect('teacher_detail', username=request.user.username)

    if request.method == 'POST':
        form = TeacherProfileForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_detail', username=request.user.username)
    else:
        form = TeacherProfileForm(request.user)

    return render(request, 'create_profile.html', {'form': form})
