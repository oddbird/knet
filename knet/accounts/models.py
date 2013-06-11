from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    name = models.TextField(blank=True)


    def __str__(self):
        """String representation is friendly name."""
        return self.get_name()


    def get_name(self):
        """Return the friendliest available name for this user."""
        return self.name or self.get_full_name() or self.username
