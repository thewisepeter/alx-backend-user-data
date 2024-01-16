#!/usr/bin/env python3
'''
    module defining the basic_auth class
'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, Optional
from models.user import User

T = TypeVar('T')

class BasicAuth(Auth):
    '''
        definition of the class basic-auth
    '''
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization
            header string.

        Returns:
            str: The Base64 part of the Authorization header.

        Returns None if:
        - authorization_header is None
        - authorization_header is not a string
        - authorization_header doesn’t start by Basic
        (with a space at the end)
        """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None

        # Check if authorization_header starts with "Basic"
        # (with a space at the end)
        if not authorization_header.startswith("Basic "):
            return None

        # Extract the value after "Basic "
        base64_part = authorization_header[6:]
        return base64_part

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 string base64_authorization_header.

        Args:
            base64_authorization_header (str): The Base64 string.

        Returns:
            str: The decoded value as UTF-8 string.

        Returns None if:
        - base64_authorization_header is None
        - base64_authorization_header is not a string
        - base64_authorization_header is not a valid Base64 (using try/except)
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None

        try:
            # Attempt to decode the Base64 string
            decoded_value = base64.b64decode(
                base64_authorization_header
                ).decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            # Return None if decoding fails (invalid Base64)
            return None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[T]:
        """
        Returns the User instance based on user email and password.

        Args:
            user_email (str): User email.
            user_pwd (str): User password.

        Returns:
            TypeVar('User'): User instance or None.

        Returns None if:
        - user_email is None or not a string
        - user_pwd is None or not a string
        - No User instance with the given email is found in the database
        - user_pwd is not the password of the User instance found
        """
        if not isinstance(user_email, str) or user_email is None:
            return None

        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        # Assuming User.search is a class method that looks up users by email
        user_instance = User.search(user_email)

        if user_instance is None:
            return None

        if not user_instance.is_valid_password(user_pwd):
            return None

        return user_instance