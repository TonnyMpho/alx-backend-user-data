#!/usr/bin/env python3
""" Authentication module
"""
import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and returns bytes
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """ generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method that takes email and password strings and
        registers a user
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """method that checks if the password is correct
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Method that  takes an email string argument and creates
        a new session id and returns the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except Exception:
            return None
