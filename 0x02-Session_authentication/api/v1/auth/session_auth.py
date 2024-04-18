#!/usr/bin/env python3
""" Module for SessionAuth """
from .auth import Auth
from uuid import uuid4
# from models.user import User


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
