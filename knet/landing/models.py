"""Landing page models."""
from django.contrib import auth
from django.db import models
from django.utils.timezone import now


class Lead(models.Model):
    """Someone who signs up for more info at the landing page."""
    email = models.EmailField()
    following_up = models.ForeignKey(
        auth.get_user_model(),
        blank=True,
        null=True,
        limit_choices_to={'is_staff': True},
        )
    notes = models.TextField(blank=True)
    signed_up = models.DateTimeField(default=now)


    def __str__(self):
        """String representation is the email address."""
        return self.email
