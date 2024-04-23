#!/usr/bin/env python3
""" Hash password """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ Method  that takes in a password string arguments
    and returns bytes.
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Function that return a string representation of a new UUID """
    return str(uuid4())


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

    def create_session(self, email: str) -> Union[None, str]:
        """ Method that find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, str]:
        """ Method that takes a single session_id string argument and
        returns the corresponding User or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ Method that takes a single user_id integer argument
        and returns None. and updates the corresponding
        user’s session ID to None """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Method that Generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Method that update the password with token """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        user_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=user_pwd,
                             reset_token=None)
