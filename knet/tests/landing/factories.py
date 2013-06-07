"""Factories for landing-page models."""
from knet.landing import models

from ..factories import KNetModelFactory



class LeadFactory(KNetModelFactory):
    FACTORY_FOR = models.Lead

    email = "foo@example.com"
