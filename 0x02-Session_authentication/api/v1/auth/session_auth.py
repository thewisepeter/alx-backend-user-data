#!/usr/bin/env python3
'''
    module defining the basic_auth class
'''
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    '''
        definition of the SessionAuth class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
            instance method def create_session(self, user_id:
            str = None) -> str: that creates a Session ID for
            a user_id:
            Return None if user_id is None
            Return None if user_id is not a string
            Otherwise:
            Generate a Session ID using uuid module and uuid4()
            like id in Base
            Use this Session ID as key of the dictionary
            user_id_by_session_id - the value for this key must be user_id
            Return the Session ID
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
            returns a User ID based on a Session ID:

            Return None if session_id is None
            Return None if session_id is not a string
            Return the value (the User ID) for the key
            session_id in the dictionary user_id_by_session_id.
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return str(self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        '''
            returns a User instance based on a cookie value:

            You must use self.session_cookie(...) and
            self.user_id_for_session_id(...) to return the
            User ID based on the cookie _my_session_id
        '''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''

            deletes the user session / logout:

            If the request is equal to None, return False
            If the request doesn’t contain the Session ID cookie,
            return False - you must use self.session_cookie(request)
            If the Session ID of the request is not linked to any User ID,
            return False - you must use self.user_id_for_session_id(...)
            Otherwise, delete in self.user_id_by_session_id the Session ID
            (as key of this dictionary) and return True
        '''
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
