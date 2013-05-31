from knet.stories.forms import StoryForm

from ..factories import UserFactory



def test_save_assigns_teacher():
    """StoryForm assigns its teacher to the story before saving."""
    teacher = UserFactory.build()
    form = StoryForm(teacher, {'body': "Cool story bro"})

    assert form.is_valid()
    story = form.save(commit=False)

    assert story.teacher == teacher
