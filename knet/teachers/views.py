from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from ..accounts.models import User
from ..stories.forms import StoryForm


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id)
    if request.method == 'POST':
        form = StoryForm(teacher, request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Thanks for submitting your story!")
            return redirect('teacher_detail', teacher_id=teacher_id)
    else:
        form = StoryForm(teacher)

    return render(
        request, 'teacher_detail.html', {'form': form, 'teacher': teacher})
