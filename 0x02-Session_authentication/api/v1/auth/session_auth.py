#!/usr/bin/env python3
""" Module for SessionAuth """
from .auth import Auth
from uuid import uuid4


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
