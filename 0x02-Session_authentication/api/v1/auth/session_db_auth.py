#!/usr/bin/env python3
""" Module for Sessions in database """
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """ Class that handle session data
    in a database """
    def create_session(self, user_id: str = None) -> str:
        """ Method that creates and stores new instance
        of UserSession and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Method that returns the User ID by requesting
        UserSession in the database based on session_id
        """
        try:
            user = UserSession.search({'session_id': session_id})[0]
        except BaseException:
            return None

        if self.session_duration <= 0:
            return user.user_id

        if not isinstance(user.created_at, datetime):
            return None

        exp_time = timedelta(seconds=self.session_duration)
        if datetime.utcnow() > user.created_at + exp_time:
            return None
        return user.user_id

    def destroy_session(self, request=None) -> bool:
        """ Method destroys the UserSession based on
        the Session ID from the request cookie
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        user = UserSession.search({'session_id': session_id})[0]
        user.remove()
        return True
