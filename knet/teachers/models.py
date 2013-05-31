from django.db import models

from ..accounts.models import User



class TeacherProfile(models.Model):
    """A profile for a user who is a teacher."""
    user = models.OneToOneField(User, related_name='teacher_profile')
    school = models.TextField(blank=True)


    def __str__(self):
        return "Teacher Profile for {}".format(self.user)
