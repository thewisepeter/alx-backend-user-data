#!/usr/bin/env python3
'''
    module defining the Auth class
'''
from flask import request
from typing import List, TypeVar
import re

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
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

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
