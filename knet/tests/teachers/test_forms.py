from knet.teachers.forms import StoryForm, TeacherProfileForm

from ..factories import UserFactory
from .factories import TeacherProfileFactory



class TestStoryForm:
    def test_save_assigns_user_and_teacher(self):
        """StoryForm assigns user and profile to the story before saving."""
        user = UserFactory.build(id=1)
        profile = TeacherProfileFactory.build(user__id=2)
        form = StoryForm(user, profile, {'body': "Cool story bro"})

        assert form.is_valid()
        story = form.save(commit=False)

        assert story.profile == profile
        assert story.submitter == user


    def test_self_post(self):
        """If posting on my own profile, I can submit a name and date."""
        profile = TeacherProfileFactory.build()
        form = StoryForm(
            profile.user,
            profile,
            {
                'body': "Cool story",
                'submitter_name': "Joe",
                'nominal_date': "4/20/2013",
                },
            )

        assert form.is_valid(), form.errors
        story = form.save(commit=False)

        assert story.submitter_name == "Joe"
        assert story.nominal_date.isoformat() == '2013-04-20'


    def test_self_post_only(self):
        """If posting on another's profile, can't override name/date."""
        user = UserFactory.build(id=1)
        profile = TeacherProfileFactory.build(user__id=2)
        form = StoryForm(
            user,
            profile,
            {
                'body': "Cool story",
                'submitter_name': "Joe",
                'nominal_date': "4/20/2013",
                },
            )

        assert form.is_valid(), form.errors
        story = form.save(commit=False)

        assert story.submitter_name == ''
        assert story.nominal_date is None



class TestTeacherProfileForm:
    def test_save_assigns_user(self):
        """TeacherProfileForm assigns user to the profile before saving."""
        user = UserFactory.build()
        form = TeacherProfileForm(user, {'school': "Sample Elementary"})

        assert form.is_valid()
        profile = form.save(commit=False)

        assert profile.user == user
