#!/usr/bin/env python3
""" API authentication. """
from flask import request
from typing import List, TypeVar


class Auth:
    """ 3. Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method that returns False
        """
        return False

    def def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
