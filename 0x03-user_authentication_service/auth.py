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

    def get_user_from_session_id(self, session_id: str) -> User:
        """Method that finds a user based on a session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Dletes the current user session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except Exception:
            return

    def get_reset_password_token(self, email: str) -> str:
        """Method that generates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except Exception:
            raise ValueError
