#!/usr/bin/env python3
""" 5. Encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    function that expects one string argument name password and
    returns a salted, hashed password, which is a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    function that expects 2 arguments and returns a boolean.
    Arguments:
    - hashed_password: bytes type
    - password: string type
    Uses bcrypt to validate that the provided password matches
    the hashed password.
    """
    return bcrypt.checkpw(password.encode("UTF-8"), hashed_password)
