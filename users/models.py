from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser."""

    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Override save to set can_data_be_shared based on age."""
        # Force False si âge < 15
        if self.age and self.age < 15:
            self.can_data_be_shared = False

        # Si age >= 15, on garde la valeur choisie par l'utilisateur (True ou False)
        super().save(*args, **kwargs)
