#!/usr/bin/python3
""" Hash password """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Metho that register users """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation for login the users """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_pwd = user.hashed_password
        pwd = password.encode('utf-8')

        if bcrypt.checkpw(pwd, user_pwd):
            return True
        return False


def _hash_password(password: str) -> bytes:
    """ Method  that takes in a password string arguments
    and returns bytes.
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())
