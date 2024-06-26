#!/usr/bin/env python3
""" Module for SessionAuth """
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """" Class Session Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Instance method that creates a Session ID
        for a user_id. """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Instance method that returns a User ID based
        on a Session ID. """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Instance method that returns a User instance based
        on a cookie value. """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ Instance method that deletes the user session / logout """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
