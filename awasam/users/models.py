
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.db import models
from .managers import UserManager
from .actions import generate_reference_code



class User(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)
    username = models.CharField(
        _("Username"), max_length=255, unique=False, blank=True,
    )
    verified = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=100,
        choices=(
            ("Student","Student"),
            ("Writer","Writer"),
            ("Editor","Editor"),
            ("Admin","Admin"),
        ),
        default="Student",
    )
    date_joined = models.DateField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()


    @cached_property
    def referrals_count(self):
        return self.referrals().count()


    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        return super().save(*args, **kwargs)



class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile_user",
    )
    full_name = models.CharField(blank=True, max_length=100)
    initials = models.CharField(max_length=2, blank=True)
    referred_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="profile_referred_by",
    )
    referral_code = models.CharField(max_length=5000, blank=True)
    course_orders = models.ManyToManyField("orders.Course", blank=True)
    normal_orders = models.ManyToManyField("orders.Normal", blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True,null=True, upload_to="profiles/")

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a referral code and initials.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            None
        """
        # save first to get the profile pk to be able to generate the full_name
        super().save(*args, **kwargs)
        # Generate a referral code using the primary key
        self.referral_code = generate_reference_code(self.pk)

        # Generate initials using the full name
        # self.initials = self.generate_initials()

        # Call the parent class save method
    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})

    def generate_initials(self) -> str | None:
        """
        Use the full name that has been generated to get the initial.

        Returns:
            str | None: The initials of the first two names in the full name, or None if
            the full name is not available.
        """
        if self.full_name:
            """Use the full name that has been generated to get the initial"""
            initials = [name[0].upper() for name in self.full_name.split(" ")]
            return "".join(initials) if initials else self.initials
        return None

    def get_referral_signup_url(self):
        """
        Returns the URL for the referral signup page with the current user's referral code.

        :return: A string representing the URL for the referral signup page.
        :rtype: str
        """
        return reverse("users:referred-signup", kwargs={
            "referral_code":self.referral_code,
        })

    @cached_property
    def referrals(self) -> int:
        # find the total referrals by a user and cache the result
        return self.user.referrals_count
    @property
    def profile_identity(self):
        return self.user.email[:self.user.email.index("@")].title()


