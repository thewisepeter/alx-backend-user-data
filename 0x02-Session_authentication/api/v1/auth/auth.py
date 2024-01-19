#!/usr/bin/env python3
'''
    module defining the Auth class
'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''
        class definition of the Auth
    '''

    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
        '''
            returns False - path and excluded_paths
            will be used later, now, you don’t need
            to take care of them
        '''
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(str.strip, excluded_paths):
                pattern = ''
                if exclusion_path.endswith('*'):
                    pattern = exclusion_path[:-1]
                    if path.startswith(pattern):
                        return False
                elif exclusion_path.endswith('/'):
                    pattern = exclusion_path[:-1]
                    if path == pattern or path.startswith(pattern + '/'):
                        return False
                else:
                    pattern = exclusion_path
                    if path == pattern or path.startswith(pattern + '/'):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
           returns None - request will be the Flask
           request object

        if request is None:
            return None

        header = request.headers.get('Authorization')
        if header:
            return header
        return None
        '''
        return request.headers.get('Authorization') if request else None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
           returns None - request will be the Flask request
           object
        '''
        return None

    def session_cookie(self, request=None):
        '''
            returns a cookie value from a request

            Return None if request is None
            Return the value of the cookie named _my_session_id
            from request - the name of the cookie must be defined
            by the environment variable SESSION_NAME
        '''
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
