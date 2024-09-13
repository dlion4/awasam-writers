from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, User
from typing import Any

@receiver(post_save, sender=User)
def create_user_profile(
    sender: type[User],
    instance: User,
    created: bool,  # noqa: FBT001
    **kwargs: Any,
) -> None:
    """
    Create a user profile when a new user is created, or save the existing user profile
    when the user is updated.

    Args:
        sender (Type[User]): The class of the sender of the signal.
    Parameters:
        sender (class): The class of the sender of the signal.
        instance (User): The instance of the User model that triggered the signal.
        created (bool): A boolean indicating whether the User instance was created or
            whether it was updated.
        whether it was updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None| Optional[None]:
            This function does not return anything. However, it ensures that a profile
            associated with the created user was also created.
        None| But ensure a profile associated with the created user was also created
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        """This part saves the profile to the user model attached"""
        instance.profile_user.save()
