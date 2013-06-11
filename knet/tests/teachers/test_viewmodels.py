from datetime import datetime

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
    assert vt.bio == tp.bio
    assert vt.full_name == str(tp.user)


def test_stories(db):
    """Stories method gets all stories for profile, most recent first."""
    s1 = StoryFactory.create(created=datetime(2013, 6, 11))
    s2 = StoryFactory.create(created=datetime(2013, 6, 10), profile=s1.profile)
    s3 = StoryFactory.create(created=datetime(2013, 6, 12), profile=s1.profile)

    vt = ViewTeacher(s1.profile)

    assert list(vt.stories()) == [s3, s1, s2]
