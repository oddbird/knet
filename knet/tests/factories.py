import factory

from knet.accounts import models



class UserFactory(factory.Factory):
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
