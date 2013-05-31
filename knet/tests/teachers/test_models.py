from .factories import TeacherProfileFactory



def test_str():
    tp = TeacherProfileFactory.build(user__name="Someone")

    assert str(tp) == "Teacher Profile for Someone"
