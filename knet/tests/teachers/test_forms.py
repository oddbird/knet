from knet.teachers.forms import StoryForm, TeacherProfileForm

from ..factories import UserFactory
from .factories import TeacherProfileFactory



class TestStoryForm(object):
    def test_save_assigns_teacher(self):
        """StoryForm assigns teacher profile to the story before saving."""
        profile = TeacherProfileFactory.build()
        form = StoryForm(profile, {'body': "Cool story bro"})

        assert form.is_valid()
        story = form.save(commit=False)

        assert story.profile == profile



class TestTeacherProfileForm(object):
    def test_save_assigns_user(self):
        """TeacherProfileForm assigns user to the profile before saving."""
        user = UserFactory.build()
        form = TeacherProfileForm(user, {'school': "Sample Elementary"})

        assert form.is_valid()
        profile = form.save(commit=False)

        assert profile.user == user
