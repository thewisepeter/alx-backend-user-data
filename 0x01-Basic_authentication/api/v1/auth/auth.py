#!/usr/bin/env python3
'''
    module defining the Auth class
'''
from flask import request
from typing import List, TypeVar


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
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            # Make the comparison slash tolerant
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*" and path.startswith(excluded_path[:-1]):
                return False
        return False

    def authorization_header(self, request=None) -> str:
        '''
           returns None - request will be the Flask
           request object
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
           returns None - request will be the Flask request
           object
        '''
        return None
