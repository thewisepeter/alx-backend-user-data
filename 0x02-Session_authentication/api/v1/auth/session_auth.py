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
