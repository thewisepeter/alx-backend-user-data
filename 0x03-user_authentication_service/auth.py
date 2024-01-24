#!/usr/bin/env python3
""" module that takes in a password string
    arguments and returns bytes.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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


def _generate_uuid() -> str:
    '''
        function that generates unique id
    '''
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
            function that registers new user
        '''
        try:
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add user to database
            return self._db.add_user(email, _hash_password(password))

        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''
            validates a log in
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''
            function that creates a session
        '''
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id

        except NoResultFound:
            return False

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
            method that finds user by session id
        '''

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        '''
            function that destroys session
        '''
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''
            password reset function
        '''
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()

            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
            updates password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)

            # Hash the new password and update the user's hashed_password field
            user.hashed_password = _hash_password(password)

            # Set reset_token to None
            user.reset_token = None
            return None
        except NoResultFound:
            raise ValueError
