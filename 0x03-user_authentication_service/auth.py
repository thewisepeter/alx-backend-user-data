#!/usr/bin/env python3
""" module that takes in a password string
    arguments and returns bytes.
"""
import bcrypt


def _hash_password(password: str) -> str:
    '''
        function that returns byte representation
        of a password
    '''
    # Encode the plain-text password to bytes using UTF-8
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Return the hashed password as a byte representation
    return hashed_password
