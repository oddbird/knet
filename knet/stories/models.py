from django.core.exceptions import ValidationError
from django.db import models
from django.utils import text, timezone

from ..accounts.models import User


class Story(models.Model):
    """A story from a student about the impact a teacher had on them."""
    teacher = models.ForeignKey(User)
    body = models.TextField()
    # submitter requested that this story remain private
    private = models.BooleanField(default=False)
    submitter_name = models.TextField(blank=True)
    submitter_email = models.EmailField(blank=True, max_length=254)

    # teacher has approved this story for their profile
    published = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return text.Truncator(self.body).words(10)


    def clean(self):
        if self.private and self.published:
            raise ValidationError("Cannot publish a private story.")
