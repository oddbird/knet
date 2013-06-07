from django.core.exceptions import ValidationError
import pytest

from .factories import StoryFactory, TeacherProfileFactory



class TestTeacherProfile:
    def test_str(self):
        tp = TeacherProfileFactory.build(user__name="Someone")

        assert str(tp) == "Teacher Profile for Someone"



class TestStory:
    def test_str(self):
        """String representation is the first ten words of the body."""
        s = StoryFactory.build(
            body="A long time ago in a galaxy far, far away. "
            "It is a period of civil war."
            )

        assert str(s) == "A long time ago in a galaxy far, far away...."



    def test_cannot_publish_a_private_story(self):
        """Teacher cannot publish a story the submitter has requested be private."""
        s = StoryFactory.build(body="Love ya", private=True, published=True)

        with pytest.raises(ValidationError):
            s.clean()
