from django.shortcuts import get_object_or_404, redirect, render

from ..accounts.models import User
from .forms import StoryForm


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id)
    if request.method == 'POST':
        form = StoryForm(teacher, request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_detail', teacher_id=teacher_id)
    else:
        form = StoryForm(teacher)

    return render(
        request, 'teacher_detail.html', {'form': form, 'teacher': teacher})
