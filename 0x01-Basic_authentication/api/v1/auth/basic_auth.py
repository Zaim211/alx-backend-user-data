#!/usr/bin/env python3
""" Basic auth """
from .auth import Auth
import base64


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
