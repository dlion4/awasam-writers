import json
import secrets
import string
import threading
import time
from typing import Any
from urllib.parse import parse_qs

from django.conf import settings
from django.contrib.auth.models import User as UserObject
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.http import HttpRequest
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import base36_to_int
from django.utils.http import int_to_base36
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import timedelta

from .tasks import send_background_email



class BackgroundEmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_background_email(self.email)


class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    """
        A token generator that creates expiring tokens for password reset.
        Explanation:
        Generates a token for password reset with an expiry time. The token includes
        the user's primary key and a timestamp indicating when the token was generated.
        timestamp and is validated based on the expiry time.

        Args:
        - self
        - user: The user for whom the token is generated.

        Returns:
        - str: The generated token.

        Raises:
        - None

        Example usage:
            >> token = expiring_token_generator.make_token(user)
            >> is_valid = expiring_token_generator.check_token(user, token)
    """

    TOKEN_EXPIRY_TIMEOUT:int = 300 # Expiry set to 5 minutes | will change later based on the requirements
    def make_token(self, user):
        timestamp = int(time.time())
        return f"{super().make_token(user)}-{int_to_base36(timestamp)}"

    def check_token(self, user, token):
        try:
            token, timestamp = token.rsplit("-", 1)
            timestamp = base36_to_int(timestamp)
        except (ValueError, TypeError):
            return False
        # Check token age
        if time.time() - timestamp > self.TOKEN_EXPIRY_TIMEOUT:  # The time duration for whcih the token remains valid
            return False
        return super().check_token(user, token)

expiring_token_generator = ExpiringTokenGenerator()



class BuildMagicLink:

    def _build_link_from_path(
        self, request:HttpRequest, path:str, kwds:dict | None=None,
        )->str:

        return request.build_absolute_uri(reverse(path, kwargs=kwds))

    def  build_url_from_path(
        self, request:HttpRequest, path:str, kwds:dict | None=None,
    ):
        """
        Builds a URL from a given path.

        Explanation:
        This function constructs a URL using the provided path, args, and kwargs.

        Args:
        - request: An HttpRequest object.
        - path: A string representing the path for the URL.
        - args: Additional positional arguments. (optional)
        - kwargs: Additional keyword arguments. (optional)

        Returns:
        The constructed URL.
        """
        return self._build_link_from_path(
            request, path, kwds,
        )

    def build_login_link_from_user(self, request:HttpRequest, user:UserObject):
        """
        Builds a login link for a given user.

        Args:
            request (HttpRequest): The HTTP request object.
            user (UserObject): The user object for which the login link is being built.

        Returns:
            str: The absolute URL of the login link.

        This method generates a login link for a given user by encoding the user's primary key
        and generating a token using the default token generator. It then constructs the login
        link by concatenating the user's encoded primary key, the generated token, and the
        "/users/login/" URL path. The resulting URL is obtained by calling the
        `build_absolute_uri` method on the request object.

        Example:
            If the user's primary key is 123 and the generated token is "abc", the login link
            will be "http://example.com/users/login/MTIzNA/abc/".
        """

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = expiring_token_generator.make_token(user)
        return self._build_link_from_path(
            request,
            "users:login_with_link",
            {
                "uid": uid,
                "token": token,
            },
        )


    def send_login_email(
        self, user:UserObject,email_template:str= "account/mails/login.html", context:dict={}):  # noqa: B006
        link = self.build_login_link_from_user(self.request, user)
        thread = threading.Thread(
            target=send_background_email,
            args=(
                user,
               email_template,
                {
                    "user": user,
                    "email":user.email,
                    "link": link,
                    "subject": "Login Request",
                    "from_email": settings.DEFAULT_FROM_EMAIL,
                    "extra": {k:v for k,v in context.items() if v is not None},
                },
            ),
        )
        thread.start()

    def send_signup_email(
        self, email,email_template:str="account/mails/signup.html", context:dict={},  # noqa: B006
        )->None:
        link=self._build_link_from_path(request=self.request, path="users:signup")
        thread = threading.Thread(target=send_background_email, args=(
            None, email_template,
            {
                "email": email,
                "link": link,
                "subject": "Earnkraft Registration",
                "from_email": "no-reply@Earnkraft.com",
                "extra": {k:v for k,v in context.items() if v is not None},
            },
            None,
        ))
        thread.start()

    def send_welcome_email(
        self, email,email_template:str="account/mails/welcome/index.html", context:dict={},  # noqa: B006
    )->None:
        """This is the welcome email sent wen a new user just register can be both for
        the
        Referred and the un referred users
        """
        thread = threading.Thread(target=send_background_email, args=(
            None, email_template,
            {
                "email": email,
                "subject": "Welcome to Earnkraft Investment",
                "from_email": "no-reply@Earnkraft.com",
                "extra": {k:v for k,v in context.items() if v is not None},
            },
            None,
        ))
        thread.start()
        # Wait for the thread to complete
        
    def _generate_token(self,user_pk):
        """
        Generates a referral code based on the provided user primary key.

        Parameters:
            user_pk (int): The primary key of the user.

        Returns:
            str: The generated referral code.
        Example:
            >>> generate_referral_code(123)
            'cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377'
        """
        random_letters = "".join(secrets.choice(string.ascii_lowercase) for _ in range(2))
        random_str = "".join(
            secrets.choice(string.ascii_lowercase + string.digits) for _ in range(45))
        timestamp = int(time.time())
        return f"{random_letters}-{user_pk}-{random_str}-{timestamp}"
    
    def __validate_token(self, token:str, duration:str="minutes", timeout:int=5): # the timeout for this code to be marked expired is 5 minutes by default
        """
            Validates a referral code.

            Args:
                code (str): The referral code to be validated.

            Returns:
                bool: True if the code is valid and not older than 7 days, False otherwise.

            Raises:
                ValueError: If the code does not have the expected format.

            This function splits the code into its components using the '-' delimiter.
            It checks if the prefix has the expected length. It then converts the timestamp
            to an integer and calculates the age of the code. Finally, it returns True if
            the code is valid and not older than 7 days, and False otherwise.

            Example:
                >>> validate_referral_code('cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377')
                True
        """
        prefix_len:int = 2
        try:
            prefix, user_pk, random_str, timestamp = token.rsplit("-", 3)
            if len(prefix) != prefix_len:
                return False
            timestamp = int(timestamp)
        except ValueError:
            return False
        # Check if the code is older than 5 minutes
        code_age = timezone.now() - timezone.datetime.fromtimestamp(
            timestamp, tz=timezone.utc)
        if duration == "days":
            return not code_age > timedelta(days=timeout)
        return not code_age > timedelta(minutes=timeout)

    def generate_account_activation_token(self, user_pk):
        return self._generate_token(user_pk)
    
    def validate_account_activation_token(self, code):
        return self.__validate_token(token=code)
    
    def generate_reference_code(self, user_pk):
        return self._generate_token(user_pk)

    def validate_reference_code(self, code, timeout:int=7): 
        # default timeout is set to 7 days by default for the reference code validation before being marked expired
        return self.__validate_token(token=code,duration="days", timeout=timeout)
        



class JavascriptPostCleanFormViewMixin:
    def _post_data(self, request:HttpRequest):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid Post form data"})
        return data

    def ajax_filter_formatted_data(self, request):
        data = self._post_data(request)
        parsed_data = parse_qs(data)
        if "csrfmiddlewaretoken" in parsed_data:
            del parsed_data["csrfmiddlewaretoken"]
        return  {key: values[0] for key, values in parsed_data.items()}

    def fetch_filter_formatted_data(self,request):
        return self._post_data(request)

