from django.core.exceptions import ValidationError
from django.db import models
from django.utils import text, timezone

from ..accounts.models import User



class TeacherProfile(models.Model):
    """A profile for a user who is a teacher."""
    user = models.OneToOneField(User, related_name='teacher_profile')
    school = models.TextField()
    bio = models.TextField(blank=True)


    def __str__(self):
        return "Teacher Profile for {}".format(self.user)



class Story(models.Model):
    """A story from a student about the impact a teacher had on them."""
    profile = models.ForeignKey(TeacherProfile, related_name='stories')
    body = models.TextField()

    # this is always the user who actually created the story
    submitter = models.ForeignKey(User, related_name='submitted_stories')
    # overrides for stories posted by proxy to own profile
    submitter_name = models.TextField(blank=True)
    submitter_email = models.EmailField(blank=True, max_length=254)
    nominal_date = models.DateField(blank=True, null=True)
    # submitter requested that this story remain private
    private = models.BooleanField(default=False)

    # teacher has approved this story for their profile
    published = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return text.Truncator(self.body).words(10)


    def clean(self):
        if self.private and self.published:
            raise ValidationError("Cannot publish a private story.")

    class Meta:
        verbose_name_plural = 'stories'
