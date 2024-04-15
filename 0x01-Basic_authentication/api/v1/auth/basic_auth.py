#!/usr/bin/env python3
""" Basic auth """
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Class Basic auth """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """ Method that returns the Base64 part of the
        Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        basic_auth = authorization_header.split(" ")[-1]
        return basic_auth

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """ Method that returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64_authorization_header.encode('utf-8')
            decode64 = base64.b64decode(decoded)
            return decode64.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """ Method that returns the user email and password
        from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        user_email = decoded_base64_authorization_header.split(':')[0]
        user_pwd = decoded_base64_authorization_header[len(user_email) + 1:]
        return (user_email, user_pwd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ Method that returns the User instance based
        on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
            if not user or user == []:
                return None
            for usr in user:
                if usr.is_valid_password(user_pwd):
                    return usr
            return None
        except Exception:
            return None
