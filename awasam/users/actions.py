import secrets, random, time, string
from datetime import datetime, timedelta
from django.utils import timezone


def generate_reference_code(user_pk):
    """
    Generates a referral code based on the provided user primary key.

    Parameters:
        user_pk (int): The primary key of the user.

    Returns:
        str: The generated referral code.
    Example:
        >>> generate_reference_code(123)
        'cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377'
    """
    random_letters = "".join(secrets.choice(string.ascii_lowercase) for _ in range(2))
    random_str = "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(45))
    timestamp = int(time.time())
    return f"{random_letters}-{user_pk}-{random_str}-{timestamp}"


def validate_reference_code(code:str)->bool:
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
            >>> validate_reference_code('cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377')
            True
    """
    prefix_len:int = 2
    try:
        prefix, user_pk, random_str, timestamp = code.rsplit("-", 3)
        if len(prefix) != prefix_len:
            return False
        timestamp = int(timestamp)
    except ValueError:
        return False
    # Check if the code is older than 7 days
    code_age = timezone.now() - timezone.datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return not code_age > timedelta(days=7)

