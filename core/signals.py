from registration.signals import user_registered
from django.dispatch import receiver


@receiver(user_registered)
def registered_user(sender, **kwargs):
    from .models import Profile
    user = kwargs.get("user")
    Profile.objects.create(user=user)

__all__ = [
    "registered_user",
]
