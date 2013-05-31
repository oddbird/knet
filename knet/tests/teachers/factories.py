import factory

from knet.teachers.models import TeacherProfile

from ..factories import UserFactory



class TeacherProfileFactory(factory.Factory):
    FACTORY_FOR = TeacherProfile

    user = factory.SubFactory(UserFactory)
