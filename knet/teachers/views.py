from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import TeacherProfile
from ..stories.forms import StoryForm


def teacher_detail(request, username):
    teacher_profile = get_object_or_404(
        TeacherProfile.objects.select_related('user'), user__username=username)
    teacher = teacher_profile.user
    if request.method == 'POST':
        redirect_response = redirect('teacher_detail', username=username)

        if 'delete-story' in request.POST:
            with transaction.atomic():
                teacher.stories.filter(pk=request.POST['delete-story']).delete()
            messages.success(request, "Story deleted.")
            return redirect_response

        form = StoryForm(teacher, request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Thanks for submitting your story!")
            return redirect_response
    else:
        form = StoryForm(teacher)

    return render(
        request, 'teacher_detail.html', {'form': form, 'teacher': teacher})
