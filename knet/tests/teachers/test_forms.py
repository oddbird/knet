from knet.teachers.forms import StoryForm

from .factories import TeacherProfileFactory



def test_save_assigns_teacher():
    """StoryForm assigns teacher profile to the story before saving."""
    profile = TeacherProfileFactory.build()
    form = StoryForm(profile, {'body': "Cool story bro"})

    assert form.is_valid()
    story = form.save(commit=False)

    assert story.profile == profile
