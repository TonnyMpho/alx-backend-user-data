#!/usr/bin/env python3
""" API authentication. """
from flask import request
from typing import List, TypeVar


class Auth:
    """ 3. Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for the given path """
        if path is None or excluded_paths is None:
            return True

        path = path.rstrip('/') + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request """
        return None
