#!/usr/bin/env python3
""" Expiration date to a Session ID """
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Class that adds an
    expiration date to a Session ID
    """
    def __init__(self):
        """ Method that Assign an instance attribute
        session_duration """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Method that Create a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Method that returns a user ID based on a session ID """
        if session_id is None:
            return None
        user_session_id = self.user_id_by_session_id.get(session_id)
        if user_session_id is None:
            return None
        if self.session_duration <= 0:
            return user_session_id.get('user_id')
        if "created_at" not in user_session_id.keys():
            return None
        created_at = user_session_id.get('created_at')
        expire_time = timedelta(seconds=self.session_duration)
        success = created_at + expire_time
        if success < datetime.now():
            return None
        return user_session_id.get('user_id')
