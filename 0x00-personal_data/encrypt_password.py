#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """ Function that expects one string argument name
    password and returns a salted
    """
    b_p = password.encode()
    return hashpw(b_p, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function that expects 2 arguments and
    returns a boolean
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
