import factory

from knet.stories import models

from ..factories import KNetModelFactory
from ..teachers.factories import TeacherProfileFactory



class StoryFactory(KNetModelFactory):
    FACTORY_FOR = models.Story

    profile = factory.SubFactory(TeacherProfileFactory)
    body = "It was a dark and stormy night."
