#!/usr/bin/python3
""" Hash password """
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Method  that takes in a password string arguments
    and returns bytes.
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())
