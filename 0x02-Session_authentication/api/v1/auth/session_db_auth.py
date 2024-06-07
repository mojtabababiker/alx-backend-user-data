#!/usr/bin/env python3
"""
Session base with databse-save authonetication model
"""
import os
from uuid import uuid4
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Session base with databse-save authonetication class
    """
    def create_session(self, user_id=None):
        """
        overload: add the session to the databse
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session = UserSession(user_id=user_id, id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrive the user id from the session with session id
        on the database
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            session = UserSession.get(session_id)
        except Exception:
            return None
        user_id = session.user_id
        return user_id

    def destroy_session(self, request=None):
        """
        Overload: to destroy the session on the databse
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        session = self.user_id_for_session_id(session_id)
        if session is None:
            return False
        UserSession.remove(session_id)
        return True
