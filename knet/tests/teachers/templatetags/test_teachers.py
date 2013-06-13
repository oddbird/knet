from knet.teachers.templatetags.teachers import teacher_profile

from ...factories import UserFactory
from ..factories import TeacherProfileFactory


class TestTeacherProfile:
    def test_has_teacher_profile(self, db):
        tp = TeacherProfileFactory.create()

        assert teacher_profile(tp.user) == tp


    def test_has_no_teacher_profile(self, db):
        u = UserFactory.create()

        assert teacher_profile(u) is None
