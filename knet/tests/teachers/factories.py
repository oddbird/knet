import factory

from knet.teachers import models

from ..factories import UserFactory, KNetModelFactory



class TeacherProfileFactory(KNetModelFactory):
    FACTORY_FOR = models.TeacherProfile

    user = factory.SubFactory(UserFactory)



class StoryFactory(KNetModelFactory):
    FACTORY_FOR = models.Story

    profile = factory.SubFactory(TeacherProfileFactory)
    body = "It was a dark and stormy night."
