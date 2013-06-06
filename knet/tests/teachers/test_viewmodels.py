from knet.teachers.viewmodels import ViewTeacher

from .factories import TeacherProfileFactory, StoryFactory



def test_str():
    """Passes through string representation of teacher."""
    tp = TeacherProfileFactory.build(user__name="A Song")
    vt = ViewTeacher(tp)

    assert str(vt) == "A Song"


def test_attributes():
    """Some attributes pass through to user or profile."""
    tp = TeacherProfileFactory.build()
    vt = ViewTeacher(tp)

    assert vt.user == tp.user
    assert vt.school == tp.school
    assert vt.date_joined == tp.user.date_joined
    assert vt.bio == tp.user.bio
    assert vt.full_name == str(tp.user)


def test_stories(db):
    """Stories method gets all stories for profile."""
    s = StoryFactory.create()
    vt = ViewTeacher(s.profile)

    assert list(vt.stories()) == [s]
