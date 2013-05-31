import factory

from knet.teachers.models import TeacherProfile

from ..factories import UserFactory, KNetModelFactory



class TeacherProfileFactory(KNetModelFactory):
    FACTORY_FOR = TeacherProfile

    user = factory.SubFactory(UserFactory)
