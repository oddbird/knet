import factory

from knet.accounts import models



class KNetModelFactory(factory.DjangoModelFactory):
    """We don't want to go to the database to get the next sequence value."""
    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls):
        """Set up an initial sequence value for Sequence attributes."""
        return 0



class UserFactory(KNetModelFactory):
    FACTORY_FOR = models.User

    username = factory.Sequence(lambda n: "test{0}".format(n))


    @classmethod
    def _prepare(cls, create, **kwargs):
        """Special handling for ``set_password`` method."""
        password = kwargs.pop("password", None)
        user = super(UserFactory, cls)._prepare(False, **kwargs)
        if password:
            user.set_password(password)
        if create:
            user.save()
        return user
