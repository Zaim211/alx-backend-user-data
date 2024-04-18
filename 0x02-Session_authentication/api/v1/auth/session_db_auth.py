#!/usr/bin/python3
""" Module for Sessions in database """
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Class that handle session data
    in a database """
    def create_session(self, user_id=None):
        """ Method that creates and stores new instance
        of UserSession and returns the Session ID
        """
        session_id = super().create_session(user_id)
        user = UserSession(session_id: session_id, user_id: user_id)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Method that returns the User ID by requesting
        UserSession in the database based on session_id
        """
        try:
            user_id = UserSession.search({'session_id': session_id})
        except ValueError:
            return None

    def destroy_session(self, request=None):
        """ Method destroys the UserSession based on
        the Session ID from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session_user = UserSession.search({'session_id': session_id})
        if session_user:
            session_user[0].remove()
            return True
        return False
