#!/usr/bin/env python3
'''
    module defining the basic_auth class
'''
from api.v1.auth.auth import Auth


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
