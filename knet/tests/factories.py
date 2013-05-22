import factory

from knet.accounts import models



class ProfileFactory(factory.Factory):
    FACTORY_FOR = models.Profile

    username = factory.Sequence(lambda n: "test{0}".format(n))


    @classmethod
    def _prepare(cls, create, **kwargs):
        """Special handling for ``set_password`` method."""
        password = kwargs.pop("password", None)
        user = super(ProfileFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
