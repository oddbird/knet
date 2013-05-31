import factory

from knet.stories import models

from ..factories import UserFactory



class StoryFactory(factory.Factory):
    FACTORY_FOR = models.Story

    teacher = factory.SubFactory(UserFactory)
    body = "It was a dark and stormy night."
